from flask_mail import Mail, Message



class Mailer(object):
    def __init__(self, app):
        self.app = app
        self.app.config.update(mail_settings)

    def mail_this(self, email):
        mail = Mail(self.app)
        msg = Message(subject = "Your book is due soon.",
                      sender = self.app.config.get("MAIL_USERNAME"),
                      recipients = [email],  # need a way to find the emails...but her emails.....
                      body = "Your book is due soon")
        mail.send(msg)