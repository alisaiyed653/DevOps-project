from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Outlook SMTP server settings
outlook_smtp_server = 'smtp.office365.com'
outlook_smtp_port = 587

# Your Outlook email address and app password
outlook_email = 'kiloo.wiloo@hotmail.co.uk'
outlook_app_password = 'ambheta1'

print("outlook emai:", outlook_email)
print("outlook passowrd:", outlook_app_password)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    full_name = request.form['full_name']
    email = request.form['email']
    mobile_number = request.form['mobile_number']
    address = request.form['address']

    # Construct email message
    message = MIMEMultipart()
    message['From'] = outlook_email
    message['To'] = 'stone.choice.propertiesltd@gmail.com'
    message['Subject'] = 'New Contact Form Submission'

    body = f"Name: {full_name}\nEmail: {email}\nMobile Number: {mobile_number}\nAddress: {address}"
    message.attach(MIMEText(body, 'plain'))

    # Send email using Outlook SMTP server
    with smtplib.SMTP(outlook_smtp_server, outlook_smtp_port) as server:
        server.starttls()  # Enable TLS encryption
        server.login(outlook_email, outlook_app_password)

        # Send the email
        server.send_message(message)

    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
