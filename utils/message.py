import sqlite3
import os


class Message:
    def __init__(
        self,
        id: str | None = None,
        sender_id: str | None = None,
        receiver_id: str | None = None,
        content: str | None = None,
        file_path: str | None = None,
        file_name: str | None = None,
        file_type: str | None = None,
        timestamp: str | None = None,
    ):
        self.id = id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.file_path = file_path
        self.file_name = file_name
        self.file_type = file_type
        self.timestamp = timestamp

    @classmethod
    def from_row(cls, row: tuple) -> "Message | None":
        """
        Create a Message instance from a database row.
        Assuming the row is a tuple with the following structure:

        (id, sender_id, receiver_id, content, file_path, file_name, file_type, timestamp)
        """
        if row is None or len(row) != 8:
            return None

        return cls(
            id=row[0],
            sender_id=row[1],
            receiver_id=row[2],
            content=row[3],
            file_path=row[4],
            file_name=row[5],
            file_type=row[6],
            timestamp=row[7],
        )

    @classmethod
    def from_id(cls, message_id: str) -> "Message | None":
        """
        Create a Message instance from a message ID.
        This method should be implemented to fetch the message details from the database.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
        row = cur.fetchone()

        conn.close()

        return cls.from_row(row) if row else None

    @classmethod
    def get_by_user(cls, user_id: str) -> list["Message"]:
        """
        Get all messages for a user.
        This method should be implemented to fetch the messages from the database.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM messages WHERE sender_id = ? OR receiver_id = ?",
            (user_id, user_id),
        )
        rows = cur.fetchall()

        conn.close()

        return (
            [msg for row in rows if (msg := cls.from_row(row)) is not None]
            if rows
            else []
        )

    def save(self):
        """
        Save the message instance to the database.
        This method should be implemented to insert or update the message in the database.
        """
        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        if self.id is None:
            # Insert new message
            cur.execute(
                "INSERT INTO messages (sender_id, receiver_id, content, file_path, file_name, file_type) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    self.sender_id,
                    self.receiver_id,
                    self.content,
                    self.file_path,
                    self.file_name,
                    self.file_type,
                ),
            )
            self.id = cur.lastrowid
        else:
            # Update existing message
            cur.execute(
                "UPDATE messages SET sender_id = ?, receiver_id = ?, content = ?, file_path = ?, file_name = ?, file_type = ? WHERE id = ?",
                (
                    self.sender_id,
                    self.receiver_id,
                    self.content,
                    self.file_path,
                    self.file_name,
                    self.file_type,
                    self.id,
                ),
            )

        conn.commit()
        conn.close()

    def validate(self) -> bool:
        """
        Validate the message instance.
        This method checks if the message data is valid.
        - sender_id and receiver_id must not be empty and must not be the same.
        - Either content or file_path must be present.
        """
        if not self.sender_id or not self.receiver_id:
            return False

        if self.sender_id == self.receiver_id:
            return False

        if not self.content and not self.file_path:
            return False

        return True

    def to_dict(self) -> dict:
        """
        Convert the message instance to a dictionary.
        This method should be implemented to return the message data as a dictionary.
        """
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "file_path": self.file_path,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "timestamp": self.timestamp,
        }

    def delete(self):
        """
        Delete the message instance from the database.
        If the message is a file attachment, also delete the file from the filesystem.
        """

        # Delete file if this message has a file attachment
        if self.file_path and os.path.isfile(self.file_path):
            try:
                os.remove(self.file_path)
            except Exception:
                pass  # Ignore errors when deleting the file

        conn = sqlite3.connect("chatapp.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM messages WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
