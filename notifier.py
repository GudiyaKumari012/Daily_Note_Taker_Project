from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
from flask import Flask

app = Flask(__name__)

scheduler = APScheduler()

# Flask-Mail Configuration for Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'rohitpoddar937@gmail.com'  # Replace with your Gmail email address
app.config['MAIL_PASSWORD'] = 'rxyihergjzeasyrg'   # Replace with your Gmail app password

mail = Mail(app)


def index():
    try:
        print("Sending email...")
        msg = Message('Hello', sender='rohitpoddar937@gmail.com', recipients=['rohitpoddar_1@yahoo.com'])  # Replace with the recipient's email address
        msg.body = "Hello Flask message sent from Flask-Mail using Gmail"
        mail.send(msg)
        print("Email sent successfully.")
        return "Sent"
    except Exception as e:
        print(f"Error: {e}")
        return "Error occurred"

if __name__ == '__main__':
    # Use the correct variable name 'scheduler'
    scheduler.add_job(id='emailSender', func=index, trigger='interval', seconds=30)
    scheduler.start()
    app.run(debug=True)
