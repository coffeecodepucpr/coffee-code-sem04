"""Central API: learnplat (Lessons CRUD + read subjects/users)."""

from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Response, status
import data
from schemas import (
    SubjectOut, UserOut, LessonCreate, LessonUpdate, 
    LessonPatch, LessonOut, TeacherSubjectOut
)

DESCRIPTION = "Learning platform: lessons, subjects, users. In-memory data."

app = FastAPI(
    title="learnplat API",
    description=DESCRIPTION,
    version="1.0.0",
    openapi_tags=[
        {"name": "subjects", "description": "Subjects reference data (read-only)."},
        {"name": "users", "description": "Users reference data (read-only)."},
        {"name": "teacher-subjects", "description": "Linking table (read-only)."},
        {"name": "lessons", "description": "Lessons CRUD."},
    ],
)

# ---------- helper functions ----------
def get_lesson_or_404(lesson_id: int) -> dict:
    lesson = data.LESSONS.get(lesson_id)
    if lesson is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lesson not found")
    return lesson

def validate_student(user_id: int) -> None:
    user = data.USERS.get(user_id)
    if user is None or user["role"] != "student":
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"User {user_id} does not exist or is not a student"
        )

def validate_teacher_subject(teach_subj_id: int) -> None:
    if teach_subj_id not in data.TEACHER_SUBJECTS:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Teacher-subject link {teach_subj_id} does not exist"
        )


# ---------- root ----------

@app.get("/", include_in_schema=False)
def root():
    return {"api": "Learning Platform", "documentation": "/docs"}

# ---------- subjects (read-only) ----------
@app.get(
    "/subjects",
    response_model=list[SubjectOut],
    tags=["subjects"],
    summary="List of subjects"
)
def list_subjects():
    return list(data.SUBJECTS.values())

@app.get(
    "/subjects/{subject_id}",
    response_model=SubjectOut,
    tags=["subjects"],
    summary="Subject by ID",
    responses={404: {"description": "Not found"}}
)
def get_subject(subject_id: int):
    subj = data.SUBJECTS.get(subject_id)
    if subj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")
    return subj

# ---------- users (read-only) ----------
@app.get("/users", response_model=list[UserOut], tags=["users"],
         summary="List of users")
def list_users():
    return list(data.USERS.values())

@app.get(
    "/users/{user_id}",
    response_model=UserOut,
    tags=["users"],
    summary="User by ID",
    responses={404: {"description": "Not found"}}
)
def get_user(user_id: int):
    user = data.USERS.get(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user

# ---------- teacher-subjects (read-only) ----------
@app.get(
    "/teacher-subjects",
    response_model=list[TeacherSubjectOut],
    tags=["teacher-subjects"],
    summary="List of teacher-subject links"
)
def list_teacher_subjects():
    return list(data.TEACHER_SUBJECTS.values())


# ---------- lessons (CRUD) ----------
@app.get(
    "/lessons",
    response_model=list[LessonOut],
    tags=["lessons"],
    summary="List of lessons"
)
def list_lessons(user_id: int | None = None, day_of_week: int | None = None,
                 status_filter: str | None = None):
    lessons = list(data.LESSONS.values())
    if user_id is not None:
        lessons = [l for l in lessons if l["user_id"] == user_id]
    if day_of_week is not None:
        lessons = [l for l in lessons if l["day_of_week"] == day_of_week]
    if status_filter is not None:
        lessons = [l for l in lessons if l["status"] == status_filter]
    return lessons

@app.get(
    "/lessons/{lesson_id}",
    response_model=LessonOut,
    tags=["lessons"],
    summary="Lesson by ID",
    responses={404: {"description": "Not found"}}
)
def get_lesson(lesson_id: int):
    return get_lesson_or_404(lesson_id)

@app.post(
    "/lessons",
    response_model=LessonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["lessons"],
    summary="Create lesson",
    responses={422: {"description": "Invalid data"}}
)
def create_lesson(new_lesson: LessonCreate, response: Response):
    validate_student(new_lesson.user_id)
    validate_teacher_subject(new_lesson.teach_subj_id)
    lesson_id = next(data.LESSON_COUNTER)
    lesson = {**new_lesson.model_dump(), "lesson_id": lesson_id, "created_at": datetime.now(timezone.utc)}
    data.LESSONS[lesson_id] = lesson
    response.headers["Location"] = f"/lessons/{lesson_id}"
    return lesson

@app.put(
    "/lessons/{lesson_id}",
    response_model=LessonOut,
    tags=["lessons"],
    summary="Full lesson replacement",
    responses={404: {"description": "Not found"}, 422: {"description": "Invalid data"}}
)
def replace_lesson(lesson_id: int, new_lesson: LessonUpdate):
    old_lesson = get_lesson_or_404(lesson_id)
    validate_student(new_lesson.user_id)
    validate_teacher_subject(new_lesson.teach_subj_id)
    lesson = {**new_lesson.model_dump(), "lesson_id": lesson_id, "created_at": old_lesson["created_at"]}
    data.LESSONS[lesson_id] = lesson
    return lesson

@app.patch(
    "/lessons/{lesson_id}",
    response_model=LessonOut,
    tags=["lessons"],
    summary="Partial lesson update",
    responses={404: {"description": "Not found"}, 422: {"description": "Invalid data"}}
)
def update_lesson(lesson_id: int, changes: LessonPatch):
    lesson = get_lesson_or_404(lesson_id)
    fields = changes.model_dump(exclude_unset=True)
    if "user_id" in fields:
        validate_student(fields["user_id"])
    if "teach_subj_id" in fields:
        validate_teacher_subject(fields["teach_subj_id"])
    lesson.update(fields)
    return lesson

@app.delete(
    "/lessons/{lesson_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["lessons"],
    summary="Delete lesson",
    responses={404: {"description": "Not found"}}
)
def delete_lesson(lesson_id: int):
    get_lesson_or_404(lesson_id)
    del data.LESSONS[lesson_id]

