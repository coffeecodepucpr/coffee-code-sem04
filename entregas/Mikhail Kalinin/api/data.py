"""In-memory data. Everything resets to the seed state on server restart."""
import itertools
from datetime import datetime, timezone, date, time

SUBJECTS = {
    1: {"subject_id": 1, "name": "Mathematics", "code": "MAT101"},
    2: {"subject_id": 2, "name": "Physics", "code": "PHY101"},
    3: {"subject_id": 3, "name": "Programming", "code": "PRO101"},
    4: {"subject_id": 4, "name": "History", "code": "HIS101"},
    5: {"subject_id": 5, "name": "Literature", "code": "LIT101"},
    6: {"subject_id": 6, "name": "Chemistry", "code": "CHE101"},
}

USERS = {
    1: {"user_id": 1, "role": "teacher", "user_name": "James Anderson",
        "email": "james.anderson@example.com", "created_at": datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)},
    2: {"user_id": 2, "role": "teacher", "user_name": "Emily Thompson",
        "email": "emily.thompson@example.com", "created_at": datetime(2026, 9, 2, 12, 0, tzinfo=timezone.utc)},
    3: {"user_id": 3, "role": "student", "user_name": "Michael Davis",
        "email": "michael.davis@example.com", "created_at": datetime(2026, 9, 3, 12, 0, tzinfo=timezone.utc)},
    4: {"user_id": 4, "role": "student", "user_name": "Sarah Wilson",
        "email": "sarah.wilson@example.com", "created_at": datetime(2026, 9, 4, 12, 0, tzinfo=timezone.utc)},
    5: {"user_id": 5, "role": "student", "user_name": "David Martinez",
        "email": "david.martinez@example.com", "created_at": datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)},
    6: {"user_id": 6, "role": "student", "user_name": "Jessica Brown",
        "email": "jessica.brown@example.com", "created_at": datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc)},
    7: {"user_id": 7, "role": "student", "user_name": "Christopher Lee",
        "email": "christopher.lee@example.com", "created_at": datetime(2026, 9, 7, 12, 0, tzinfo=timezone.utc)},
    8: {"user_id": 8, "role": "student", "user_name": "Olivia Taylor",
        "email": "olivia.taylor@example.com", "created_at": datetime(2026, 9, 8, 12, 0, tzinfo=timezone.utc)},
}

# N:N link between teacher and subject
TEACHER_SUBJECTS = {
    1: {"teach_subj_id": 1, "user_id": 1, "subject_id": 1, "created_at": date(2026, 9, 1)},
    2: {"teach_subj_id": 2, "user_id": 1, "subject_id": 2, "created_at": date(2026, 9, 2)},
    3: {"teach_subj_id": 3, "user_id": 1, "subject_id": 3, "created_at": date(2026, 9, 3)},
    4: {"teach_subj_id": 4, "user_id": 2, "subject_id": 4, "created_at": date(2026, 9, 4)},
    5: {"teach_subj_id": 5, "user_id": 2, "subject_id": 5, "created_at": date(2026, 9, 5)},
    6: {"teach_subj_id": 6, "user_id": 1, "subject_id": 6, "created_at": date(2026, 9, 6)},
}

LESSONS = {
    1: {"lesson_id": 1, "user_id": 7, "teach_subj_id": 1, "day_of_week": 1,
        "start_time": time(18, 0), "end_time": time(19, 0), "status": "completed"},
    2: {"lesson_id": 2, "user_id": 4, "teach_subj_id": 2, "day_of_week": 2,
        "start_time": time(19, 0), "end_time": time(20, 0), "status": "canceled"},
    3: {"lesson_id": 3, "user_id": 6, "teach_subj_id": 3, "day_of_week": 3,
        "start_time": time(10, 0), "end_time": time(11, 0), "status": "canceled"},
    4: {"lesson_id": 4, "user_id": 3, "teach_subj_id": 4, "day_of_week": 4,
        "start_time": time(19, 30), "end_time": time(20, 30), "status": "scheduled"},
    5: {"lesson_id": 5, "user_id": 8, "teach_subj_id": 5, "day_of_week": 5,
        "start_time": time(17, 0), "end_time": time(18, 0), "status": "scheduled"},
    6: {"lesson_id": 6, "user_id": 3, "teach_subj_id": 6, "day_of_week": 6,
        "start_time": time(18, 30), "end_time": time(19, 30), "status": "scheduled"},
}

LESSON_COUNTER = itertools.count(7)
