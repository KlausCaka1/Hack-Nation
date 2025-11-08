from flask import Flask, render_template, request
import compare
import gemenAI
import markdown2  # for rendering markdown nicely

app = Flask(__name__)


# -----------------------------
# Reqeust to get matches for our CV and find strength and weakness
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    resume_keywords = []
    strengths_weaknesses_html = ""
    matches = []

    if request.method == "POST":
        file = request.files.get("resume_pdf")
        if file:
            # Extract resume text
            resume_text = compare.extract_text_from_pdf(file)

            # Compute keywords and top matches
            resume_keywords, top_matches = compare.compute_matches(resume_text)

            # Prepare prompt for GemenAI
            prompt = ', '.join(
                resume_keywords) + "\n" + resume_text + "\nCan you give strengths and weaknesses for this CV?"
            strengths_weaknesses_md = gemenAI.getSolution(prompt)

            # Convert markdown to HTML
            strengths_weaknesses_html = markdown2.markdown(strengths_weaknesses_md)

            # Convert matches to list of dicts
            matches = top_matches.to_dict(orient="records")

#rendering the templates in this case our main html
    return render_template(
        "main.html",
        resume_keywords=resume_keywords,
        strengths_weaknesses_html=strengths_weaknesses_html,
        matches=matches
    )


if __name__ == "__main__":
    app.run(debug=True)
