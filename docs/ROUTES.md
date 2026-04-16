# 路由設計文件 - 智慧食譜管理系統

本文件基於前面的 PRD、架構與資料庫設計，規劃 Flask 應用程式內所有的網址路由 (Routes) 結構以及對應的 Jinja2 頁面模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (食譜列表) | GET | `/` | `templates/index.html` | 顯示所有食譜，支援 `?category=xxx` 篩選 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/create.html` | 顯示填寫食譜（包含材料與步驟）的表單 |
| 建立食譜 | POST | `/recipes` | — | 儲存至資料庫並重導向 |
| 食譜詳情 | GET | `/recipes/<int:recipe_id>` | `templates/detail.html` | 顯示單一食譜的備料與烹飪步驟 |
| 編輯食譜頁面 | GET | `/recipes/<int:recipe_id>/edit` | `templates/edit.html` | 顯示舊有資料表單以供編輯 |
| 更新食譜 | POST | `/recipes/<int:recipe_id>/update` | — | 接收表單並更新資料庫內容 |
| 刪除食譜 | POST | `/recipes/<int:recipe_id>/delete` | — | 刪除該筆資料後重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 (食譜列表)
- **輸入**: URL Query Parameter `?category=` (可選)
- **處理邏輯**: 右有 `category`，則呼叫 `RecipeModel.get_all(category)`，否則呼叫 `RecipeModel.get_all()`
- **輸出**: 渲染 `index.html`，並將取得的 `recipes` 變數傳入。
- **錯誤處理**: 通常無錯誤，若無資料則前端顯示空視圖。

### 新增食譜頁面
- **輸入**: 無。
- **處理邏輯**: 單純回傳新增頁面的 View。
- **輸出**: 渲染 `create.html`。
- **錯誤處理**: 無。

### 建立食譜
- **輸入**: HTML Form Data (標題、時間、分類，以及多組食材文字、步驟文字、預覽圖與步驟圖)。
- **處理邏輯**: 
  1. 檢查並處裡上傳的圖檔，存至 `static/uploads/` 內。
  2. 整合所有資料，呼叫 `RecipeModel.create(...)` 存入 DB。
- **輸出**: 建立成功後，`redirect( url_for('index.home') )` 或是導向詳細頁。
- **錯誤處理**: 若有必填欄位空白或格式錯誤，重新退回並渲染 `create.html`。

### 食譜詳情
- **輸入**: URL 路徑上的 `recipe_id`
- **處理邏輯**: 呼叫 `RecipeModel.get_by_id(recipe_id)`。
- **輸出**: 渲染 `detail.html`，傳入食譜資料詳細。
- **錯誤處理**: 若回傳的資料不存在 (None)，則回應 404 可使用 `abort(404)` 並渲染 404 頁面。

### 編輯食譜頁面
- **輸入**: URL 路徑上的 `recipe_id`
- **處理邏輯**: 呼叫 `RecipeModel.get_by_id(recipe_id)` 取得資料，以便表單建立初期能顯示預設值。
- **輸出**: 渲染 `edit.html`。
- **錯誤處理**: 找不到對應的 `recipe_id` 回應 404。

### 更新食譜
- **輸入**: URL 參數 `recipe_id` 與新的 Form Data。
- **處理邏輯**: 呼叫 `RecipeModel.update(...)`
- **輸出**: 完成後 `redirect( url_for('recipe.detail', recipe_id=recipe_id) )`。
- **錯誤處理**: 必填檢查，錯誤時回傳 `edit.html` 帶上警告。

### 刪除食譜
- **輸入**: URL 參數 `recipe_id`
- **處理邏輯**: 呼叫 `RecipeModel.delete(recipe_id)`。
- **輸出**: 刪除完畢後 `redirect( url_for('index.home') )`。
- **錯誤處理**: 若沒找到或刪除權限有誤（目前無權限設計）可略過。

## 3. Jinja2 模板清單

將在 `app/templates/` 中建立以下檔案，皆繼承於統一的主版面：

1. **`base.html`**：主版面，包含共用的標題、導覽列 (Navbar) 以及引入靜態檔案 (style.css)。
2. **`index.html`**：首頁，以網格呈現食譜列表。
3. **`create.html`**：新增食譜表單頁面（需要使用 `enctype="multipart/form-data"` 支援圖片）。
4. **`detail.html`**：瀏覽單次食譜的頁面，包含份量材料表與分步圖文解說。
5. **`edit.html`**：修改舊有食譜用的表單。
6. **`404.html`**：找無食譜時的簡單錯誤訊息提示頁。

## 4. 路由骨架程式碼
請參考 `app/routes/` 目錄下的 Python 檔案，為了未來擴充與開發明確，我們採用 Flask 的 Blueprint 來實作。
