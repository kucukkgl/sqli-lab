# SQL Injection Lab (Flask + SQLite)

## Setup

1. Run `init_db.py` to create `users.db`
2. Start the app: `python app.py`
3. Visit `http://<target-vm-ip>:5000/` from Burp Suite VM

## Targets

- `/search?user=` → GET-based SQLi
- `/login` → POST-based SQLi
- `/profile` → Cookie-based SQLi (`session_id`)
- `logs.txt` → Forensic trace of all queries

## Challenge

Extract the flag from the hidden `flags` table:
```sql
' UNION SELECT null, flag, null FROM flags--
