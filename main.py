import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

# Import our tools
# This is the database connection file
from db import get_session

# These are our models
from models.students import Students
from models.enrollments import Enrollments
from models.courses import Courses

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
def get_courses(session: Session = Depends(get_session), ):
    courses = session.query(Courses)
    return courses.all()


@app.get('/students')
def get_students(session: Session = Depends(get_session), ):
    students = session.query(Students)
    return students.all()


@app.get('/enrollments')
def get_enrollments(session: Session = Depends(get_session), ):
    enrollments = session.query(Enrollments, Students, Courses).join(
        Students, Students.id == Enrollments.student_id).join(Courses, Courses.id == Enrollments.course_id)

    # We can't just return the all() value...
    # ...all() will return a series of tuples, containing a instance of each class.
    # But, we can assign it to a variable...
    all_enrollments = enrollments.all()

    # ...then we can use a for loop to make a list
    # conventional syntax
    enrollments_list = []
    for enrollment in all_enrollments:
        enrollment_dict = {
            "enrollment_id": enrollment.Enrollments.id,
            "student_name": enrollment.Students.name,
            "course_name": enrollment.Courses.name,
        }
        enrollments_list.append(enrollment_dict)

    # alternative method, using list comprehension syntax
    # enrollments_list = [
    #     {
    #         "enrollment_id": enrollment.Enrollments.id,
    #         "student_name": enrollment.Students.name,
    #         "course_name": enrollment.Courses.name,
    #     }
    #     for enrollment in enrollments
    # ]

    # When we get back that list...
    # ...we need to import the proper response class to be returned
    return JSONResponse(content={"enrollments": enrollments_list})


@app.post('/students/add')
async def add_student(name: str, session: Session = Depends(get_session)):
    student = Students(name=name)
    session.add(student)
    session.commit()
    return {"Student Added": student.name}


@app.post('/courses/add')
async def add_course(name: str, session: Session = Depends(get_session)):
    course = Courses(name=name)
    session.add(course)
    session.commit()
    return {"Course Added": course.name}


@app.post('/enrollments/add')
async def add_enrollment(student_id: int, course_id: int, enrollment_date: date, session: Session = Depends(get_session)):
    enrollment = Enrollments(
        student_id=student_id, course_id=course_id, enrollment_date=enrollment_date)
    session.add(enrollment)
    session.commit()
    return {"message": "Enrollment Added"}


@app.put('/students/update')
async def add_student(id: int, name: str, session: Session = Depends(get_session)):
    student = session.query(Student).filter(Student.id == id).first()
    if student is not None:
        student.name = name
        session.add(student)
        session.commit()
        return {"Student Updated": student.name}
    else:
        return {"message": "User ID not found"}


@app.put('/courses/update')
async def add_course(id: int, name: str, session: Session = Depends(get_session)):
    course = session.query(Courses).filter(Courses.id == id).first()
    if course is not None:
        course.name = name
        session.add(course)
        session.commit()
        return {"Course Updated": course.name}
    else:
        return {"message": "Course ID not found"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
