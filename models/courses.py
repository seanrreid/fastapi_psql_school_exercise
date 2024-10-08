from .base import Base

class Course(Base, table=True):
    __tablename__ = "courses"

    course_name: str
