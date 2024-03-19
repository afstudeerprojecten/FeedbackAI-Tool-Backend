from enum import Enum
from sqlalchemy.types import Enum as SQLAlchemyEnum
import os
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship


class Organisation(Base):
    __tablename__ = 'organisations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    teachers = relationship("Teacher", back_populates="organisation")
    students = relationship("Student", back_populates="organisation")
    role = Column(String, default="organisation")

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    organisation_id = Column(Integer, ForeignKey('organisations.id'))

    organisation = relationship("Organisation", back_populates="teachers")
    role = Column(String, default="teacher")


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    organisation_id = Column(Integer, ForeignKey('organisations.id'))

    organisation = relationship("Organisation", back_populates="students")
    role = Column(String, default="student")


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship("Teacher", back_populates="courses")

class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    templates = relationship("Template", back_populates="assignment")

class Template(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'))

    assignment = relationship("Assignment", back_populates="templates")

class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    student_id = Column(Integer, ForeignKey('students.id'))

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")

class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    submission_id = Column(Integer, ForeignKey('submissions.id'))

    submission = relationship("Submission", uselist=False, back_populates="feedback")
