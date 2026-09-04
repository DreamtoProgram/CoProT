from fastapi import APIRouter, HTTPException, Depends, status
# import pymysql
from Backend.database.connection import get_db
from Backend.schemas import user
from Backend.schemas.problem import ProblemCreate, ProblemUpdate, ProblemResponse, ProblemsResponse, MessageResponse
from Backend.utils.auth import get_current_user

router = APIRouter(
    prefix = "/problems",
    tags = ['Problems']
)

@router.post('/', 
            response_model = MessageResponse,
            status_code = status.HTTP_201_CREATED
            )
def createProblem(problem : ProblemCreate, user = Depends(get_current_user), db = Depends(get_db)) -> str:

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "User not authenticated"
        )
    
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

        return {"message": "Data Successfully validated and recorded into coprot database!"}

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal Server Error: {str(e)}"
        )
    
@router.get('/', response_model = ProblemsResponse)
def get_problem(user = Depends(get_current_user),db = Depends(get_db)):

    cursor = db.cursor()

    cursor.execute(
        'select * from problems where user_id = %s', (user["user_id"],)
    )

    problems = cursor.fetchall()

    cursor.close()

    if not problems:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No problems found for the user"
        )

    count = len(problems)

    return {
        "count" : count,
        "problems" : list(problems)
    }


@router.get('/{problemId}', response_model = ProblemResponse)
def get_problem(problemId : int, user = Depends(get_current_user), db = Depends(get_db)):
    try:
        cursor = db.cursor()

        cursor.execute(
            "Select * from problems " \
            "where problem_id = %s and user_id = %s", (problemId, user["user_id"])
        )

        requiredProblem = cursor.fetchone()

        cursor.close()

    except Exception:
            raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    if requiredProblem:
        return requiredProblem

    else:
        raise HTTPException(
        status_code=404,
        detail="Problem not found"
    )

    


@router.delete('/{problem_id}', response_model = MessageResponse, status_code = status.HTTP_200_OK)  # for Modification successfull code is 200 code.
def delete_problem(problem_id : int, user = Depends(get_current_user), db = Depends(get_db)):
    try:

        cursor = db.cursor()
        cursor.execute(
            'Delete from problems where problem_id = %s and user_id = %s', (problem_id, user["user_id"])
        )
        deleted_or_not = cursor.rowcount
        cursor.close()
        db.commit()
        
        if deleted_or_not == 1:
            return {
                'message' : 'problem deleted successfully'
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="Problem not found"
            )

    except Exception:
        raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )


@router.put('/{problem_id}', response_model = MessageResponse, status_code = status.HTTP_200_OK)
def update_problem(problem_id : int, update_credentials : ProblemUpdate, db = Depends(get_db), user = Depends(get_current_user)):

    try:
        cursor = db.cursor()
        update_data = update_credentials.model_dump(exclude_unset=True) # very important without this we will not be able to perform partial update feature.

        if not update_data:
            return {
                'message' : 'Not Provided; Data needs to update'
            }
        
        variables = []
        values = []

        for key, value in update_data.items():
            variables.append(f"{key} = %s")
            values.append(value)

        set_clause = ', '.join(variables)
        query = f"""
            Update problems
            set {set_clause}
            where
            problem_id = %s and user_id = %s
            """

        values.append(problem_id)
        values.append(user["user_id"])
        update_values = (
            values
        )

        cursor.execute(query, update_values)

        updated_or_not = cursor.rowcount
        db.commit()
        cursor.close()

        if updated_or_not == 1:
            return {
                'message' : 'Updated Successfully'
            }

        raise HTTPException(
                status_code=404,
                detail="Problem not found"
            )
    

    except Exception:
        raise HTTPException (
            status_code = 500,
            detail = "Internal Server Error"
        )


    