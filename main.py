from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import our tools
# This is the database connection file
from db import session

# These are our models
from models import Students, Enrollments, Courses

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
def get_courses():
    courses = session.query(Courses)
    return courses.all()


@app.get('/students')
def get_students():
    students = session.query(Students)
    return students.all()

@app.get('/enrollments')
def get_enrollments():
    enrollments = session.query(Enrollments, Students, Courses).join(Students, Students.id == Enrollments.student_id).join(Courses, Courses.id == Enrollments.course_id)

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
