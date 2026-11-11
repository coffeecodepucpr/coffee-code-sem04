"The schemas that describe the format of the API data."

from datetime import datetime, date, time
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

# ---------- read-only reference data ----------
class SubjectOut(BaseModel):
    subject_id: int
    name: str
    code: str

class UserOut(BaseModel):
    user_id: int
    role: Literal["teacher", "student"]
    user_name: str = Field(min_length=1, max_length=120)
    email: str
    created_at: datetime

# ---------- lessons (CRUD) ----------
VALID_STATUSES = ("scheduled", "completed", "canceled")

class LessonBase(BaseModel):
    user_id: int = Field(gt=0, description="Student ID")
    teach_subj_id: int = Field(gt=0, description="Teacher-subject link ID")
    day_of_week: int = Field(ge=1, le=7, description="1=Mon ... 7=Sun")
    start_time: time
    end_time: time
    status: Literal["scheduled", "completed", "canceled"]

class LessonCreate(LessonBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "user_id": 3, "teach_subj_id": 1, "day_of_week": 2,
                "start_time": "18:00", "end_time": "19:00", "status": "scheduled",
            }]
        }
    )

class LessonUpdate(LessonBase):
    """Full lesson replacement (PUT)."""

class LessonPatch(BaseModel):
    """Partial update (PATCH). Null is not allowed for required fields."""
    user_id: int | None = Field(default=None, gt=0)
    teach_subj_id: int | None = Field(default=None, gt=0)
    day_of_week: int | None = Field(default=None, ge=1, le=7)
    start_time: time | None = None
    end_time: time | None = None
    status: Literal["scheduled", "completed", "canceled"] | None = None

    @field_validator("user_id", "teach_subj_id", "day_of_week", "start_time", "end_time", "status")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("this field does not accept null: omit it to leave it unchanged")
        return value

class LessonOut(LessonBase):
    lesson_id: int

class TeacherSubjectOut(BaseModel):
    teach_subj_id: int
    user_id: int
    subject_id: int
    created_at: date
