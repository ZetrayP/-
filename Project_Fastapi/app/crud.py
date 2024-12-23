from sqlmodel import Session, select
from .models import Student, Group
from typing import List
import random

def create_student(session: Session, name: str, email: str, group_id: int = None) -> Student:
    student = Student(name=name, email=email, group_id=group_id)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def create_group(session: Session, name: str) -> Group:
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

def get_student(session: Session, student_id: int) -> Student:
    return session.get(Student, student_id)

def get_group(session: Session, group_id: int) -> Group:
    return session.get(Group, group_id)

def delete_student(session: Session, student_id: int):
    student = session.get(Student, student_id)
    if student:
        session.delete(student)
        session.commit()

def delete_group(session: Session, group_id: int):
    group = session.get(Group, group_id)
    if group:
        session.delete(group)
        session.commit()

def get_students(session: Session) -> List[Student]:
    statement = select(Student)
    return session.exec(statement).all()

def get_groups(session: Session) -> List[Group]:
    statement = select(Group)
    return session.exec(statement).all()

def add_student_to_group(session: Session, student_id: int, group_id: int):
    student = session.get(Student, student_id)
    if student:
        student.group_id = group_id
        session.commit()

def remove_student_from_group(session: Session, student_id: int):
    student = session.get(Student, student_id)
    if student:
        student.group_id = None
        session.commit()

def group_students(session: Session):
    students = session.query(Student).all()
    groups = session.query(Group).all()
    if not groups:
        raise ValueError("No groups available")
    random.shuffle(students)
    group_count = len(groups) 
    for index, student in enumerate(students):
        student.group_id = groups[index % group_count].id
        session.add(student)
    session.commit()

def transfer_student(session: Session, student_id: int, new_group_id: int):
    student = session.get(Student, student_id)
    if student:
        student.group_id = new_group_id
        session.commit()
