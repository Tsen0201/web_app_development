-- ============================================
-- 任務管理系統 — SQLite Schema
-- ============================================
-- 執行方式：sqlite3 instance/database.db < database/schema.sql
-- ============================================

-- 分類表
CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 任務表
CREATE TABLE IF NOT EXISTS tasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    description  TEXT    DEFAULT '',
    status       TEXT    NOT NULL DEFAULT 'pending'
                         CHECK (status IN ('pending', 'completed')),
    due_date     TEXT,
    category_id  INTEGER,
    reminder_at  TEXT,
    recurrence   TEXT    DEFAULT 'none'
                         CHECK (recurrence IN ('none', 'daily', 'weekly', 'monthly')),
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),

    FOREIGN KEY (category_id) REFERENCES categories (id)
        ON DELETE SET NULL
);

-- 索引：加速依日期查詢（月曆功能）
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks (due_date);

-- 索引：加速依分類篩選
CREATE INDEX IF NOT EXISTS idx_tasks_category_id ON tasks (category_id);

-- 索引：加速依狀態篩選
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks (status);

-- ============================================
-- 預設分類（種子資料）
-- ============================================
INSERT OR IGNORE INTO categories (name) VALUES ('工作');
INSERT OR IGNORE INTO categories (name) VALUES ('日常');
INSERT OR IGNORE INTO categories (name) VALUES ('休閒');
