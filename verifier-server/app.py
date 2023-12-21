import requests
import json


event_addr = "0x750e3394f4551dcf9d61b5152260ddf6c0cdf781064874bb27a66c330072d31d"
module_addr = "0x750e3394f4551dcf9d61b5152260ddf6c0cdf781064874bb27a66c330072d31d"
module_name = "DNuVModuleTest"
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

for task in get_pending_tasks(complete_tasks=False):
    print(task)
