# 流程圖文件 - 智慧食譜管理系統

本文件根據產品需求文件 (PRD) 與系統架構文件 (ARCHITECTURE)，將系統的使用者操作路徑以及資料處理流程視覺化。

## 1. 使用者流程圖（User Flow）

此流程圖呈現從使用者進入網站開始，瀏覽食譜、新增食譜，到編輯與刪除等主要功能的操作路徑。

```mermaid
flowchart LR
    A([使用者造訪網站]) --> B[首頁 - 食譜列表]
    B --> C{選擇操作}
    
    C -->|點擊分類標籤| E[過濾後的食譜清單]
    E --> C
    
    C -->|點擊新增食譜| D[新增食譜頁面]
    D --> D1[填寫基本資訊與首圖]
    D1 --> D2[新增多筆材料與份量]
    D2 --> D3[新增烹飪步驟與對應圖片]
    D3 --> D4[送出儲存]
    D4 -->|成功| B
    
    C -->|點擊特定食譜| F[食譜詳細閱讀頁]
    F --> G{進階操作}
    G -->|瀏覽內容| H[閱讀備料與分步引導]
    G -->|編輯| I[編輯食譜頁面]
    I --> J[更新儲存]
    J -->|成功| F
    G -->|刪除| K[確認刪除]
    K -->|是| B
```

## 2. 系統序列圖（Sequence Diagram）

以下流程描述「使用者點擊新增食譜」直到「資料存入資料庫」的底層系統互動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as 模型 (Models)
    participant DB as SQLite

    User->>Browser: 填寫完整食譜表單與上傳圖片，點擊「儲存」
    Browser->>Flask: 發送 POST /create (包含欄位資料與圖檔)
    Flask->>Flask: 驗證資料並將圖片儲存到 static/uploads/
    Flask->>Model: 呼叫建立食譜的方法 (傳遞表單與圖片路徑)
    
    Model->>DB: 1. INSERT INTO recipes (寫入主食譜)
    Model->>DB: 2. INSERT INTO ingredients (寫入多筆材料)
    Model->>DB: 3. INSERT INTO steps (寫入多筆步驟)
    
    DB-->>Model: 交易 (Transaction) 寫入成功
    Model-->>Flask: 回傳建立成功的 Recipe ID
    Flask-->>Browser: HTTP 302 Redirect (重導向至首頁或詳細頁)
    Browser-->>User: 畫面重新載入，顯示最新的食譜
```

## 3. 功能清單對照表

根據上述流程，初步定義出食譜管理系統需要的 URL 路由與 HTTP 方法對照：

| 功能名稱 | 對應 URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **查看首頁** | `/` | GET | 顯示所有食譜卡片縮圖 |
| **依分類篩選** | `/?category=xxx` 或 `/category/<name>` | GET | 以分類標籤過濾食譜清單 |
| **顯示新增表單** | `/create` | GET | 載入用來填寫新食譜的網頁介面 |
| **送出新增食譜** | `/create` | POST | 接收表單並儲存至資料庫 |
| **查看食譜詳細** | `/recipe/<id>` | GET | 列出該篇食譜的所有食材與分步引導 |
| **顯示編輯表單** | `/recipe/<id>/edit` | GET | 載入並帶入舊資料以供編輯 |
| **送出編輯食譜** | `/recipe/<id>/edit` | POST | 更新該篇食譜資料庫的內容 |
| **刪除特定食譜** | `/recipe/<id>/delete` | POST | 執行刪除作業並回到首頁 |
