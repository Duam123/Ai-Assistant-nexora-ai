
from pathlib import Path
import pymupdf


def read_document(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Document not found.")

    extension = path.suffix.lower()
    pages = []

    if extension == ".txt":
        content = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        pages.append({
            "page": "TXT",
            "text": content
        })

    elif extension == ".pdf":
        document = pymupdf.open(str(path))

        try:
            for page_number, page in enumerate(document, start=1):
                text = page.get_text().strip()

                if text:
                    pages.append({
                        "page": page_number,
                        "text": text
                    })
        finally:
            document.close()

    else:
        raise ValueError(
            "Only PDF and TXT files are supported."
        )

    if not pages:
        raise ValueError(
            "No readable text found. "
            "The PDF may be scanned or image-based."
        )

    full_content = "\n\n".join(
        page["text"] for page in pages
    )

    return {
        "filename": path.name,
        "content": full_content,
        "pages": pages
    }
