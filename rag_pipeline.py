from embeddings import client
from embeddings import generate_embedding

from vector_store import collection


def search_document(question, source_name):

    question_vector = generate_embedding(question)

    # Get documents belonging to the selected PDF
    existing_documents = collection.get(
        where={"source": source_name},
        include=[]
    )

    total_documents = len(existing_documents["ids"])

    if total_documents == 0:
        return [], []

    results = collection.query(

        query_embeddings=[question_vector],

        n_results=min(5, total_documents),

        where={"source": source_name},

        include=["documents", "metadatas"]
    )

    documents = results["documents"][0]
    metadata = results["metadatas"][0]

    return documents, metadata


def generate_answer(question, source_name):

    documents, metadata = search_document(
        question,
        source_name
    )

    if not documents:

        return (
            "No relevant information was found "
            "in the selected document.",
            []
        )

    context = "\n\n".join(documents)

    prompt = f"""
You are DocuMind, an intelligent document assistant.

Your job is to answer questions using the provided PDF context.

Rules:
1. Answer using only the provided context.
2. Do not invent information.
3. If the answer is unavailable, clearly say so.
4. Give a clear and easy-to-understand answer.

PDF Context:
{context}

User Question:
{question}

Answer:
"""

    response = client.models.generate_content(

        model="gemini-3.5-flash",

        contents=prompt
    )

    answer = response.text

    return answer, metadata