import os


class FileHandler:

    def save_uploaded_file(
        self,
        uploaded_file,
        upload_directory: str
    ) -> str:

        os.makedirs(
            upload_directory,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_directory,
            uploaded_file.name
        )

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )

        return file_path