"""FastAPI Service Lab
Goal: Build a task management API with proper routing, schemas, and DI
"""
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(title="Task Management API")


# TODO: Define Pydantic models
# class TaskCreate(BaseModel):
#     title: str
#     description: Optional[str] = None
#     priority: str = "medium"

# class TaskResponse(BaseModel):
#     id: str
#     title: str
#     description: Optional[str]
#     priority: str
#     completed: bool
#     created_at: str


# TODO: Create an in-memory task store
# tasks_db: dict = {}

# TODO: Create a dependency for the task store
# def get_task_store():
#     return tasks_db


# TODO: Implement routes
# POST /tasks - create a task (return 201)
# GET /tasks - list all tasks
# GET /tasks/{task_id} - get single task (404 if not found)
# DELETE /tasks/{task_id} - delete task (return 204)
