import requests
import json
import time
import asyncio
import websockets

BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/ws"

TOKEN = None
USERNAME = None

def register_user(username, password):
    global TOKEN
    data = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/sign-up/", json=data)
    if response.status_code == 200:
        print(f"Пользователь {username} зарегистрирован.")
        TOKEN = login_user(username, password)
        return True
    else:
        print(f"Ошибка регистрации: {response.text}")
        return False

def login_user(username, password):
    global TOKEN, USERNAME
    data = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/login/", data=data)
    if response.status_code == 200:
        TOKEN = response.json().get("access_token")
        USERNAME = username
        print(f"Успешный вход. Токен получен.")
        return TOKEN
    else:
        print(f"Ошибка авторизации: {response.text}")
        return None

def send_brutforce(hash_value, charset, max_length):
    if not TOKEN:
        print("Сначала авторизуйтесь.")
        return None

    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"hash": hash_value, "charset": charset, "max_length": max_length}
    response = requests.post(f"{BASE_URL}/brut_hash", json=data, headers=headers)
    if response.status_code == 200:
        task_id = response.json()["task_id"]
        print(f"Задача отправлена. Task ID: {task_id}")
        return task_id
    else:
        print(f"Ошибка отправки задачи: {response.text}")
        return None

def check_status(task_id, wait=False):
    if not TOKEN:
        print("Сначала авторизуйтесь.")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}
    while True:
        response = requests.get(f"{BASE_URL}/get_status?task_id={task_id}", headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(json.dumps(result, indent=2))
            if wait and result["status"].lower() in ["success", "completed", "failure"]:
                break
        else:
            print(f"Ошибка проверки статуса: {response.text}")
            break

        if not wait:
            break
        time.sleep(2)

async def listen_websocket():
    if not TOKEN:
        print("Сначала авторизуйтесь.")
        return

    uri = f"{WS_URL}?token={TOKEN}"
    try:
        async with websockets.connect(uri) as websocket:
            print("WebSocket подключён. Ожидаем уведомления...\n")
            while True:
                message = await websocket.recv()
                try:
                    data = json.loads(message)
                    print(f"WS сообщение: {json.dumps(data, indent=2)}\n")
                except json.JSONDecodeError:
                    print(f"Нераспознанное сообщение: {message}")
    except Exception as e:
        print(f"Ошибка WebSocket: {e}")

def start_websocket_listener():
    asyncio.run(listen_websocket())

def main():
    print("Консольный клиент")
    print("Доступные команды:")
    print("  register <username> <password>")
    print("  login <username> <password>")
    print("  brut <hash_value> <charset> <max_length>")
    print("  status <task_id>")
    print("  status_wait <task_id>")
    print("  exit")

    while True:
        command = input("> ").strip().split()
        if not command:
            continue

        cmd = command[0].lower()

        if cmd == "exit":
            print("Выход.")
            break
        elif cmd == "register" and len(command) == 3:
            register_user(command[1], command[2])
        elif cmd == "login" and len(command) == 3:
            login_user(command[1], command[2])
        elif cmd == "brut" and len(command) == 4:
            send_brutforce(command[1], command[2], int(command[3]))
        elif cmd == "status" and len(command) == 2:
            check_status(command[1])
        elif cmd == "status_wait" and len(command) == 2:
            check_status(command[1], wait=True)
        elif cmd == "ws":
            start_websocket_listener()
        else:
            print("Неизвестная команда. Попробуйте ещё раз.")

if __name__ == "__main__":
    main()
