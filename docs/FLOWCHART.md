# 系統流程圖與使用者操作路徑 (Flowchart & Sequence)

本文件根據 PRD (任務管理系統) 與系統架構文件所繪製，用於視覺化展現系統的使用者操作動線與後端資料處理流程。

## 1. 使用者流程圖 (User Flow)

描述使用者進入任務管理系統後，可以進行的各種操作與頁面跳轉邏輯。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Index[首頁 - 任務列表看板]
    
    Index --> Action{接著想做什麼？}
    
    %% 新增任務線
    Action -->|新增任務| AddTask[點擊「新增」]
    AddTask --> FillForm[填寫標題、日期、選擇分類]
    FillForm --> SubmitAdd[送出表單]
    SubmitAdd --> Index
    
    %% 管理任務線
    Action -->|管理現有任務| SelectTask[選擇某個任務]
    SelectTask --> TaskAction{對任務的操作}
    
    TaskAction -->|查看細節| ViewTask[展開/跳轉至詳細資訊]
    ViewTask --> Index
    
    TaskAction -->|修改內容| EditForm[變更標題或時間]
    EditForm --> SubmitEdit[儲存修改]
    SubmitEdit --> Index
    
    TaskAction -->|勾選狀態| ToggleStatus[標記為「已完成」或「未完成」]
    ToggleStatus --> Index
    
    TaskAction -->|刪除| DeleteConfirm{確認刪除？}
    DeleteConfirm -->|是| SubmitDelete[任務被移除]
    SubmitDelete --> Index
    DeleteConfirm -->|否| Index
    
    %% 月曆線
    Action -->|整體排程檢視| ViewCalendar[切換至「本月月曆」視圖]
    ViewCalendar --> FilterTime[點擊不同月份或日期]
    FilterTime --> ShowDayTasks[列出該日期的代辦事項]
    ShowDayTasks --> Index
```

## 2. 系統序列圖 (Sequence Diagram)

此圖描述當使用者欲「新增一個新任務」時，系統從前端至後端、乃至資料庫的完整互動經過。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML)
    participant Route as Flask Route (Controller)
    participant Model as 任務 Model (處理資料)
    participant DB as SQLite
    
    User->>Browser: 填寫「新增任務」表單並送出
    Browser->>Route: 發送 POST /task 請求 (含表單內容)
    
    rect rgb(245, 245, 255)
        Note over Route, DB: 後端資料處理階段
        Route->>Route: 驗證格式是否正確 (如：標題不可空)
        Route->>Model: 呼叫建立任務函數 
        Model->>DB: 執行 INSERT INTO tasks...
        DB-->>Model: 回傳成功指令
        Model-->>Route: 任務物件建立完成
    end
    
    Route-->>Browser: HTTP 302 重導向回首頁 (/)
    
    Browser->>Route: 發送 GET / 請求重新載入
    Route->>Model: 查詢全部任務
    Model->>DB: 執行 SELECT * FROM tasks
    DB-->>Model: 回傳全部資料
    Model-->>Route: 打包為 Python 字典 / 陣列
    Route-->>Browser: 結合 Jinja2 渲染 HTML 回傳給瀏覽器
    Browser-->>User: 顯示已包含新一筆任務的最新畫面
```

## 3. 功能清單與路徑對照表

這是未來開發路由時的對照清單，用來指引每個功能分別由哪個網址和 HTTP Method 來處理。

| 功能區塊 | 操作行為 | 網址路徑 (URL Context) | HTTP Method | 對應的動作與頁面 |
| :--- | :--- | :--- | :--- | :--- |
| **瀏覽介面** | **查看首頁任務列表** | `/` | `GET` | 渲染 `index.html`。回傳預設/當日列出的任務 |
| **瀏覽介面** | **查看月曆視圖** | `/calendar` | `GET` | 渲染 `calendar.html`。回傳月曆所需的結構與資料 |
| **任務操作** | **新增任務** | `/task` | `POST` | 寫入資料庫，完成後重導回 `/` |
| **任務操作** | **更新任務內容** | `/task/<test_id>` | `POST` *(或 PUT)* | 寫入變更至指定任務，完成重導回原處 |
| **任務操作** | **刪除任務** | `/task/<task_id>/delete`| `POST` | 從資料庫移除指定任務，重導回 `/` |
| **任務操作** | **切換任務狀態** | `/task/<task_id>/toggle`| `POST` | 將指定任務設為完成或未完成，重導回 `/`|
| **進階輔助** | *(若需用前端 JS 抓單日資料)*| `/api/tasks` | `GET` | 回傳特定日期的 JSON 格式，搭配 URL 參數 `?date=YYYY-MM-DD` |
