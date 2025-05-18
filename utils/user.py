import sqlite3
import bcrypt


class User:
    def __init__(
        self,
        id: str | None = None,
        email: str | None = None,
        password: str | None = None,
        name: str | None = None,
        profile_picture: str | None = None,
        created_at: str | None = None,
    ):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.profile_picture = profile_picture
        self.created_at = created_at

    @classmethod
    def from_row(cls, row: tuple) -> "User | None":
        """
        Create a User instance from a database row.
        Assuming the row is a tuple with the following structure:

        (id, email, password, name, profile_picture, created_at)
        """
        if row is None or len(row) != 6:
            return None

        return cls(
            id=row[0],
            email=row[1],
            password=row[2],
            name=row[3],
            profile_picture=row[4],
            created_at=row[5],
        )

    @classmethod
    def from_id(cls, user_id: str) -> "User | None":
        """
        Create a User instance from a user ID.
        This method should be implemented to fetch the user details from the database.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()

        conn.close()

        return cls.from_row(row) if row else None

    @classmethod
    def get_all_except(cls, user_id: str) -> list["User"]:
        """
        Get all users except the current user.
        This method should be implemented to fetch all users from the database.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE id != ?", (user_id,))
        rows = cur.fetchall()

        conn.close()

        return (
            [user for row in rows if (user := cls.from_row(row)) is not None]
            if rows
            else []
        )

    def save(self):
        """
        - Save the user instance to the database.
        - Assumes self.password is already hashed.
        - If the user has an ID, update the existing record.
        - If the user does not have an ID, insert a new record.
        """

        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        if self.id:
            # Update existing user
            cur.execute(
                "UPDATE users SET email = ?, password = ?, name = ?, profile_picture = ? WHERE id = ?",
                (self.email, self.password, self.name, self.profile_picture, self.id),
            )
        else:
            # Insert new user
            cur.execute(
                "INSERT INTO users (email, password, name, profile_picture) VALUES (?, ?, ?, ?)",
                (self.email, self.password, self.name, self.profile_picture),
            )
            self.id = str(cur.lastrowid)

        conn.commit()
        conn.close()

    def to_dict(self) -> dict:
        """
        Convert the user instance to a dictionary.
        """
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at,
        }
