import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

EMAIL_SENDER    = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD  = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECEIVER  = os.getenv("EMAIL_RECEIVER", "")
SMTP_HOST       = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT       = int(os.getenv("EMAIL_SMTP_PORT", 587))

SEVERITY_EMOJI = {
    "critical": "🚨",
    "high":     "🔴",
    "medium":   "🟡",
    "low":      "🟢"
}

HEAL_EMOJI = {
    "healed":      "✅",
    "heal_failed": "❌",
    "skipped":     "⚠️",
    "idle":        "💤"
}


def build_email_html(
    dashboard_name: str,
    health_status: str,
    heal_status: str,
    root_cause: str,
    affected_dbt_model: str,
    confidence_score: float,
    severity: str,
    fix_recommendation: str
) -> str:
    """Builds a clean HTML email body."""
    sev_emoji  = SEVERITY_EMOJI.get(severity, "🔴")
    heal_emoji = HEAL_EMOJI.get(heal_status, "❓")
    timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S CDT")

    # Format fix as HTML list if it's a list
    if isinstance(fix_recommendation, list):
        fix_html = "<ol>" + "".join(f"<li>{f}</li>" for f in fix_recommendation) + "</ol>"
    else:
        fix_html = f"<p>{fix_recommendation or 'See logs for details'}</p>"

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 700px; margin: auto; padding: 20px;">

        <div style="background:#1a1a2e; color:white; padding:20px; border-radius:8px 8px 0 0;">
            <h2 style="margin:0">{sev_emoji} BI Platform Alert — {dashboard_name}</h2>
            <p style="margin:5px 0; font-size:13px; color:#aaa;">🕐 {timestamp}</p>
        </div>

        <div style="border: 1px solid #ddd; border-top: none; padding: 20px; border-radius: 0 0 8px 8px;">

            <table width="100%" cellpadding="10" style="border-collapse:collapse;">
                <tr style="background:#f5f5f5;">
                    <td><strong>Health Status</strong></td>
                    <td><span style="color:{'red' if health_status == 'failed' else 'orange'}; font-weight:bold;">
                        {health_status.upper()}</span></td>
                </tr>
                <tr>
                    <td><strong>Heal Status</strong></td>
                    <td>{heal_emoji} {heal_status.upper()}</td>
                </tr>
                <tr style="background:#f5f5f5;">
                    <td><strong>Severity</strong></td>
                    <td>{sev_emoji} {severity.upper()}</td>
                </tr>
                <tr>
                    <td><strong>Confidence</strong></td>
                    <td>{confidence_score:.0%}</td>
                </tr>
                <tr style="background:#f5f5f5;">
                    <td><strong>dbt Model Rebuilt</strong></td>
                    <td><code style="background:#eee; padding:2px 6px; border-radius:4px;">
                        {affected_dbt_model or 'N/A'}</code></td>
                </tr>
            </table>

            <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">

            <h3 style="color:#333;">🧠 Root Cause Analysis</h3>
            <p style="background:#fff8e1; padding:12px; border-left:4px solid #f0a500;
                       border-radius:4px; color:#555;">
                {root_cause}
            </p>

            <h3 style="color:#333;">🔧 Fix Recommendation</h3>
            <div style="background:#e8f5e9; padding:12px; border-left:4px solid #4caf50;
                        border-radius:4px; color:#444;">
                {fix_html}
            </div>

            <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">

            <p style="font-size:12px; color:#999; text-align:center;">
                🤖 Sent by <strong>Real-Time Agentic BI Platform</strong> — Self-Healing Dashboards
            </p>
        </div>
    </body>
    </html>
    """


def send_email_notification(
    dashboard_name: str,
    health_status: str,
    heal_status: str,
    root_cause: str,
    affected_dbt_model: str,
    confidence_score: float,
    severity: str = "high",
    fix_recommendation: str = ""
) -> dict:
    """
    Sends HTML email alert via Gmail SMTP.
    Falls back to mock if credentials not configured.
    """
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        return mock_email_notify(dashboard_name, health_status, heal_status)

    sev_emoji = SEVERITY_EMOJI.get(severity, "🔴")
    subject   = (
        f"{sev_emoji} [{severity.upper()}] BI Alert: "
        f"{dashboard_name} — {health_status.upper()} | Heal: {heal_status.upper()}"
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECEIVER

    html_body = build_email_html(
        dashboard_name, health_status, heal_status,
        root_cause, affected_dbt_model, confidence_score,
        severity, fix_recommendation
    )
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        return {"success": True, "message": f"Email sent to {EMAIL_RECEIVER}"}

    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "message": "SMTP Auth failed — check EMAIL_PASSWORD (use App Password, not Gmail password)"
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


def mock_email_notify(
    dashboard_name: str,
    health_status: str,
    heal_status: str
) -> dict:
    print(
        f"           [MOCK EMAIL] 📧 Notification sent for {dashboard_name} "
        f"| Status: {health_status} | Heal: {heal_status}"
    )
    return {"success": True, "message": "mock"}