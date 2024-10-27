import openai
from app.core import ports
from typing import List, cast, Union


class OpenAIAdapter(ports.LlmPort):
    def __init__(self, api_key: str, model: str, max_tokens: int, temperature: float):
        self._client = openai.OpenAI(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature

    def generate_text(self, prompt: str, retrieval_context: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"The context is: {retrieval_context}, "
                        "please respond to the following question:"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Asegura que MyPy sepa que `content` es str
        if response and response.choices and response.choices[0].message:
            return cast(str, response.choices[0].message.content)

        # Devolver un string vacío o lanzar un error si no hay contenido
        return ""

    def create_embeddings(self, text: str) -> Union[List[float], List]:
        try:
            response = self._client.embeddings.create(
                input=text, model="text-embedding-ada-002"
            )

            # Verificar que la respuesta tenga el formato esperado
            if response and hasattr(response, "data") and len(response.data) > 0:
                embedding_data = response.data[0]  # Obtenemos el primer elemento
                if hasattr(embedding_data, "embedding"):
                    embedding = embedding_data.embedding
                    if isinstance(embedding, list):
                        print(f"Embedding generado: {embedding}")
                        return embedding  # Retorna el embedding si es una lista
            # Si no hay embedding o no cumple con la estructura, lanzar un error o retornar lista vacía
            print("No se encontró un embedding válido.")
            return []
        except Exception as e:
            print(f"Error al generar el embedding: {e}")
            return []
