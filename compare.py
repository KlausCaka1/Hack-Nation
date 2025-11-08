import json
import re
import pandas as pd
import pdfplumber
import text_cleaner
import filter_context
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

# Load a pre-trained embedding model (compact but powerful)
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')


# -----------------------------
# 1. Read PDF file
# -----------------------------
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# -----------------------------
# 2. Load JSON
# -----------------------------
json_path = "job-descriptions.json"  # Update path
try:
    with open(json_path, "r", encoding="utf-8") as f:
        jobs_data = [json.loads(line) for line in f]
except json.JSONDecodeError:
    with open(json_path, "r", encoding="utf-8") as f:
        jobs_data = json.load(f)
jobs_df = pd.DataFrame(jobs_data)
jobs_df = jobs_df.head(100)

# -----------------------------
# 4. Clearing the text and apply normalization from NLTK
# -----------------------------
jobs_df.columns = jobs_df.columns.str.strip().str.lower()
jobs_df['clean_desc'] = jobs_df['description'].apply(filter_context.normalization)


# -----------------------------
# 5.Precompute TF-IDF matrix
# -----------------------------
job_texts = jobs_df['clean_desc'].tolist()
vectorizer = TfidfVectorizer()
job_tfidf_matrix = vectorizer.fit_transform(job_texts)

# -----------------------------
# 6. Rank Top Matches
# -----------------------------
def compute_matches(resume_text, top_n_keywords=10, top_n_jobs=20):
    # === 1. Clean + TF-IDF (existing NLTK logic) ===
    resume_clean = filter_context.normalization(resume_text)
    resume_keywords = filter_context.GetTFIDF(resume_clean, top_n=top_n_keywords)

    resume_vec = vectorizer.transform([resume_clean])
    similarity_scores_tfidf = cosine_similarity(resume_vec, job_tfidf_matrix)[0]
    jobs_df['similarity_tfidf'] = similarity_scores_tfidf

    # === 2. Semantic Embeddings (transformers) ===
    resume_emb = semantic_model.encode(resume_clean, convert_to_tensor=True)
    job_embs = semantic_model.encode(jobs_df['clean_desc'].tolist(), convert_to_tensor=True)
    semantic_similarities = util.cos_sim(resume_emb, job_embs)[0].cpu().numpy()
    jobs_df['similarity_semantic'] = semantic_similarities

    # === 3. Keyword Overlap (from TF-IDF) ===
    jobs_df['top_keywords'] = jobs_df['clean_desc'].apply(lambda x: filter_context.GetTFIDF(x, top_n=top_n_keywords))
    jobs_df['keyword_overlap'] = jobs_df['top_keywords'].apply(
        lambda x: len(set(resume_keywords).intersection(set(x)))
    )

    # === 4. Hybrid Combined Score ===
    # You can tune these weights — semantic tends to be more robust
    jobs_df['combined_score'] = (
        0.3* jobs_df['similarity_tfidf']
        + 0.4 * jobs_df['similarity_semantic']
        + 0.3 * (jobs_df['keyword_overlap'] / top_n_keywords)
    )

    # === 5. Sort and Return ===
    top_matches = jobs_df.sort_values(by='combined_score', ascending=False).head(top_n_jobs)

    return resume_keywords, top_matches
