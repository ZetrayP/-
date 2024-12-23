from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from .database import get_session
from .models import Student, Group
from .crud import (
    create_student, create_group, get_student, get_group,
    delete_student, delete_group, get_students, get_groups,
    add_student_to_group, remove_student_from_group, group_students, transfer_student
)

router = APIRouter()

@router.post("/students", response_model=Student)
async def api_create_student(name: str, email: str, group_id: int = None, session: Session = Depends(get_session)):
    return create_student(session, name, email, group_id)

@router.post("/groups", response_model=Group)
async def api_create_group(name: str, session: Session = Depends(get_session)):
    return create_group(session, name)

@router.get("/students/{student_id}", response_model=Student)
async def api_get_student(student_id: int, session: Session = Depends(get_session)):
    student = get_student(session, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/groups/{group_id}", response_model=Group)
async def api_get_group(group_id: int, session: Session = Depends(get_session)):
    group = get_group(session, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.delete("/students/{student_id}")
async def api_delete_student(student_id: int, session: Session = Depends(get_session)):
    delete_student(session, student_id)
    return {"detail": "Student deleted"}

@router.delete("/groups/{group_id}")
async def api_delete_group(group_id: int, session: Session = Depends(get_session)):
    delete_group(session, group_id)
    return {"detail": "Group deleted"}

@router.get("/students", response_model=list[Student])
async def api_get_students(session: Session = Depends(get_session)):
    return get_students(session)

@router.get("/groups", response_model=list[Group])
async def api_get_groups(session: Session = Depends(get_session)):
    return get_groups(session)

@router.post("/groups/{group_id}/students/{student_id}")
async def api_add_student_to_group(group_id: int, student_id: int, session: Session = Depends(get_session)):
    add_student_to_group(session, student_id, group_id)
    return {"detail": "Student added to group"}

@router.delete("/groups/{group_id}/students/{student_id}")
async def api_remove_student_from_group(group_id: int, student_id: int, session: Session = Depends(get_session)):
    remove_student_from_group(session, student_id)
    return {"detail": "Student removed from group"}

@router.post("/group_students")
async def api_group_students(session: Session = Depends(get_session)):
    try:
        group_students(session)
        return {"detail": "All students were randomly grouped"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/students/{student_id}/transfer/{new_group_id}")
async def api_transfer_student(student_id: int, new_group_id: int, session: Session = Depends(get_session)):
    transfer_student(session, student_id, new_group_id)
    return {"detail": "Students have been moved to a new group"}
