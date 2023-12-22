import requests
import json
import threading
import time
import pyautogui


event_addr = "0x750e3394f4551dcf9d61b5152260ddf6c0cdf781064874bb27a66c330072d31d"
module_addr = "0x750e3394f4551dcf9d61b5152260ddf6c0cdf781064874bb27a66c330072d31d"
module_name = "DNuVModuleTest1"
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

def background():
    while True:
        for task in get_pending_tasks(complete_tasks=False):
            print(task)
        print('\n\n')
        time.sleep(5)

b = threading.Thread(name='background', target=background)
b.start()