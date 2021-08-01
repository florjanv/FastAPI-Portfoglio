from src.routers import education, experience, projects, skills, user, authentication
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(experience.router)
app.include_router(education.router)
app.include_router(skills.router)
app.include_router(projects.router)