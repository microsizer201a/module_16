from http.client import HTTPException

from fastapi import FastAPI, Path
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    id: Annotated[int, Path(ge=1, le=200, description="Enter User Id", example="1")]
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")]
    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")],
        user: User):
    new_id = int(max(user.id for user in users)) + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return f"User {new_user.id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=200, description="Enter User Id", example="1")],
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")],
        user: User):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(ge=1, le=200, discription="Enter User Id", example=1)):
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return user
    raise HTTPException(status_code=404, detail="User was not found")