from fastapi import FastAPI
from Backend.routes.problems import router as problem_router
from Backend.routes.users import router as user_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title = "CoProT",
    description = "Hey, Welcome to Coding Problem Tracker- Keep track on your solved coding problems."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def homePage() -> dict:
    return {
        'message' : 'Welcome User, to your CoProT'
    }

app.include_router(problem_router)
app.include_router(user_router)

