import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import date

# Import our tools
# This is the database connection file
from db import get_session

# These are our models
from models.students import Student
from models.enrollments import Enrollment
from models.courses import Course

app = FastAPI()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Root Route"}


@app.get('/courses')
def get_courses(session: Session = Depends(get_session)):
    statement = select(Course)
    results = session.exec(statement)
    return results.all()


@app.get('/students')
def get_students(session: Session = Depends(get_session), ):
    statement = select(Student)
    results = session.exec(statement)
    return results.all()


@app.get('/enrollments')
def get_enrollments(session: Session = Depends(get_session), ):
    statement = (
        select(Enrollment, Student, Course)
        .join(Student, Student.id == Enrollment.student_id)
        .join(Course, Course.id == Enrollment.course_id)
    )
    results = session.exec(statement).all()
    enrollments_list = [
        {
            "enrollment_id": enrollment.id,
            "student": student.student_name,
            "course": course.course_name,
        }
        for enrollment, student, course in results
    ]

    return enrollments_list


@app.post('/students/add')
async def add_student(name: str, session: Session = Depends(get_session)):
    student = Student(student_name=name)
    session.add(student)
    session.commit()
    return {"Student Added": student.student_name}


@app.post('/courses/add')
async def add_course(name: str, session: Session = Depends(get_session)):
    course = Course(course_name=name)
    session.add(course)
    session.commit()
    return {"Course Added": course.course_name}


@app.post('/enrollments/add')
async def add_enrollment(student_id: int, course_id: int, enrollment_date: date, session: Session = Depends(get_session)):
    enrollment = Enrollment(
        student_id=student_id, course_id=course_id, enrollment_date=enrollment_date)
    session.add(enrollment)
    session.commit()
    return {"message": "Enrollment Added"}


@app.put('/students/update')
async def add_student(id: int, name: str, session: Session = Depends(get_session)):
    statement = select(Student).where(Student.id == id)
    results = session.exec(statement)
    student = results.one()
    if student is not None:
        student.student_name = name
        session.add(student)
        session.commit()
        return {"Student Updated": student.student_name}
    else:
        return {"message": "User ID not found"}


@app.put('/courses/update')
async def add_course(id: int, name: str, session: Session = Depends(get_session)):
    statement = select(Course).where(Course.id == id)
    results = session.exec(statement)
    course = results.one()
    if course is not None:
        course.course_name = name
        session.add(course)
        session.commit()
        return {"Course Updated": course.course_name}
    else:
        return {"message": "Course ID not found"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
