import sqlite3
import os

# 自動定位 instance 資料夾下的 database.db
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'database.db')

def get_db_connection():
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 讓 SELECT 回傳的資料可以用 dict 的方式取值
    conn.row_factory = sqlite3.Row
    return conn

class RecipeModel:
    @staticmethod
    def create(title, image_path, prep_time, category, ingredients_data, steps_data):
        """
        新增食譜與其對應的材料、步驟
        ingredients_data: [{'name': '...', 'amount': '...'}, ...]
        steps_data: [{'step_number': 1, 'description': '...', 'image_path': '...'}, ...]
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 1. 寫入 recipes 表格
            cursor.execute('''
                INSERT INTO recipes (title, image_path, prep_time, category)
                VALUES (?, ?, ?, ?)
            ''', (title, image_path, prep_time, category))
            
            recipe_id = cursor.lastrowid
            
            # 2. 寫入 ingredients 表格
            for ing in ingredients_data:
                cursor.execute('''
                    INSERT INTO ingredients (recipe_id, name, amount)
                    VALUES (?, ?, ?)
                ''', (recipe_id, ing['name'], ing['amount']))
                
            # 3. 寫入 steps 表格
            for step in steps_data:
                cursor.execute('''
                    INSERT INTO steps (recipe_id, step_number, description, image_path)
                    VALUES (?, ?, ?, ?)
                ''', (recipe_id, step['step_number'], step['description'], step.get('image_path')))
                
            conn.commit()
            return recipe_id
        except Exception as e:
            conn.rollback() # 發生錯誤則還原交易
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all(category=None):
        """取得所有食譜，支援以分類標籤篩選"""
        conn = get_db_connection()
        if category:
            recipes = conn.execute('SELECT * FROM recipes WHERE category = ? ORDER BY created_at DESC', (category,)).fetchall()
        else:
            recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        """根據 ID 取得單一食譜及其材料與步驟"""
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        if not recipe:
            conn.close()
            return None
            
        ingredients = conn.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
        steps = conn.execute('SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_number ASC', (recipe_id,)).fetchall()
        conn.close()
        
        result = dict(recipe)
        result['ingredients'] = [dict(i) for i in ingredients]
        result['steps'] = [dict(s) for s in steps]
        return result

    @staticmethod
    def update(recipe_id, title, image_path, prep_time, category):
        """更新食譜基本資訊"""
        conn = get_db_connection()
        conn.execute('''
            UPDATE recipes
            SET title = ?, image_path = ?, prep_time = ?, category = ?
            WHERE id = ?
        ''', (title, image_path, prep_time, category, recipe_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        """刪除食譜（關聯的材料與步驟將會因為 ON DELETE CASCADE 自動被刪除）"""
        conn = get_db_connection()
        # 需開啟 foreign_keys 支持 CASCADE 刪除
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()
