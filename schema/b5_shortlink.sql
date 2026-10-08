-- 🔗 shortlink schema
CREATE TABLE links(id INTEGER PRIMARY KEY, slug TEXT UNIQUE, url TEXT, password_hash TEXT, expires_at DATETIME, enabled INTEGER DEFAULT 1, created_at DATETIME);
CREATE TABLE clicks(id INTEGER PRIMARY KEY, link_id INTEGER REFERENCES links(id), ip TEXT, referrer TEXT, ua TEXT, at DATETIME);
