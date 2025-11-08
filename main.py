import tkinter as tk
from tkinter import filedialog, scrolledtext
import compare


# -----------------------------
# GUI Setup
# -----------------------------
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return
    resume_text = compare.extract_text_from_pdf(file_path)
    resume_keywords, top_matches = compare.compute_matches(resume_text)

    # Display results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "=== Resume Keywords ===\n")
    result_text.insert(tk.END, ", ".join(resume_keywords) + "\n\n")
    result_text.insert(tk.END, "=== Top Matching Jobs ===\n\n")

    for idx, row in enumerate(top_matches.itertuples(), start=1):
        # Highlight overlapping keywords
        overlap_keywords = set(resume_keywords).intersection(set(row.top_keywords))

        result_text.insert(tk.END, f"{idx}. {row.title} at {row.company_name}\n")
        result_text.insert(tk.END, f"   TF-IDF similarity : {row.similarity:.3f}\n")
        result_text.insert(tk.END, f"   Keyword overlap   : {row.keyword_overlap} ({', '.join(overlap_keywords)})\n")
        result_text.insert(tk.END, f"   Combined score    : {row.combined_score:.3f}\n")
        result_text.insert(tk.END, f"   Job keywords      : {', '.join(row.top_keywords)}\n")
        result_text.insert(tk.END, "-" * 60 + "\n")

# Main window
root = tk.Tk()
root.title("Resume-Job Matcher")
root.geometry("800x600")

upload_btn = tk.Button(root, text="Upload Resume PDF", command=upload_file)
upload_btn.pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=100, height=30)
result_text.pack(padx=10, pady=10)

root.mainloop()
