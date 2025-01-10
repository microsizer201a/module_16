from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {"1": "Имя: Example, возраст: 18"}

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
                   age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]):
    curr_id_ = str(int(max(users, key=int)) + 1 if users else 1)
    users[curr_id_] = f"Имя: {username}, возраст: {age}"
    return f"User {curr_id_} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=200, description="Enter User Id", example="1")],
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]):
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} is updated"

@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(ge=1, le=200, discription="Enter User Id", example=1)):
    users.pop(str(user_id))
    return f"User {user_id} has been deleted"

