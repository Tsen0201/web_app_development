# 系統架構設計 (Architecture Design)

## 1. 技術架構說明

根據 PRD (任務管理系統) 的需求，考量專案為個人使用工具，開發上應重視「快速實作、輕量、易維護」。

- **後端框架**：**Python + Flask**
  - **原因**：Flask 是輕量彈性的後端框架，無論是寫 API 還是整合渲染畫面都很方便，非常適合中小型與個人專案。
- **模板引擎**：**Jinja2**
  - **原因**：由 Flask 內建支援，負責在後端合成 HTML 頁面再傳給瀏覽器。這樣**不需要前後端分離**，能大幅度降低系統複雜度與開發時間。
- **資料庫**：**SQLite**
  - **原因**：SQLite 是一套無須另外架設伺服器的微型資料庫，資料庫就是一個本地的`.db`檔案。對單人存取情境綽綽有餘，而且備份極其容易。

### Flask MVC 模式說明
因為不需要前後端分離，我們會在 Flask 裡採用經典的 MVC（Model-View-Controller）模式：

- **Model (資料模型)**：負責定義資料儲存格式（例如：任務要在資料庫裡的樣貌）並負責與資料庫（SQLite）連線、讀寫資料。
- **View (視圖/畫面)**：就是負責產生給使用者看的網頁介面。藉由 **Jinja2 模板引擎** 把 Model 抓出來的資料填進 HTML 中，最終顯示在瀏覽器。
- **Controller (控制器)**：在 Flask 裡負責這個角色的是**路由 (Routes)**。它負責接住從瀏覽器發送來的網址請求 (Request)，決定叫喚哪個 Model 拿資料，然後再把資料丟給哪個 View 產生畫面並回傳。

---

## 2. 專案資料夾結構

整個專案將按照職責進行分類放置。以下為建議的資料夾結構樹狀圖：

```text
web_app_development/
├── app/                  # 應用程式主資料夾
│   ├── __init__.py       # 初始化 Flask 應用程式、綁定資料庫設定
│   ├── models/           # 資料庫模型 (Model) 控制對資料的存取
│   │   ├── __init__.py
│   │   └── schema.py     # 定義任務 (Task)、分類 (Category) 資料表結構
│   ├── routes/           # Flask 路由 (Controller)，處理邏輯
│   │   ├── __init__.py
│   │   └── pages.py      # 主要介面的網址路由處理
│   ├── templates/        # Jinja2 HTML 模板 (View)
│   │   ├── base.html     # 全局共同版型 (如導覽列)
│   │   ├── index.html    # 首頁 / 任務清單列表
│   │   └── calendar.html # 月曆檢視畫面
│   └── static/           # CSS、JavaScript 等靜態資源
│       ├── css/style.css # 全站樣式
│       └── js/main.js    # 用來幫助提醒通知或處理月曆點擊的程式
├── instance/             # 不加入版本控制的資料 (放主機本地檔案)
│   └── database.db       # SQLite 資料庫實體檔案
├── docs/                 # 系統設計相關文件
│   ├── PRD.md            # 產品需求文件
│   └── ARCHITECTURE.md   # 系統架構文件 (本文件)
├── app.py                # 整個專案啟動時的主入口
└── requirements.txt      # 記錄用到了哪些 Python 套件 (如 Flask, SQLAlchemy)
```

---

## 3. 元件關係圖

以下展示瀏覽器跟我們 Flask 系統之間是如何對話與傳遞資料的：

```mermaid
flowchart TD
    Browser((瀏覽器))

    subgraph 後端應用伺服器 (Flask)
        Route[Flask Route (Controller)]
        Template[Jinja2 Template (View)]
        Model[Model (資料模型)]
    end

    DB[(SQLite 資料庫)]

    %% HTTP Request
    Browser -- "1. HTTP Request (例如：看月曆)" --> Route
    
    %% DB Query
    Route -- "2. 詢問需要顯示的資料" --> Model
    Model -- "3. 執行 SQL 查詢" --> DB
    DB -- "4. 回傳任務資料" --> Model
    Model -- "5. 將資料整理為 Python 物件" --> Route
    
    %% Render HTML
    Route -- "6. 傳遞資料以供渲染" --> Template
    Template -- "7. 幫忙組合出完整的 HTML" --> Route
    
    %% HTTP Response
    Route -- "8. HTTP Response (最終網頁)" --> Browser
```

---

## 4. 關鍵設計決策

1. **捨棄前後端分離架構**
   - **原因**：雖然目前流行 React + 獨立 API 的做法，但在沒有強烈元件復用需求、以「單人使用工具」為主要取向時，讓 Flask 直接處理「資料 + HTML畫面 (SSR)」是最務實、成本最低且好維護的方式。
2. **採用微型資料庫 SQLite**
   - **原因**：免安裝、免設定，資料庫只是電腦裡的一個小檔案。針對沒有大規模連線併發挑戰的個人工具，這能大幅降低部署管理與主機費用的門檻。
3. **藉由輕量 JavaScript 輔助增強介面功能 (提醒 / 月曆切換)**
   - **原因**：為了在非前後端分離的系統內達到「跳出時間提醒通知」的需求，會在網頁中適量加入前端 JavaScript (`static/js/main.js`) 掛載計時器檢查或是輔助日曆格子的直接互動，在簡單架構下盡量提昇「好用程度」。
4. **使用 MVC 模式分類資料夾**
   - **原因**：沒有把所有程式碼塞進一兩個巨型 Python 檔案裡，而是按照 `models`, `routes`, `templates` 劃分清楚。這可以避免專案成長後程式碼變「義大利麵條（難以閱讀）」，在未來加入「週期性重複任務」等進階功能時更容易找到切入點。
