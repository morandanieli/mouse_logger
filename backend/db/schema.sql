CREATE TABLE if not exists moves (
    x int,
    y int,
    timestamp real,
    session_id text,
    event_type text
);

CREATE TABLE if not exists keys (
    key text,
    keyCode int,
    timestamp real,
    session_id text,
    event_type text
);

CREATE TABLE if not exists images (
    session_id text primary key,
    path text
);