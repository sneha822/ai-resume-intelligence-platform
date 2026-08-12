import os
from pypdf import PdfReader
from src.logger import logger


def read_resume_file(file_path: str) -> str:
    """Reads content from text (.txt) and PDF (.pdf) files safely."""
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
                    text += page_text + "\n"
            return text
            
        else:
            raise ValueError(f"Unsupported file type: {extension}")
            
    except Exception as error:
        logger.error(f"Error reading file {file_path}: {str(error)}")
        raise error


# Alias for backward compatibility with early test scripts
def read_text_file(file_path: str) -> str:
    """Reads text from a file (calls read_resume_file)."""
    return read_resume_file(file_path)