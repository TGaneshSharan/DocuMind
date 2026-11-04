def create_chunks(text, chunk_size=500, overlap=100):

    text = text.strip()

    if not text:
        return []

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(text), step):

        chunk = text[start:start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks