from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.tasks.router import router as task_router
from app.websocket.router import router as websocket_router

app = FastAPI(title="Real-Time Task Processing System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routes
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(websocket_router)



# Health endpoint
@app.get("/health")
async def health_check():
    from app.database import db
    server_info = await db.command("ping")
    return {
        "status": "ok",
        "message": "FastAPI server and MongoDB are running",
        "mongo": server_info
    }
