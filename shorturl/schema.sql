DROP TABLE IF EXISTS urls_map;

CREATE TABLE urls_map (
	id INTEGER PRIMARY KEY,
   	short_url TEXT DEFAULT NULL,
	original_url TEXT DEFAULT NULL,
    created_at DATETIME DEFAULT (datetime('now', 'utc'))
);