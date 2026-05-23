import re


def clean_text(text):
    """
    Cleans extra spaces and blank lines from text.
    """
    if not text:
        return ""

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            cleaned_lines.append(stripped_line)

    return "\n".join(cleaned_lines)


def chunk_text(text, chunk_size=900, overlap=150):
    """
    Splits long text into overlapping chunks.

    chunk_size:
    Approximate number of characters in each chunk.

    overlap:
    Number of characters repeated from previous chunk.
    This helps preserve context between chunks.
    """
    cleaned_text = clean_text(text)

    if not cleaned_text:
        return []

    chunks = []
    start = 0
    text_length = len(cleaned_text)

    while start < text_length:
        end = start + chunk_size
        chunk = cleaned_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

        if start >= text_length:
            break

    return chunks


def create_document_chunks(resume_text, jd_text):
    """
    Creates labeled chunks for resume and job description.
    Labels help the assistant know where the chunk came from.
    """
    document_chunks = []

    resume_chunks = chunk_text(resume_text)
    jd_chunks = chunk_text(jd_text)

    for index, chunk in enumerate(resume_chunks, start=1):
        document_chunks.append({
            "source": "resume",
            "chunk_id": f"resume_chunk_{index}",
            "text": chunk
        })

    for index, chunk in enumerate(jd_chunks, start=1):
        document_chunks.append({
            "source": "job_description",
            "chunk_id": f"jd_chunk_{index}",
            "text": chunk
        })

    return document_chunks


def tokenize_text(text):
    """
    Converts text into simple searchable words.
    This is a basic retrieval method before real vector search.
    """
    text = text.lower()
    words = re.findall(r"\b[a-zA-Z0-9+#.]+\b", text)

    stopwords = {
        "the", "and", "or", "a", "an", "to", "of", "in", "for", "with",
        "on", "by", "is", "are", "was", "were", "be", "as", "at", "from",
        "this", "that", "it", "your", "you", "we", "our", "their", "has",
        "have", "had", "using", "use", "can", "will", "should"
    }

    useful_words = []

    for word in words:
        if word not in stopwords and len(word) > 1:
            useful_words.append(word)

    return useful_words


def score_chunk(query_words, chunk_text_value):
    """
    Scores one chunk based on keyword overlap with the user question.
    """
    chunk_words = tokenize_text(chunk_text_value)
    chunk_word_set = set(chunk_words)

    score = 0

    for word in query_words:
        if word in chunk_word_set:
            score += 1

    return score


def retrieve_relevant_chunks(question, document_chunks, top_k=4):
    """
    Retrieves the most relevant resume/JD chunks for a user question.

    This is not real vector search yet.
    It is basic keyword-based retrieval.
    Later, we will replace/upgrade it with embeddings + vector DB.
    """
    if not question or not document_chunks:
        return []

    query_words = tokenize_text(question)

    scored_chunks = []

    for chunk in document_chunks:
        score = score_chunk(query_words, chunk["text"])

        if score > 0:
            scored_chunks.append({
                "score": score,
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"]
            })

    scored_chunks.sort(key=lambda item: item["score"], reverse=True)

    return scored_chunks[:top_k]


def format_retrieved_chunks(retrieved_chunks):
    """
    Converts retrieved chunks into readable context for the AI prompt.
    """
    if not retrieved_chunks:
        return "No highly relevant chunks found."

    formatted_text = ""

    for item in retrieved_chunks:
        formatted_text += f"\nSource: {item['source']} | Chunk: {item['chunk_id']} | Score: {item['score']}\n"
        formatted_text += item["text"]
        formatted_text += "\n---\n"

    return formatted_text.strip()