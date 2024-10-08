from sqlmodel import Field
from datetime import date

from .base import Base


class Enrollment(Base, table=True):
    __tablename__ = "enrollments"

    student_id: int = Field(foreign_key="students.id")
    course_id: int = Field(foreign_key="courses.id")
    enrollment_date: date
