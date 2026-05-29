from src.logger import logger


def read_text_file(file_path: str):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        logger.info(
            f"Successfully read file: {file_path}"
        )

        return text

    except FileNotFoundError:

        logger.error(
            f"File not found: {file_path}"
        )

    except Exception as error:

        logger.error(
            f"Unexpected error: {error}"
        )

    return ""