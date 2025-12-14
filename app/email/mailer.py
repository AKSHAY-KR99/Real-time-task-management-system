from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import MAIL_FROM, MAIL_PASSWORD, MAIL_USERNAME, MAIL_SERVER, MAIL_PORT 

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_PORT=MAIL_PORT,
    MAIL_STARTTLS=True, 
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

async def send_task_completed_email(email: str, task_title: str):
    message = MessageSchema(
        subject="Task Completed",
        recipients=[email],
        body=f"Your task '{task_title}' has been completed successfully.",
        subtype="plain",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
