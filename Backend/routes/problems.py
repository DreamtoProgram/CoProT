from fastapi import APIRouter, Depends, HTTPException, status

from Backend.database.connection import get_db
from Backend.schemas.problem import (
    ProblemCreate,
    ProblemUpdate,
    ProblemResponse,
    ProblemsResponse,
    MessageResponse
)
from Backend.utils.auth import get_current_user


router = APIRouter(
    prefix="/problems",
    tags=["Problems"]
)


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED
)
def create_problem(
    problem: ProblemCreate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):

    try:
        cursor = db.cursor()

        query = """
            INSERT INTO problems
            (
                problem_name,
                platform,
                topic,
                difficulty,
                attempts,
                has_universal_pattern,
                pattern_name,
                notes,
                solved_date,
                user_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            problem.problem_name,
            problem.platform,
            problem.topic,
            problem.difficulty,
            problem.attempts,
            problem.has_universal_pattern,
            problem.pattern_name,
            problem.notes,
            problem.solved_date,
            user["user_id"]
        )

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return {
            "message": "Data successfully validated and recorded into CoProT database!"
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get(
    "/",
    response_model=ProblemsResponse
)
def get_problems(
    user=Depends(get_current_user),
    db=Depends(get_db)
):

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM problems WHERE user_id = %s",
        (user["user_id"],)
    )

    problems = cursor.fetchall()
    cursor.close()

    if not problems:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No problems found for the user"
        )

    return {
        "count": len(problems),
        "problems": problems
    }


@router.get(
    "/{problem_id}",
    response_model=ProblemResponse
)
def get_problem(
    problem_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):

    try:
        cursor = db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM problems
            WHERE problem_id = %s
            AND user_id = %s
            """,
            (problem_id, user["user_id"])
        )

        problem = cursor.fetchone()
        cursor.close()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )

    return problem


@router.delete(
    "/{problem_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK
)
def delete_problem(
    problem_id: int,
    user=Depends(get_current_user),
    db=Depends(get_db)
):

    try:
        cursor = db.cursor()

        cursor.execute(
            """
            DELETE FROM problems
            WHERE problem_id = %s
            AND user_id = %s
            """,
            (problem_id, user["user_id"])
        )

        deleted = cursor.rowcount

        db.commit()
        cursor.close()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

    if deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )

    return {
        "message": "Problem deleted successfully"
    }


@router.put(
    "/{problem_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK
)
def update_problem(
    problem_id: int,
    update_credentials: ProblemUpdate,
    user=Depends(get_current_user),
    db=Depends(get_db)
):

    update_data = update_credentials.model_dump(exclude_unset=True)

    if not update_data:
        return {
            "message": "No data provided; nothing to update"
        }

    try:
        cursor = db.cursor()

        variables = []
        values = []

        for key, value in update_data.items():
            variables.append(f"{key} = %s")
            values.append(value)

        set_clause = ", ".join(variables)

        query = f"""
            UPDATE problems
            SET {set_clause}
            WHERE problem_id = %s
            AND user_id = %s
        """

        values.append(problem_id)
        values.append(user["user_id"])

        cursor.execute(query, values)

        updated = cursor.rowcount

        db.commit()
        cursor.close()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

    if updated == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )

    return {
        "message": "Updated Successfully"
    }