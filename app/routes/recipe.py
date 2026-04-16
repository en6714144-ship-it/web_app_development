from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
# from app.models.recipe import RecipeModel

# 建立名為 recipe 的 Blueprint，並加上預設的 /recipes 前綴
recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/new', methods=['GET'])
def create_page():
    """
    新增食譜頁面路由。
    輸入：無
    處理邏輯：準備渲染新增頁面。
    輸出：渲染 templates/create.html
    """
    pass

@recipe_bp.route('', methods=['POST'])
def create_submit():
    """
    新增食譜提交路由。
    輸入：Form Data (title, prep_time, category, ingredients, steps, files)
    處理邏輯：驗證欄位、處理圖片上傳，並寫入資料庫。
    輸出：重導向至首頁或該食譜的詳細頁面。
    """
    pass

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """
    檢視食譜詳細內容路由。
    輸入：URL路徑中的 recipe_id
    處理邏輯：向 Model 查詢該筆食譜的所有細節與對應食材/步驟。若無此 ID，回傳 404。
    輸出：渲染 templates/detail.html
    """
    pass

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET'])
def edit_page(recipe_id):
    """
    編輯食譜頁面路由。
    輸入：URL路徑中的 recipe_id
    處理邏輯：取得舊有資料，若無資料回傳 404。
    輸出：渲染 templates/edit.html
    """
    pass

@recipe_bp.route('/<int:recipe_id>/update', methods=['POST'])
def edit_submit(recipe_id):
    """
    更新食譜提交路由。
    輸入：URL路徑中的 recipe_id 與 Form Data
    處理邏輯：驗證資料並呼叫 Model 執行更新。
    輸出：重導向至該篇食譜的詳細頁面 ( /recipes/<id> )。
    """
    pass

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_submit(recipe_id):
    """
    刪除食譜提交路由。
    輸入：URL路徑中的 recipe_id
    處理邏輯：呼叫 Model 將該筆食譜包含食材與步驟一併刪除。
    輸出：重導向至首頁。
    """
    pass
