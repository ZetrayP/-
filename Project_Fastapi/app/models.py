from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Group(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    students: List["Student"] = Relationship(back_populates="group")

class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    group_id: Optional[int] = Field(default=None, foreign_key="group.id")
    group: Optional[Group] = Relationship(back_populates="students")
