import sqlite3


class CandidateDatabase:

    def __init__(
        self, 
        database_path: str
    ) -> None:
        """Initializes the database handler with a target file path."""
        self.database_path = database_path

    def create_connection(self) -> sqlite3.Connection:
        """Creates and returns a live connection object to the SQLite database."""
        return sqlite3.connect(self.database_path)

    def create_table(self) -> None:
        """Creates the candidates table with a UNIQUE constraint on the email field."""
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                phone TEXT,
                skills TEXT
            )
            """
        )

        connection.commit()
        connection.close()

    def insert_candidate(
        self, 
        email: str, 
        phone: str, 
        skills: str
    ) -> None:
        """
        Safely inserts a new candidate record using parameterized queries.
        Handles duplicate email conflicts gracefully without crashing the app.
        """
        connection = self.create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO candidates (
                    email, 
                    phone, 
                    skills
                ) 
                VALUES (?, ?, ?)
                """,
                (email, phone, skills)
            )
            connection.commit()
            print("Candidate inserted successfully")
            
        except sqlite3.IntegrityError:
            print(
                f"Candidate with email "
                f"'{email}' already exists."
            )
            
        finally:
            connection.close()

    def fetch_all_candidates(self) -> list:
        """Retrieves and returns all candidate records from the database table."""
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM candidates"
        )
        records = cursor.fetchall()
        
        connection.close()
        return records

    def update_phone(
        self, 
        email: str, 
        new_phone: str
    ) -> None:
        """Updates the phone number for a candidate based on their unique email address."""
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE candidates 
            SET phone = ? 
            WHERE email = ?
            """,
            (new_phone, email)
        )

        connection.commit()
        connection.close()

    def delete_candidate(
        self, 
        email: str
    ) -> None:
        """Removes a candidate record entirely from the database table via email lookups."""
        connection = self.create_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM candidates 
            WHERE email = ?
            """,
            (email,)
        )

        connection.commit()
        connection.close()