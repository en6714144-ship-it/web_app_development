import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from werkzeug.utils import secure_filename
from app.models.recipe import RecipeModel

# 建立名為 recipe 的 Blueprint，並加上預設的 /recipes 前綴
recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

def save_uploaded_file(file_obj):
    """輔助函式：安全地儲存上傳的檔案，回傳檔案名稱"""
    if file_obj and file_obj.filename != '':
        filename = secure_filename(file_obj.filename)
        # 上傳路徑設定在 current_app.config['UPLOAD_FOLDER']
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file_obj.save(upload_path)
        return filename
    return None

@recipe_bp.route('/new', methods=['GET'])
def create_page():
    """新增食譜頁面路由。"""
    return render_template('create.html')

@recipe_bp.route('', methods=['POST'])
def create_submit():
    """新增食譜提交路由。"""
    # 取得基本欄位
    title = request.form.get('title')
    prep_time = request.form.get('prep_time')
    category = request.form.get('category')
    
    # 必填驗證
    if not title or not prep_time or not category:
        flash("請填寫所有必填標籤與時間", "danger")
        return redirect(url_for('recipe.create_page'))
        
    # 建立食譜首圖
    main_image = request.files.get('image')
    image_path = save_uploaded_file(main_image)
    
    # 解析並建立動態的多筆食材清單
    ingredients_names = request.form.getlist('ingredient_name[]')
    ingredients_amounts = request.form.getlist('ingredient_amount[]')
    ingredients_data = []
    for name, amt in zip(ingredients_names, ingredients_amounts):
        if name.strip() and amt.strip():
            ingredients_data.append({'name': name.strip(), 'amount': amt.strip()})
            
    # 解析並建立動態的多筆步驟清單
    step_descriptions = request.form.getlist('step_description[]')
    step_images = request.files.getlist('step_image[]')
    
    steps_data = []
    for i, desc in enumerate(step_descriptions):
        if desc.strip():
            # 安全取對應的步驟圖片
            step_img_file = step_images[i] if i < len(step_images) else None
            step_img_path = save_uploaded_file(step_img_file)
            steps_data.append({
                'step_number': i + 1,
                'description': desc.strip(),
                'image_path': step_img_path
            })
            
    try:
        recipe_id = RecipeModel.create(
            title=title,
            image_path=image_path,
            prep_time=prep_time,
            category=category,
            ingredients_data=ingredients_data,
            steps_data=steps_data
        )
        flash("食譜新增成功！", "success")
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))
    except Exception as e:
        flash(f"資料儲存失敗：{str(e)}", "danger")
        return redirect(url_for('recipe.create_page'))

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """檢視食譜詳細內容路由。"""
    recipe = RecipeModel.get_by_id(recipe_id)
    if not recipe:
        abort(404)
    return render_template('detail.html', recipe=recipe)

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET'])
def edit_page(recipe_id):
    """編輯食譜頁面路由。"""
    recipe = RecipeModel.get_by_id(recipe_id)
    if not recipe:
        abort(404)
    return render_template('edit.html', recipe=recipe)

@recipe_bp.route('/<int:recipe_id>/update', methods=['POST'])
def edit_submit(recipe_id):
    """更新食譜提交路由。"""
    title = request.form.get('title')
    prep_time = request.form.get('prep_time')
    category = request.form.get('category')
    
    if not title or not prep_time or not category:
        flash("請填寫所有必填欄位", "danger")
        return redirect(url_for('recipe.edit_page', recipe_id=recipe_id))
        
    main_image = request.files.get('image')
    image_path = save_uploaded_file(main_image)
    
    if not image_path:
        old_recipe = RecipeModel.get_by_id(recipe_id)
        image_path = old_recipe.get('image_path')
        
    try:
        RecipeModel.update(recipe_id, title, image_path, prep_time, category)
        flash("食譜基本資訊更新成功！", "success")
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))
    except Exception as e:
        flash(f"更新失敗：{str(e)}", "danger")
        return redirect(url_for('recipe.edit_page', recipe_id=recipe_id))

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_submit(recipe_id):
    """刪除食譜提交路由。"""
    try:
        RecipeModel.delete(recipe_id)
        flash("食譜已刪除！", "success")
    except Exception as e:
        flash("刪除失敗", "danger")
    return redirect(url_for('index.home'))
