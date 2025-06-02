from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from decimal import Decimal, ROUND_HALF_UP

app = FastAPI()

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class Student(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

grade_to_point = {
    "A+": 4.5, "A": 4.0,
    "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0,
    "D+": 1.5, "D": 1.0,
    "F": 0.0
}

@app.post("/calculate-gpa")
def calculate_gpa(student: Student):
    total_points = Decimal('0')
    total_credits = Decimal('0')

    for course in student.courses:
        if course.grade not in grade_to_point:
            raise HTTPException(status_code=400, detail=f"Invalid grade: {course.grade}")
        total_points += Decimal(str(grade_to_point[course.grade])) * Decimal(str(course.credits))
        total_credits += Decimal(str(course.credits))

    if total_credits == 0:
        raise HTTPException(status_code=400, detail="No credits found")

    gpa = (total_points / total_credits).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    gpa = float(gpa)

    return {
        "student_summary": {
            "student_id": student.student_id,
            "name": student.name,
            "gpa": gpa,
            "total_credits": int(total_credits)
        }
    }
