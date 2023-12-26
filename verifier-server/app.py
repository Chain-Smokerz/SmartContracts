import requests
import json
import threading
import time
import pyautogui
from sc_interact import *
import random
import asyncio
import module_metadata


event_addr = module_metadata.event_addr
module_addr = module_metadata.module_addr
module_name = module_metadata.module_name
module = f"{module_addr}::{module_name}::VerificationPool"
event_field = "task_event"
track_file = "track.json"

url = "https://fullnode.devnet.aptoslabs.com/"
path = f"v1/accounts/{event_addr}/events/{module}/{event_field}"
headers = {
    "Content-Type": "application/json"
}

def get_pending_tasks(complete_tasks=False):
    next_index = json.load(open(track_file, "r"))['next_index']
    params = {
        "start": next_index
    }
    
    response = requests.get(url + path, params=params, headers=headers)
    tasks = [_['data'] for _ in response.json()]
    
    if complete_tasks:
        next_index += len(response.json())
        with open(track_file, 'w') as f:
            json.dump({"next_index": next_index}, f, indent=4)
    
    return tasks

def send_secret(phone, secret):
    my_coord = [1059, 456]
    message_box_coord = [1572, 1019]
    send_button_coord = [1640, 1021]
    link_coord = [1465, 948]

    pyautogui.click(message_box_coord[0], message_box_coord[1])
    time.sleep(1)
    pyautogui.write(f"https://wa.me/{phone}?text={secret}")
    pyautogui.click(send_button_coord[0], send_button_coord[1])
    time.sleep(1)
    pyautogui.click(link_coord[0], link_coord[1])
    time.sleep(2)
    pyautogui.click(send_button_coord[0], send_button_coord[1])
    time.sleep(1)
    pyautogui.click(my_coord[0], my_coord[1])

while True:
    for task in get_pending_tasks(complete_tasks=True):
        phone = task['phone']
        user = task['user']
        print(f"\nPhone: {phone}\nUser: {user}\n")

        otp = str(random.randint(100000, 999999))
        tx_hash = asyncio.run(push_otp(user, otp))
        print(f"tx_hash: {tx_hash}")
        print(f"otp: {otp}")
        send_secret(phone, otp)
    print('\n\n')
    time.sleep(10)
