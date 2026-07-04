import os
from datetime import datetime, timezone
from celery import Celery
from sqlalchemy.orm import Session

celery_app = Celery(
    "lead_followups",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)

celery_app.conf.beat_schedule = {
    "process-due-followups": {
        "task": "tasks.followup_sender.process_due_followups",
        "schedule": 3600.0,  # every hour
    }
}


@celery_app.task
def process_due_followups():
    from db import SessionLocal
    from models.db_models import FollowUp

    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        due = db.query(FollowUp).filter(
            FollowUp.status == "pending",
            FollowUp.scheduled_at <= now,
        ).all()

        sendgrid_key = os.getenv("SENDGRID_API_KEY", "")
        sent_count = 0

        for fu in due:
            if sendgrid_key:
                _send_via_sendgrid(fu, sendgrid_key)
            fu.status = "sent"
            fu.sent_at = now
            if fu.lead:
                fu.lead.stage = "contacted"
            sent_count += 1

        db.commit()
        return {"processed": sent_count}
    finally:
        db.close()


def _send_via_sendgrid(fu, api_key: str):
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        msg = Mail(
            from_email=os.getenv("SENDER_EMAIL", "noreply@example.com"),
            to_emails=fu.lead.email,
            subject=fu.subject,
            plain_text_content=fu.body,
        )
        sg.send(msg)
    except Exception:
        pass
