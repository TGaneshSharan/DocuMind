
from vector_store import collection

from pdf_processer_file import extract_text_from_pdf
from text_chunker import create_chunks
from embeddings import generate_embedding


def ingest_pdf(pdf_path, source_name):

    # Remove old chunks belonging to this PDF
    collection.delete(
        where={"source": source_name}
    )

    pages = extract_text_from_pdf(pdf_path)

    total_chunks = 0

    for page in pages:

        chunks = create_chunks(page["text"])

        for chunk in chunks:

            vector = generate_embedding(chunk)

            chunk_id = (
                f"{source_name}_page_"
                f"{page['page_number']}_chunk_{total_chunks}"
            )

            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[vector],
                metadatas=[
                    {
                        "source": source_name,
                        "page_number": page["page_number"]
                    }
                ]
            )

            total_chunks += 1

    if total_chunks == 0:
        raise ValueError(
            "No readable text found in this PDF."
        )

    return total_chunks
