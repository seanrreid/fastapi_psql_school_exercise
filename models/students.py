from .base import Base


class Students(Base, table=True):
    __tablename__ = "students"

    name: str

    def __repr__(self):
        return f"<Student {self.name!r}>"
