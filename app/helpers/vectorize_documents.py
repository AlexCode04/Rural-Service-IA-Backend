from app.core import ports
import tiktoken


def get_openai_embeddings(text: str, openai_client: ports.LlmPort) -> list[float]:
    response = openai_client.create_embeddings(text)
    print(f"Embeddings generados: {response}")
    return response


# Divide el contenido en fragmentos y luego convierte cada uno en un vector de embeddings
def document_to_vectors(
    content: str, openai_client: ports.LlmPort
) -> list[list[float]]:
    chunks = chunk_text(content, max_tokens=2048)
    print(f"Chunks generated: {chunks}")
    con_vec = [get_openai_embeddings(chunk, openai_client) for chunk in chunks]
    return con_vec  # Lista de listas de embeddings


# Divide el texto en fragmentos, respetando un máximo de tokens
def chunk_text(text: str, max_tokens: int) -> list[str]:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    # Divide los tokens en chunks de tamaño max_tokens
    chunks = [tokens[i : i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    chunk_texts = [tokenizer.decode(chunk) for chunk in chunks]
    return chunk_texts
