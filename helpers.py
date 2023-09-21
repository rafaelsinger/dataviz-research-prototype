import os
PAPER_DIR = "papers"

def get_pdf_path(title):
    # Replace characters not allowed in file names with underscores
    sanitized_title = title.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_")
    pdf_file_path = os.path.join(PAPER_DIR, f"{sanitized_title}")
    return pdf_file_path