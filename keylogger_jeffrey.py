import keyboard
from email.message import EmailMessage

def handle_key_press(event):
    if event.event_type == "down":
        print(event.name)
keyboard.hook(handle_key_press)

