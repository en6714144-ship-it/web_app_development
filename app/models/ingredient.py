from .db import get_db

class Ingredient:
    @staticmethod
    def create(recipe_id, name, quantity):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)",
            (recipe_id, name, quantity)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def delete_by_recipe(recipe_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        conn.commit()
        conn.close()
