
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from bson import ObjectId
import asyncio

from app.websocket.manager import manager
from app.tasks.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.tasks.services import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task
)
from app.core.dependencies import get_current_user
from app.database import tasks_collection
from app.tasks.celery_tasks import process_task_celery


router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Background task
async def process_task(task_id: str, user_id: str, title: str):
    try:
        await asyncio.sleep(10)

        await tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": "completed"}}
        )

        await manager.send_personal_message(
            str(user_id),
            f"Task '{title}' completed"
        )

    except Exception as e:
        print("Background Task Error:", e)


# Create Task
@router.post("/", response_model=TaskResponse)
async def create_new_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    try:
        task_data = task.dict()
        task_data["user_id"] = ObjectId(current_user["id"])

        new_task = await create_task(task_data)
        if not new_task:
            raise HTTPException(status_code=500, detail="Task creation failed")

        
        # background task call
        background_tasks.add_task(
            process_task,
            new_task["id"],
            current_user["id"],
            new_task["title"]
        )
        
        
        # Celery task call
        # process_task_celery.delay(
        #     new_task["id"],
        #     current_user["id"],
        #     new_task["title"],
        #     current_user["email"]
        # )
        
        return new_task

    except HTTPException:
        raise
    except Exception as e:
        print("Create Task API Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


# Get all tasks
@router.get("/", response_model=list[TaskResponse])
async def get_tasks_api(current_user: dict = Depends(get_current_user)):
    try:
        return await get_tasks(
            role=current_user["role"],
            user_id=current_user["id"]
        )
    except Exception as e:
        print("Get Tasks API Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


# Get single task
@router.get("/{task_id}", response_model=TaskResponse)
async def get_single_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        task = await get_task(
            task_id,
            role=current_user["role"],
            user_id=current_user["id"]
        )

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task

    except HTTPException:
        raise
    except Exception as e:
        print("Get Single Task API Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


# Update task
@router.put("/{task_id}")
async def update_task_api(
    task_id: str,
    task: TaskUpdate,
    current_user: dict = Depends(get_current_user)
):
    try:
        updated = await update_task(
            task_id=task_id,
            role=current_user["role"],
            user_id=current_user["id"],
            update_data={k: v for k, v in task.dict().items() if v is not None}
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"message": "Task updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        print("Update Task API Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


# Delete task
@router.delete("/{task_id}")
async def delete_task_api(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        deleted = await delete_task(
            task_id=task_id,
            role=current_user["role"],
            user_id=current_user["id"]
        )

        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"message": "Task deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        print("Delete Task API Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
