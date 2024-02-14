from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from db import engine

Base = declarative_base()


class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Enrollments(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey("students.id"))
    course_id = Column(ForeignKey("courses.id"))
    enrollment_date = Column(Date)


Base.metadata.create_all(engine)
