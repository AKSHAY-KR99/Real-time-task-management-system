
from datetime import datetime
from bson import ObjectId
from app.database import tasks_collection


# Create task
async def create_task(task_data: dict):
    try:
        task_data["created_at"] = datetime.utcnow()
        task_data["status"] = "pending"

        result = await tasks_collection.insert_one(task_data)
        task_data["id"] = str(result.inserted_id)
        return task_data

    except Exception as e:
        print("Create Task Error:", e)
        return None


# Get tasks
async def get_tasks(role: str, user_id: str):
    try:
        query = {} if role == "admin" else {"user_id": ObjectId(user_id)}
        cursor = tasks_collection.find(query)

        tasks = []
        async for task in cursor:
            task["id"] = str(task["_id"])
            task["user_id"] = str(task["user_id"])
            del task["_id"]
            tasks.append(task)

        return tasks

    except Exception as e:
        print("Get Tasks Error:", e)
        return []


# Get single task
async def get_task(task_id: str, role: str, user_id: str):
    try:
        query = {"_id": ObjectId(task_id)}

        if role != "admin":
            query["user_id"] = ObjectId(user_id)

        task = await tasks_collection.find_one(query)
        if not task:
            return None

        task["id"] = str(task["_id"])
        task["user_id"] = str(task["user_id"])
        del task["_id"]
        return task

    except Exception as e:
        print("Get Task Error:", e)
        return None


# Update task
async def update_task(task_id: str, role: str, user_id: str, update_data: dict):
    try:
        query = {"_id": ObjectId(task_id)}

        if role != "admin":
            query["user_id"] = ObjectId(user_id)

        result = await tasks_collection.update_one(query, {"$set": update_data})
        return result.matched_count > 0

    except Exception as e:
        print("Update Task Error:", e)
        return False


# Delete task
async def delete_task(task_id: str, role: str, user_id: str):
    try:
        query = {"_id": ObjectId(task_id)}

        if role != "admin":
            query["user_id"] = ObjectId(user_id)

        result = await tasks_collection.delete_one(query)
        return result.deleted_count == 1

    except Exception as e:
        print("Delete Task Error:", e)
        return False
