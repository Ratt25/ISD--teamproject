-- LMS AI Copilot — SQLite Schema
-- (pgvector 없이 embedding은 TEXT로 저장, 나중에 PostgreSQL 전환 가능)

CREATE TABLE IF NOT EXISTS User (
    user_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    lms_id            TEXT    NOT NULL UNIQUE,
    enc_session_cookie TEXT,
    scraping_interval INTEGER DEFAULT 3600,
    last_sync_at      TEXT
);

CREATE TABLE IF NOT EXISTS Course (
    course_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    lms_url_id  TEXT UNIQUE,
    course_code TEXT,
    title       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Enrollment (
    enroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL REFERENCES User(user_id),
    course_id INTEGER NOT NULL REFERENCES Course(course_id),
    role      TEXT NOT NULL DEFAULT 'student',
    UNIQUE (user_id, course_id)
);

CREATE TABLE IF NOT EXISTS Material (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id   INTEGER NOT NULL REFERENCES Course(course_id),
    title       TEXT,
    file_type   TEXT,
    file_path   TEXT,
    checksum    TEXT,
    synced_at   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS Doc_Chunk (
    chunk_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL REFERENCES Material(material_id),
    content     TEXT NOT NULL,
    page_ref    INTEGER,
    chunk_index INTEGER,
    embedding   TEXT  -- JSON array, Phase 2에서 pgvector로 전환
);

CREATE TABLE IF NOT EXISTS Learning_Activity (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES User(user_id),
    course_id   INTEGER NOT NULL REFERENCES Course(course_id),
    title       TEXT,
    status      TEXT,
    due_date    TEXT
);

CREATE TABLE IF NOT EXISTS Personal_Log (
    log_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES User(user_id),
    course_id   INTEGER NOT NULL REFERENCES Course(course_id),
    material_id INTEGER REFERENCES Material(material_id),
    stay_time   INTEGER
);

CREATE TABLE IF NOT EXISTS Chat_Session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES User(user_id),
    course_id  INTEGER REFERENCES Course(course_id),
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS Chat_Log (
    chat_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id     INTEGER NOT NULL REFERENCES Chat_Session(session_id),
    role           TEXT NOT NULL,
    content        TEXT NOT NULL,
    sources        TEXT,  -- JSON
    feedback_score INTEGER,
    created_at     TEXT DEFAULT (datetime('now'))
);
