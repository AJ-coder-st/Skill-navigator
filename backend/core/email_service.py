"""
Email service for sending reports, roadmaps, and milestone notifications
"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List
import json
from core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_host = getattr(settings, "SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = getattr(settings, "SMTP_PORT", 587)
        self.smtp_user = getattr(settings, "SMTP_USER", "")
        self.smtp_password = getattr(settings, "SMTP_PASSWORD", "")
        self.from_email = getattr(settings, "FROM_EMAIL", self.smtp_user)
        self.enabled = bool(self.smtp_user and self.smtp_password)
    
    async def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None):
        """Send an email"""
        if not self.enabled:
            print(f"[Email Service] Email sending disabled. Would send to {to_email}: {subject}")
            return False
        
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = to_email
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                use_tls=True,
            )
            print(f"[Email Service] Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"[Email Service] Failed to send email: {str(e)}")
            return False
    
    async def send_analysis_report(self, to_email: str, user_name: str, jd_result: Dict, profile_result: Dict, skill_gap_result: Dict):
        """Send skill gap analysis report"""
        subject = "Your Career Readiness Analysis Report"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
                .section {{ margin: 20px 0; padding: 15px; background: white; border-radius: 5px; }}
                .skill {{ display: inline-block; padding: 5px 10px; margin: 5px; background: #e3f2fd; border-radius: 3px; }}
                .missing {{ background: #ffebee; }}
                .strong {{ background: #e8f5e9; }}
                .partial {{ background: #fff3e0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 Career Readiness Analysis Report</h1>
                    <p>Hello {user_name},</p>
                </div>
                <div class="content">
                    <div class="section">
                        <h2>📋 Job Requirements</h2>
                        <p><strong>Role:</strong> {jd_result.get('role', 'N/A')}</p>
                        <p><strong>Experience Level:</strong> {jd_result.get('experience_level', 'N/A')}</p>
                        <p><strong>Required Skills:</strong></p>
                        <div>
                            {''.join([f'<span class="skill">{skill}</span>' for skill in jd_result.get('required_skills', [])[:10]])}
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>✅ Your Profile</h2>
                        <p><strong>Experience Level:</strong> {profile_result.get('experience_level', 'N/A')}</p>
                        {f'<p><strong>Summary:</strong> {profile_result.get("skill_summary", "")}</p>' if profile_result.get('skill_summary') else ''}
                    </div>
                    
                    <div class="section">
                        <h2>📊 Skill Gap Analysis</h2>
                        <p><strong>Missing Skills ({len(skill_gap_result.get('missing_skills', []))}):</strong></p>
                        <div>
                            {''.join([f'<span class="skill missing">{item.get("skill", item) if isinstance(item, dict) else item}</span>' for item in skill_gap_result.get('missing_skills', [])[:10]])}
                        </div>
                        <p><strong>Strong Skills ({len(skill_gap_result.get('strong_skills', []))}):</strong></p>
                        <div>
                            {''.join([f'<span class="skill strong">{item.get("skill", item) if isinstance(item, dict) else item}</span>' for item in skill_gap_result.get('strong_skills', [])[:10]])}
                        </div>
                    </div>
                    
                    {f'<div class="section"><h2>💡 AI Recommendations</h2><p>{skill_gap_result.get("reasoning", "")[:500]}</p></div>' if skill_gap_result.get('reasoning') else ''}
                    
                    <div class="section">
                        <p><strong>Next Steps:</strong></p>
                        <ul>
                            <li>Focus on learning the missing skills</li>
                            <li>Check your personalized roadmap</li>
                            <li>Practice with recommended exercises</li>
                        </ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
Career Readiness Analysis Report

Hello {user_name},

Job Requirements:
Role: {jd_result.get('role', 'N/A')}
Experience Level: {jd_result.get('experience_level', 'N/A')}
Required Skills: {', '.join(jd_result.get('required_skills', [])[:10])}

Your Profile:
Experience Level: {profile_result.get('experience_level', 'N/A')}

Skill Gap Analysis:
Missing Skills: {len(skill_gap_result.get('missing_skills', []))}
Strong Skills: {len(skill_gap_result.get('strong_skills', []))}

Visit the app to see your complete analysis and personalized roadmap.
        """
        
        return await self.send_email(to_email, subject, html_content, text_content)
    
    async def send_roadmap(self, to_email: str, user_name: str, roadmap: Dict):
        """Send learning roadmap"""
        subject = "Your Personalized Learning Roadmap"
        
        milestones = roadmap.get('milestones', [])
        milestones_html = ""
        for i, milestone in enumerate(milestones, 1):
            milestones_html += f"""
            <div style="margin: 15px 0; padding: 15px; background: white; border-left: 4px solid #667eea; border-radius: 5px;">
                <h3>Week {i}: {milestone.get('title', f'Milestone {i}')}</h3>
                <p><strong>Focus:</strong> {milestone.get('focus', 'N/A')}</p>
                <p><strong>Skills:</strong> {', '.join(milestone.get('skills', []))}</p>
            </div>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🗺️ Your Learning Roadmap</h1>
                    <p>Hello {user_name},</p>
                </div>
                <div class="content">
                    <p>Here's your personalized {roadmap.get('duration_weeks', 8)}-week learning roadmap:</p>
                    {milestones_html}
                    <p style="margin-top: 20px;"><strong>Total Duration:</strong> {roadmap.get('duration_weeks', 8)} weeks</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_milestone_notification(self, to_email: str, user_name: str, milestone: Dict, milestone_number: int):
        """Send milestone completion notification"""
        subject = f"🎉 Milestone {milestone_number} Completed!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Congratulations!</h1>
                    <p>Hello {user_name},</p>
                </div>
                <div class="content">
                    <p>You've successfully completed <strong>Milestone {milestone_number}</strong>!</p>
                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h3>{milestone.get('title', f'Milestone {milestone_number}')}</h3>
                        <p><strong>Focus:</strong> {milestone.get('focus', 'N/A')}</p>
                        <p>Great job! Keep up the excellent work on your learning journey.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

email_service = EmailService()
