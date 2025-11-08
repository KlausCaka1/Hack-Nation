import json
import re
import pandas as pd
import pdfplumber
import text_cleaner
import filter_context
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
jobs_df = jobs_df.head(4000)
jobs_df.columns = jobs_df.columns.str.strip().str.lower()
jobs_df['clean_desc'] = jobs_df['description'].apply(filter_context.normalization)

# Precompute TF-IDF matrix
job_texts = jobs_df['clean_desc'].tolist()
vectorizer = TfidfVectorizer()
job_tfidf_matrix = vectorizer.fit_transform(job_texts)

# -----------------------------
# 3. Rank Top Matches
# -----------------------------
def compute_matches(resume_text, top_n_keywords=20, top_n_jobs=50):
    resume_clean = filter_context.normalization(resume_text)
    resume_keywords = filter_context.GetTFIDF(resume_clean, top_n=top_n_keywords)

    # Vectorize resume
    resume_vec = vectorizer.transform([resume_clean])
    similarity_scores = cosine_similarity(resume_vec, job_tfidf_matrix)[0]
    jobs_df['similarity'] = similarity_scores

    # Keywords and overlap
    jobs_df['top_keywords'] = jobs_df['clean_desc'].apply(lambda x: filter_context.GetTFIDF(x, top_n=top_n_keywords))
    jobs_df['keyword_overlap'] = jobs_df['top_keywords'].apply(lambda x: len(set(resume_keywords).intersection(set(x))))

    # Combined score
    jobs_df['combined_score'] = 0.7 * jobs_df['similarity'] + 0.3 * (jobs_df['keyword_overlap'] / top_n_keywords)
    top_matches = jobs_df.sort_values(by='combined_score', ascending=False).head(top_n_jobs)

    return resume_keywords, top_matches
