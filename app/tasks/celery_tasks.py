# app/tasks/celery_tasks.py

import asyncio
from bson import ObjectId
from app.celery_worker import celery_app
from app.database import tasks_collection
from app.websocket.manager import manager
from app.email.mailer import send_task_completed_email


@celery_app.task
def process_task_celery(task_id, user_id, title, email):
    asyncio.run(_process(task_id, user_id, title, email))


async def _process(task_id, user_id, title, email):
    await asyncio.sleep(10)

    await tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": "completed"}}
    )

    await manager.send_personal_message(
        str(user_id),
        f"Task '{title}' completed"
    )

    send_task_completed_email(
        email=email,
        task_title=f"Your task '{title}' has been completed successfully."
    )
