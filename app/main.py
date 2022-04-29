from fastapi import FastAPI
from .database import engine
from . import models
from routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# allows path operations to be in different modules, by grabbing router object from post and user files
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# Path (or Route) operation
@app.get("/")  # root path
# Path operation function
def root():
    # whatever is returned is what gets sent back to the user and Fast API converts it to JSON
    return {"message": "Welcome to my API !!!!! cool"}
