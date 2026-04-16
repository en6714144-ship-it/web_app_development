import sqlite3
from .db import get_db

class Tag:
    @staticmethod
    def create(name):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO tags (name) VALUES (?)", (name,))
            conn.commit()
            last_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # If tag already exists, retrieve its id
            cursor.execute("SELECT id FROM tags WHERE name = ?", (name,))
            row = cursor.fetchone()
            last_id = row['id']
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tags ORDER BY name ASC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def add_to_recipe(recipe_id, tag_id):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)",
                (recipe_id, tag_id)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            pass # Ignore if this relation already exists
        conn.close()
        
    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.* FROM tags t
            JOIN recipe_tags rt ON t.id = rt.tag_id
            WHERE rt.recipe_id = ?
        """, (recipe_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def clear_recipe_tags(recipe_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipe_tags WHERE recipe_id = ?", (recipe_id,))
        conn.commit()
        conn.close()
