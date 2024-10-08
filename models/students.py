from .base import Base


class Student(Base, table=True):
    __tablename__ = "students"

    student_name: str

    def __repr__(self):
        return f"<Student {self.student_name!r}>"
