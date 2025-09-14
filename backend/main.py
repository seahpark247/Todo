from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# CORS setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB connect
conn = psycopg2.connect(
    host="localhost",
    database="todo",
    user="todo",
    password="1234",
    cursor_factory=RealDictCursor
)
cur = conn.cursor()

# Pydantic Model
class Todo(BaseModel):
    title: str
    completed: bool = False

@app.get("/todos")
def get_todos():
    cur.execute("SELECT * FROM todos ORDER BY id DESC")
    return cur.fetchall()

@app.post("/todos")
def create_todo(todo: Todo):
    cur.execute(
        "INSERT INTO todos (title, completed) VALUES (%s, %s) RETURNING *",
        (todo.title, todo.completed)
    )
    new_todo = cur.fetchone()
    conn.commit()
    return new_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    cur.execute(
        "UPDATE todos SET title=%s, completed=%s WHERE id=%s RETURNING *",
        (todo.title, todo.completed, todo_id)
    )
    updated = cur.fetchone()
    conn.commit()
    return updated

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    cur.execute("DELETE FROM todos WHERE id=%s RETURNING *", (todo_id,))
    deleted = cur.fetchone()
    conn.commit()
    return deleted