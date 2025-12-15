import ollama
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import markdown2


def get_unique_filename(directory, base_name, extension):
    filename = f"{base_name}{extension}"
    counter = 1

    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{base_name} ({counter}){extension}"
        counter += 1

    return os.path.join(directory, filename)


def useLlamaModel(prompt):
    desiredModel = 'llama3.2:3b'

    response = ollama.chat(
        model=desiredModel,
        messages=[{"role": "user", "content": prompt}]
    )

    ollamaResponse = response['message']['content'] or ""

    # Convert markdown → HTML
    html = markdown2.markdown(ollamaResponse)

    # Windows Downloads folder
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # Generate unique filename
    pdf_path = get_unique_filename(downloads_dir, "Generated_Resume", ".pdf")

    # Create PDF
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = [Paragraph(html, styles["Normal"])]

    doc.build(story)

    return pdf_path
