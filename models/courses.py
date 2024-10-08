from .base import Base

class Courses(Base):
    __tablename__ = "courses"

    name: str
