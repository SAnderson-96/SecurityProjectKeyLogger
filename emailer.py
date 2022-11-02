# https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
import smtplib

class Emailer:
    def __init__(self, email: str, password: str) -> None:
        '''Initializes the Emailer object with the email and application specific password.
        
        Parameters
        ---
        email: str
            The gmail account to sign into.
        password: str
            The application specific password used to login to the [email]
            
        Throws
        ---
        If the gmail servers can't be connected to or if the login isn't successful'''

        # Store the user login info and password
        self.gmail_user = email
        self.password = password

        # Connect to the gmail smtp server
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo() # Make connection
        self.server.login(self.gmail_user, self.password) # Login

    def send_email(self, recipients: object, subject: str, body: str) -> None:
        '''Sends an email from the arguments provided
        
        Parameters
        ---
        to: [list:str]
            The receiving email or list of emails.
            If to is None, the email will be sent to the same user that is sending it.
        subject: str
            The email's subject.
        body: str
            The body of the email.
        '''

        # Send email to send if the recipient isn't specified
        if recipients is None:
            recipients = self.gmail_user

        # Create the email text
        if type(recipients) == str:
            email_text = f"""From: {self.gmail_user}\nTo: {recipients}\nSubject: {subject}\n\n{body}"""
        else:
            email_text = f"""From: {self.gmail_user}\nTo: {", ".join(recipients)}\nSubject: {subject}\n\n{body}"""

        # Send the email
        self.server.sendmail(self.gmail_user, recipients, email_text)

    def __del__(self):
        # Close the server when the object is removed from memory
        self.server.close()
