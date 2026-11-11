# Central API

API for managing lessons (CRUD). Data is stored in memory.

## Installation and Running

1. Create and activate a virtual environment:
   - **Windows:** `py -m venv .venv` and `.venv\Scripts\activate`
   - **macOS/Linux:** `python3 -m venv .venv` and `source .venv/bin/activate`

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server in development mode:
   ```bash
   fastapi dev main.py
   ```

## Documentation
Interactive documentation (Swagger UI) is available at:  
http://127.0.0.1:8000/docs

## Tests

| # | Request | Expected result |
|---|---|---|
| 1 | `GET /lessons` | `200`, list of 6 lessons (each includes `created_at`) |
| 2 | `GET /lessons?status_filter=scheduled` | `200`, only the 3 scheduled lessons (IDs 4, 5, 6) |
| 3 | `GET /lessons?user_id=3` | `200`, only lessons for user 3 (IDs 4, 6) |
| 4 | `GET /lessons/3` | `200`, the lesson with `lesson_id` 3 (includes `created_at`) |
| 5 | `GET /lessons/99` | `404`, `Lesson not found` |
| 6 | `GET /lessons/abc` | `422`, `int_parsing`, with `loc` pointing to `path` and `lesson_id` |
| 7 | `POST /lessons` with `{"user_id": 5, "teach_subj_id": 1, "day_of_week": 1, "start_time": "09:00", "end_time": "10:00", "status": "scheduled"}` | `201`, `lesson_id` 7, includes `created_at`, header `Location: /lessons/7` |
| 8 | `POST /lessons` with `{"user_id": 99, "teach_subj_id": 1, "day_of_week": 1, "start_time": "09:00", "end_time": "10:00", "status": "scheduled"}` | `422`, `User 99 does not exist or is not a student` |
| 9 | `POST /lessons` with `{"user_id": 5, "teach_subj_id": 99, "day_of_week": 1, "start_time": "09:00", "end_time": "10:00", "status": "scheduled"}` | `422`, `Teacher-subject link 99 does not exist` |
| 10 | `POST /lessons` with `{"user_id": 5, "teach_subj_id": 1, "day_of_week": 8, "start_time": "09:00", "end_time": "10:00", "status": "scheduled"}` | `422`, `greater_than_equal`, with `loc` pointing to `body` and `day_of_week` |
| 11 | `PUT /lessons/7` with `{"user_id": 5, "teach_subj_id": 2, "day_of_week": 2, "start_time": "10:00", "end_time": "11:00", "status": "completed"}` | `200`, the fully replaced lesson |
| 12 | `PATCH /lessons/7` with `{"status": "canceled"}` | `200`, only the status changed to "canceled" (`created_at` is unchanged) |
| 13 | `PATCH /lessons/7` with `{"user_id": null}` | `422`, `value_error`, with `loc` pointing to `body` and `user_id`, message containing "does not accept null" |
| 14 | `DELETE /lessons/7` | `204`, no body |
| 15 | `DELETE /lessons/7` again | `404`, `Lesson not found` |
| 16 | `DELETE /lessons` | `405 Method Not Allowed` |
| 17 | `GET /subjects/99` | `404`, `Subject not found` |
