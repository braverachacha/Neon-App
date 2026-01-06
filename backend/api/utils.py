from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app
from . import mail

def generate_email_token(email):
  serializer= URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
  return serializer.dumps(email, salt='email-confirm')
  
def send_email_verification(email, link):
  msg = Message(
    subject='Verify your Neon App email',
    recipients=[email],
    html=f'''
    <p>Click to verify your registed Neon App email</p>
    <a href="{link}">Verify Email</a>
    <p>Verification link expires in 15 minutes</p>
    {link}
    '''
    )
  mail.send(msg)