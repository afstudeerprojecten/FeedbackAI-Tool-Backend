from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.database import async_engine, Base


class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="organisation")
    teachers = relationship("Teacher", back_populates="organisation")
    students = relationship("Student", back_populates="organisation")

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    name = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, default="teacher")
    organisation = relationship("Organisation", back_populates="teachers")
    courses = relationship("Course", back_populates="teacher")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    name = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, default="student")
    organisation = relationship("Organisation", back_populates="students")
    submissions = relationship("Submission", back_populates="student")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    name = Column(String)
    teacher = relationship("Teacher", back_populates="courses")
    assignments = relationship("Assignment", back_populates="course")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String)
    description = Column(String)
    word_count = Column(Integer)
    student_ages = Column(Integer)
    course = relationship("Course", back_populates="assignments")
    templates = relationship("Template", back_populates="assignment")
    submissions = relationship("Submission", back_populates="assignment")

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    content = Column(Text)
    assignment = relationship("Assignment", back_populates="templates")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    content = Column(Text)
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")
    feedback = relationship("Feedback", uselist=False, back_populates="submission")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    content = Column(Text)
    submission = relationship("Submission", back_populates="feedback")

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="admin")