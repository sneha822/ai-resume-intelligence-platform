from src.logger import logger
import os
from pypdf import PdfReader


def read_resume_file(file_path: str) -> str:
    extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
                
        elif extension == ".pdf":
            pdf = PdfReader(file_path)
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
            
        else:
            raise ValueError(f"Unsupported file type: {extension}")
            
    except Exception as error:
        logger.error(str(error))
        raise