import os
import logging
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///users.db")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


from api.models import User
LOG_FILE = os.getenv("LOG_FILE", "/tmp/token_cleanup.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


# Cleanup logic

def cleanup_tokens():
    now = datetime.utcnow()

    # Expired email verification tokens (unverified users)
    expired_verify_users = User.query.filter(
        User.email_token_expiry.isnot(None),
        User.email_token_expiry < now,
        User.is_verified == False
    ).all()

    for user in expired_verify_users:
        user.email_token = None
        user.email_token_expiry = None

    # Expired password reset tokens (unused)
    expired_reset_users = User.query.filter(
        User.reset_token_expiry.isnot(None),
        User.reset_token_expiry < now,
        User.reset_token_used == False
    ).all()

    for user in expired_reset_users:
        user.reset_token = None
        user.reset_token_expiry = None
        user.reset_token_used = True

    db.session.commit()

    message = (
        f"Cleaned {len(expired_verify_users)} expired email tokens "
        f"and {len(expired_reset_users)} expired reset tokens"
    )

    logging.info(message)
    print(message)


if __name__ == "__main__":
    with app.app_context():
        cleanup_tokens()