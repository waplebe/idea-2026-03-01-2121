from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlmodel
from sqlmodel import Field, SQLModel, create_engine, Session
import os
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///tasks.db")

app = FastAPI()

engine = create_engine(DATABASE_URL, echo=False)

class Task(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    title: str
    description: str
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

create_db_tables()

@app.get("/tasks", response_model=List[Task])
async def list_tasks():
    with Session(engine) as session:
        tasks = session.query(Task).all()
        return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    with Session(engine) as session:
        task.id = task_id
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return {"message": "Task deleted"}

@app.get("/tasks/search", response_model=List[Task])
async def search_tasks(title: str = None, description: str = None):
    """
    Searches tasks based on title and description.
    """
    with Session(engine) as session:
        query = session.query(Task)
        if title:
            query = query.filter(Task.title.contains(title))
        if description:
            query = query.filter(Task.description.contains(description))
        tasks = query.all()
        return tasks