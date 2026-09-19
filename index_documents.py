from pathlib import Path
import sys
from pathlib import Path as PathlibPath

sys.path.insert(0, str(PathlibPath(__file__).parent))

from services.rag_service import rag_service


DOCUMENTS_DIR = Path("data/documents")


def main():
    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    for pdf in pdf_files:
        print(f"Indexing: {pdf.name}")

        count = rag_service.index_pdf(
            str(pdf)
        )

        print(
            f"Indexed {count} chunks from "
            f"{pdf.name}"
        )


if __name__ == "__main__":
    main()