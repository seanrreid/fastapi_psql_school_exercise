from sqlmodel import Field

from .base import Base


class Enrollments(Base, table=True):
    student_id: int = Field(foreign_key="students.id")
    course_id: int = Field(foreign_key="courses.id")
    enrollment_date: date
