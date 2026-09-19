import psycopg2
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title : str
    description: str | None = None
    completed: bool

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "2.2"
    }

@app.get("/config")
def config():
    return {
	"db_host": os.getenv("DB_HOST"),
	"db_port": os.getenv("DB_PORT"),
	"db_name": os.getenv("DB_NAME"),
	"db_user": os.getenv("DB_USER")
    }

@app.get("/db-health")
def db_health():
    try:
        connection = psycopg2.connect(
	    host=os.getenv("DB_HOST"),
	    port=os.getenv("DB_PORT"),
	    database=os.getenv("DB_NAME"),
	    user=os.getenv("DB_USER"),
	    password=os.getenv("DB_PASSWORD")
	)

        connection.close()

        return {"database": "ok"}

    except Exception as e:
        return {
	    "database": "error",
	    "message": str(e)
	}

@app.post("/tasks")
def create_task(task: Task):
    try:
        connection = psycopg2.connect(
	    host=os.getenv("DB_HOST"),
	    port=os.getenv("DB_PORT"),
	    database=os.getenv("DB_NAME"),
	    user=os.getenv("DB_USER"),
	    password=os.getenv("DB_PASSWORD")
        )

        cursor = connection.cursor()

        cursor.execute(
	    """
	    INSERT INTO tasks (title, description)
	    VALUES (%s, %s)
	    RETURNING id, title, description, completed
	    """,
	    (task.title, task.description)
        )

        new_task = cursor.fetchone()

        connection.commit()

        cursor.close()

        connection.close()

        return {
	    "id": new_task[0],
	    "title": new_task[1],
	    "description": new_task[2],
	    "completed": new_task[3]
        }

    except Exception as e:
        return {
	    "error": str(e)
        }

@app.get("/tasks")
def get_tasks():
    try:
        connection = psycopg2.connect(
	    host=os.getenv("DB_HOST"),
	    port=os.getenv("DB_PORT"),
	    database=os.getenv("DB_NAME"),
	    user=os.getenv("DB_USER"),
	    password=os.getenv("DB_PASSWORD")
        )

        cursor = connection.cursor()

        cursor.execute(
	    """
	    SELECT id, title, description, completed
	    FROM tasks
	    ORDER BY id
	    """
        )

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        tasks = []

        for row in rows:
            tasks.append({
	        "id": row[0],
	        "title": row[1],
	        "description": row[2],
	        "completed": row[3]
	    })

        return tasks

    except Exception as e:
        return {
	    "error": str(e)
        }

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = connection.cursor()

        cursor.execute(
	    """
	    UPDATE tasks
	    SET title = %s,
	        description = %s,
	        completed = %s
	    WHERE id = %s
	    RETURNING id, title, description, completed
	    """,
	    (
	        task.title,
	        task.description,
	        task.completed,
	        task_id
	    )
        )

        updated_task = cursor.fetchone()

        if updated_task is None:
            connection.rollback()
            cursor.close()
            connection.close()

            return {"error": "Task not found"}

        connection.commit()

        cursor.close()
        connection.close()

        return{
            "id": updated_task[0],
            "title": updated_task[1],
            "description": updated_task[2],
            "completed": updated_task[3]
        }

    except Exception as e:
        return{
            "error": str(e)
        }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            RETURNING id
            """,
            (task_id,)
        )

        deleted_task = cursor.fetchone()

        if deleted_task is None:
            connection.rollback()
            cursor.close()
            connection.close()

            return {"error": "Task not found"}

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "message": "Task deleted",
            "id": deleted_task[0]
        }

    except Exception as e:
        return {
            "error": str(e)
        }
