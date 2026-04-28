# 路由設計文件 (Routes Design)

本文件根據 PRD、系統架構、流程圖與資料庫設計，規劃任務管理系統的所有 Flask 路由、HTTP 方法與對應的 Jinja2 模板。

---

## 1. 路由總覽表格

### 1.1 頁面路由（瀏覽介面）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁（任務列表） | GET | `/` | `index.html` | 顯示所有任務列表，含今日提醒 |
| 月曆檢視 | GET | `/calendar` | `calendar.html` | 以月曆形式顯示任務分布 |

### 1.2 任務操作路由

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 新增任務頁面 | GET | `/tasks/new` | `task_form.html` | 顯示新增任務表單 |
| 建立任務 | POST | `/tasks` | — | 接收表單，存入 DB，重導向 `/` |
| 任務詳情 | GET | `/tasks/<id>` | `task_detail.html` | 顯示單筆任務完整資訊 |
| 編輯任務頁面 | GET | `/tasks/<id>/edit` | `task_form.html` | 顯示編輯表單（共用新增表單模板） |
| 更新任務 | POST | `/tasks/<id>/update` | — | 接收修改，更新 DB，重導向 `/` |
| 刪除任務 | POST | `/tasks/<id>/delete` | — | 刪除任務後重導向 `/` |
| 切換任務狀態 | POST | `/tasks/<id>/toggle` | — | 切換完成/未完成，重導向 `/` |

### 1.3 分類管理路由

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 分類列表 | GET | `/categories` | `categories.html` | 顯示所有分類，可新增/編輯/刪除 |
| 建立分類 | POST | `/categories` | — | 接收表單，新增分類，重導向 `/categories` |
| 刪除分類 | POST | `/categories/<id>/delete` | — | 刪除分類，重導向 `/categories` |

### 1.4 API 路由（前端 JS 用）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 查詢特定日期任務 | GET | `/api/tasks?date=YYYY-MM-DD` | — | 回傳 JSON，供月曆點擊日期時使用 |
| 查詢待提醒任務 | GET | `/api/reminders` | — | 回傳 JSON，供前端 JS 檢查提醒用 |

---

## 2. 每個路由的詳細說明

### 2.1 `GET /` — 首頁（任務列表）

- **輸入**：無（可選 query param `?category=<id>` 用於篩選）
- **處理邏輯**：
  1. 呼叫 `task.get_all()` 取得所有任務（或 `task.get_by_category()` 篩選）
  2. 呼叫 `category.get_all()` 取得分類列表（供篩選下拉選單用）
- **輸出**：渲染 `index.html`，傳入 `tasks` 與 `categories`
- **錯誤處理**：無特殊處理

### 2.2 `GET /calendar` — 月曆檢視

- **輸入**：可選 query param `?year=YYYY&month=MM`（預設為當月）
- **處理邏輯**：
  1. 解析年月參數，預設為當前年月
  2. 呼叫 `task.get_by_month(year, month)` 取得該月任務
  3. 組裝月曆資料結構（每日對應的任務列表）
- **輸出**：渲染 `calendar.html`，傳入月曆資料
- **錯誤處理**：年月格式不合法時使用預設值

### 2.3 `GET /tasks/new` — 新增任務頁面

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `category.get_all()` 取得分類選項
- **輸出**：渲染 `task_form.html`，傳入 `categories`，`task=None` 表示新增模式
- **錯誤處理**：無

### 2.4 `POST /tasks` — 建立任務

- **輸入**：表單欄位 — `title`(必填), `description`, `due_date`, `category_id`, `reminder_at`, `recurrence`
- **處理邏輯**：
  1. 驗證 `title` 不為空
  2. 呼叫 `task.create(...)` 寫入資料庫
- **輸出**：重導向至 `/`
- **錯誤處理**：`title` 為空時，重新渲染表單並顯示錯誤訊息（使用 `flash`）

### 2.5 `GET /tasks/<id>` — 任務詳情

- **輸入**：URL 參數 `id`（任務 ID）
- **處理邏輯**：
  1. 呼叫 `task.get_by_id(id)` 取得任務資料
- **輸出**：渲染 `task_detail.html`，傳入 `task`
- **錯誤處理**：找不到任務時回傳 404

### 2.6 `GET /tasks/<id>/edit` — 編輯任務頁面

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `task.get_by_id(id)` 取得現有任務資料
  2. 呼叫 `category.get_all()` 取得分類選項
- **輸出**：渲染 `task_form.html`，傳入 `task` 與 `categories`（編輯模式）
- **錯誤處理**：找不到任務時回傳 404

### 2.7 `POST /tasks/<id>/update` — 更新任務

- **輸入**：URL 參數 `id` + 表單欄位同 2.4
- **處理邏輯**：
  1. 驗證 `title` 不為空
  2. 呼叫 `task.update(id, ...)` 更新資料庫
- **輸出**：重導向至 `/`
- **錯誤處理**：`title` 為空時 flash 錯誤；找不到任務時回傳 404

### 2.8 `POST /tasks/<id>/delete` — 刪除任務

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `task.delete(id)` 從資料庫移除
- **輸出**：重導向至 `/`
- **錯誤處理**：找不到任務時回傳 404

### 2.9 `POST /tasks/<id>/toggle` — 切換任務狀態

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `task.toggle_status(id)` 切換 pending ↔ completed
- **輸出**：重導向至 `/`
- **錯誤處理**：找不到任務時回傳 404

### 2.10 `GET /categories` — 分類列表

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `category.get_all()` 取得所有分類
- **輸出**：渲染 `categories.html`，傳入 `categories`
- **錯誤處理**：無

### 2.11 `POST /categories` — 建立分類

- **輸入**：表單欄位 — `name`(必填)
- **處理邏輯**：
  1. 驗證 `name` 不為空且不重複
  2. 呼叫 `category.create(name)` 寫入資料庫
- **輸出**：重導向至 `/categories`
- **錯誤處理**：名稱為空或重複時 flash 錯誤

### 2.12 `POST /categories/<id>/delete` — 刪除分類

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `category.delete(id)` 從資料庫移除
- **輸出**：重導向至 `/categories`
- **錯誤處理**：找不到分類時回傳 404

### 2.13 `GET /api/tasks` — 查詢特定日期任務（JSON）

- **輸入**：query param `date=YYYY-MM-DD`
- **處理邏輯**：
  1. 呼叫 `task.get_by_date(date)` 查詢該日任務
- **輸出**：回傳 JSON `{ "tasks": [...] }`
- **錯誤處理**：缺少 `date` 參數時回傳 400

### 2.14 `GET /api/reminders` — 查詢待提醒任務（JSON）

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `task.get_pending_reminders()` 取得所有待提醒任務
- **輸出**：回傳 JSON `{ "reminders": [...] }`
- **錯誤處理**：無

---

## 3. Jinja2 模板清單

所有模板放在 `app/templates/` 目錄下，皆繼承 `base.html`。

| 模板檔案 | 繼承 | 說明 |
| :--- | :--- | :--- |
| `base.html` | — | 全局基礎版型：含導覽列、頁尾、CSS/JS 引入 |
| `index.html` | `base.html` | 首頁：任務列表看板，含篩選與新增按鈕 |
| `calendar.html` | `base.html` | 月曆檢視頁面，顯示當月任務分布 |
| `task_form.html` | `base.html` | 任務新增/編輯共用表單（依 `task` 是否存在區分模式） |
| `task_detail.html` | `base.html` | 單一任務詳細資訊頁面 |
| `categories.html` | `base.html` | 分類管理頁面：列表 + 新增表單 |

---

## 4. 路由骨架程式碼

路由骨架位於 `app/routes/` 目錄下：

| 檔案 | 說明 |
| :--- | :--- |
| `__init__.py` | Blueprint 匯入與註冊 |
| `pages.py` | 頁面路由（首頁、月曆） |
| `tasks.py` | 任務 CRUD 路由 |
| `categories.py` | 分類管理路由 |
| `api.py` | JSON API 路由（供前端 JS 使用） |
