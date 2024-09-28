import os
from fastapi import UploadFile
from app.core.models import Document, User
from app.core import ports
from app.helpers.strategies_poc import FileReader



class RAGService:
    def __init__(self, db: ports.DatabasePort) -> None:
        self.db = db

    def save_document(self, file: UploadFile) -> None:
        # Obtener el nombre del archivo
        file_name = file.filename

        # Crear la carpeta 'media' si no existe
        os.makedirs('media', exist_ok=True)

        # Guardar el archivo en la carpeta 'media'
        file_path = os.path.join('media', file_name)
        with open(file_path, 'wb') as f:
            f.write(file.file.read())

        #Crear modelo ducumento con valores iniciales
        document = Document(nombre=file_name, ruta=file_path)
        #Obtengo el contenido del documento
        content = FileReader(document.ruta).read_file()
        print(content)

        #Guardar información del documento en MongoDB
        self.db.save_document(document)

    def get_document(self, document_id: str) -> Document:
        return self.db.get_document(document_id)





