import sqlite3


class Friendship:
    def __init__(
        self,
        id: str | None = None,
        user1_id: str | None = None,
        user2_id: str | None = None,
        status: str | None = None,
        created_at: str | None = None,
    ):
        self.id = id
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.status = status
        self.created_at = created_at

    @classmethod
    def from_row(cls, row: tuple) -> "Friendship | None":
        """
        Create a Friendship instance from a database row.
        Assuming the row is a tuple with the following structure:

        (id, user1_id, user2_id, status, created_at)
        """
        if row is None or len(row) != 5:
            return None

        return cls(
            id=row[0],
            user1_id=row[1],
            user2_id=row[2],
            status=row[3],
            created_at=row[4],
        )

    @classmethod
    def from_id(cls, friendship_id: str) -> "Friendship | None":
        """
        Create a Friendship instance from a friendship ID.
        This method should be implemented to fetch the friendship details from the database.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM friendships WHERE id = ?", (friendship_id,))
        row = cur.fetchone()

        conn.close()

        return cls.from_row(row) if row else None

    @classmethod
    def from_user_ids(cls, user1_id: str, user2_id: str) -> "Friendship | None":
        """
        Create a Friendship instance from two user IDs.
        This method should be implemented to fetch the friendship details from the database.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM friendships WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)",
            (user1_id, user2_id, user2_id, user1_id),
        )
        row = cur.fetchone()

        conn.close()

        return cls.from_row(row) if row else None

    @classmethod
    def get(cls, user_id: str) -> list["Friendship"]:
        """
        Mengembalikan daftar pertemanan untuk pengguna tertentu.
        Mengambil semua pertemanan yang melibatkan pengguna dengan ID yang diberikan.
        Mengembalikan pertemanan dengan status 'accepted' atau 'pending'.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM friendships WHERE (user1_id = ? OR user2_id = ?) AND status IN ('accepted', 'pending')",
            (user_id, user_id),
        )
        rows = cur.fetchall()

        conn.close()

        return (
            [
                friendship
                for row in rows
                if row and (friendship := cls.from_row(row)) is not None
            ]
            if rows
            else []
        )

    def save(self) -> None:
        """
        Save the friendship instance to the database.
        If the friendship already exists, update it. Otherwise, insert a new record.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        if self.id is None:
            cur.execute(
                "INSERT INTO friendships (user1_id, user2_id, status) VALUES (?, ?, ?)",
                (self.user1_id, self.user2_id, self.status),
            )
            self.id = cur.lastrowid
        else:
            cur.execute(
                "UPDATE friendships SET status = ? WHERE id = ?",
                (self.status, self.id),
            )

        conn.commit()
        conn.close()

    def delete(self) -> None:
        """
        Delete the friendship instance from the database.
        """
        if self.id is None:
            return

        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM friendships WHERE id = ?", (self.id,))

        conn.commit()
        conn.close()
