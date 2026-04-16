from .db import get_db

class Recipe:
    @staticmethod
    def create(title, description, instructions):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO recipes (title, description, instructions) VALUES (?, ?, ?)",
            (title, description, instructions)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(recipe_id, title, description, instructions):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE recipes SET title = ?, description = ?, instructions = ? WHERE id = ?",
            (title, description, instructions, recipe_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()
