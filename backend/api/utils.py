from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app
import secrets
from . import mail


def generate_email_token(email=None):
    """Generate a secure random token for email verification"""
    return secrets.token_urlsafe(32)
  
def send_email_verification(email, link, username):
    msg = Message(
        subject='Verify Your Neon App Email',
        recipients=[email]
    )
    
    msg.html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0a0e27;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #0a0e27; padding: 40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #0f1428; border-radius: 15px; overflow: hidden; border: 1px solid #00d9ff; box-shadow: 0 0 40px rgba(0, 217, 255, 0.2);">
                        
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #1a1f3a 0%, #0f1428 100%); padding: 40px 30px; text-align: center; border-bottom: 2px solid #00d9ff;">
                                <h1 style="margin: 0; color: #00d9ff; font-size: 32px; text-shadow: 0 0 20px #00d9ff, 0 0 40px #00d9ff;">
                                    ⚡ NEON APP
                                </h1>
                                <p style="margin: 10px 0 0 0; color: #b8c5d6; font-size: 14px; letter-spacing: 2px;">
                                    EMAIL VERIFICATION
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="margin: 0 0 20px 0; color: #00ff88; font-size: 24px; text-shadow: 0 0 15px #00ff88;">
                                    <span>Hello {username}</span>Welcome to Neon App! 🎉
                                </h2>
                                
                                <p style="margin: 0 0 25px 0; color: #b8c5d6; font-size: 16px; line-height: 1.6;">
                                    Thank you for signing up! We're excited to have you on board. 
                                    To get started, please verify your email address by clicking the button below.
                                </p>
                                
                                <!-- Button -->
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td align="center" style="padding: 20px 0;">
                                            <a href="{link}" style="display: inline-block; background: #00d9ff; color: #0a0e27; 
                                                   padding: 15px 40px; text-decoration: none; border-radius: 8px; 
                                                   font-weight: bold; font-size: 16px; text-transform: uppercase; 
                                                   letter-spacing: 1px; box-shadow: 0 0 25px rgba(0, 217, 255, 0.6), 
                                                   0 5px 15px rgba(0, 0, 0, 0.3);">
                                                ✓ VERIFY EMAIL
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Warning Box -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 30px;">
                                    <tr>
                                        <td style="background: rgba(255, 0, 102, 0.1); border-left: 4px solid #ff0066; 
                                                   padding: 15px 20px; border-radius: 5px;">
                                            <p style="margin: 0; color: #ff6699; font-size: 14px;">
                                                ⏱️ <strong>Important:</strong> This verification link will expire in <strong>15 minutes</strong>.
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Alternative Link -->
                                <p style="margin: 25px 0 0 0; color: #6b7c8f; font-size: 13px; line-height: 1.6;">
                                    If the button doesn't work, copy and paste this link into your browser:
                                </p>
                                <p style="margin: 10px 0 0 0; padding: 10px; background: rgba(0, 217, 255, 0.05); 
                                          border-radius: 5px; border: 1px solid rgba(0, 217, 255, 0.2);">
                                    <a href="{link}" style="color: #00d9ff; text-decoration: none; word-break: break-all; font-size: 12px;">
                                        {link}
                                    </a>
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background: #0a0e27; padding: 30px; text-align: center; border-top: 1px solid rgba(0, 217, 255, 0.2);">
                                <p style="margin: 0 0 10px 0; color: #6b7c8f; font-size: 13px;">
                                    Didn't request this email? You can safely ignore it.
                                </p>
                                <p style="margin: 10px 0 0 0; color: #4a5568; font-size: 12px;">
                                    © 2026 Neon App. All rights reserved.
                                </p>
                            </td>
                        </tr>
                        
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    mail.send(msg)
    
    
def send_password_reset_email(to_email, reset_link):
    msg = Message(
        'Reset Your Password',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[to_email]
    )
    
    msg.html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #0a0e27; color: #b8c5d6; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #0f1428; border-radius: 10px; padding: 30px; border: 1px solid #00d9ff;">
                <h1 style="color: #00d9ff; text-shadow: 0 0 10px #00d9ff;">Reset Your Password</h1>
                <p>You requested to reset your password. Click the button below to set a new password:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" 
                       style="background: #00d9ff; color: #0a0e27; padding: 12px 30px; text-decoration: none; 
                              border-radius: 5px; font-weight: bold; display: inline-block;
                              box-shadow: 0 0 20px rgba(0, 217, 255, 0.5);">
                        Reset Password
                    </a>
                </div>
                <p style="color: #ff0066;">This link will expire in 15 minutes.</p>
                <p style="font-size: 12px; color: #6b7280; margin-top: 20px;">
                    If you didn't request this, please ignore this email.
                </p>
            </div>
        </body>
    </html>
    """
    
    mail.send(msg)