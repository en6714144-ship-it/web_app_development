from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import RecipeModel

# 建立名為 index 的 Blueprint
index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def home():
    """
    首頁路由：顯示所有食譜，支援依分類過濾。
    """
    category = request.args.get('category')
    recipes = RecipeModel.get_all(category)
    return render_template('index.html', recipes=recipes, current_category=category)
