def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into overlapping chunks.
    Required for RAG retrieval accuracy.
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks
