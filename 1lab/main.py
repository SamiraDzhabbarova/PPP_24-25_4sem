import os
import time
import json
import socket
import sys
from threading import Thread

FORBIDDEN_SYMBOLS = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
NOT_FILES = ["server.py", "client.py", "main.py"]


def create_program_directory(program_name):
    if not os.path.exists(program_name):
        os.makedirs(program_name)

def run_program(program_name):
    output_file = os.path.join(program_name, f"{program_name}_output.txt")
    command = f"python {program_name}.py > {output_file} 2>&1"
    os.system(command)

def load_programs_info():
    if os.path.exists("programs_info.json"):
        with open("programs_info.json", "r") as file:
            return json.load(file)
    return {}

def save_programs_info(programs_info):
    with open("programs_info.json", "w") as file:
        json.dump(programs_info, file, indent=4)

def is_program_name_valid(program_name):
    for symbol in FORBIDDEN_SYMBOLS:
        if symbol in program_name:
            return False
    return True

def scan_for_programs(programs_info):
    for item in os.listdir():
        if item.endswith(".py") and os.path.isfile(item) and item not in NOT_FILES:
            program_name = item[:-3]
            if program_name not in programs_info:
                programs_info[program_name] = {"runs": []}
                create_program_directory(program_name)
                print(f"Найдена программа: {program_name}")
    return programs_info

def remove_deleted_programs(programs_info):
    programs_to_remove = []
    for program_name in programs_info:
        if not os.path.exists(f"{program_name}.py"):
            programs_to_remove.append(program_name)
            print(f"Программа {program_name} удалена и больше не будет запускаться.")
    
    for program_name in programs_to_remove:
        del programs_info[program_name]
    return programs_info

def run_programs_cyclically(programs_info):
    while True:
        programs_info = remove_deleted_programs(programs_info)
        save_programs_info(programs_info)

        for program_name in list(programs_info.keys()):
            print(f"Запуск программы: {program_name}")
            run_program(program_name)
            programs_info[program_name]["runs"].append(time.strftime("%Y-%m-%d %H:%M:%S"))
            save_programs_info(programs_info)
        time.sleep(10)


def server_main():
    programs_info = load_programs_info()

    programs_info = scan_for_programs(programs_info)
    save_programs_info(programs_info)

    cycler_thread = Thread(target=run_programs_cyclically, args=(programs_info,))
    cycler_thread.daemon = True
    cycler_thread.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Сервер запущен и ожидает подключений...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключение установлено: {addr}")
        command = client_socket.recv(1024).decode()

        if command.startswith("ADD"):
            program_name = command.split()[1]
            if program_name in programs_info:
                client_socket.send(f"Программа {program_name} уже существует.".encode())
            elif not is_program_name_valid(program_name):
                client_socket.send(f"Некорректное имя программы: {program_name}.".encode())
            else:
                client_socket.send("Ожидание кода программы...".encode())
                program_code = client_socket.recv(1024).decode()

                create_program_directory(program_name)
                with open(f"{program_name}.py", "w") as file:
                    file.write(program_code)

                programs_info[program_name] = {"runs": []}
                save_programs_info(programs_info)
                client_socket.send(f"Программа {program_name} добавлена.".encode())

        elif command.startswith("RUN"):
            program_name = command.split()[1]
            if program_name in programs_info:
                run_program(program_name)
                programs_info[program_name]["runs"].append(time.strftime("%Y-%m-%d %H:%M:%S"))
                save_programs_info(programs_info)
                client_socket.send(f"Программа {program_name} запущена.".encode())
            else:
                client_socket.send(f"Программа {program_name} не найдена.".encode())

        elif command.startswith("GET"):
            program_name = command.split()[1]
            if program_name in programs_info:
                output_file = os.path.join(program_name, f"{program_name}_output.txt")
                if os.path.exists(output_file):
                    with open(output_file, "rb") as file:
                        client_socket.sendfile(file)
                else:
                    client_socket.send("Файл с выводом не найден.".encode())
            else:
                client_socket.send(f"Программа {program_name} не найдена.".encode())

        client_socket.close()

def add_program(program_name, program_code):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Подключение к серверу
    client_socket.send(f"ADD {program_name}".encode())
    response = client_socket.recv(1024).decode()
    if response == "Ожидание кода программы...":
        client_socket.send(program_code.encode())
        response = client_socket.recv(1024).decode()
    print(response)
    client_socket.close()

def run_programc(program_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send(f"RUN {program_name}".encode())
    response = client_socket.recv(1024).decode()
    print(response)
    client_socket.close()

def get_program_output(program_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send(f"GET {program_name}".encode())
    with open(f"{program_name}_output.txt", "wb") as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
    client_socket.close()
    print(f"Вывод программы {program_name} сохранён в файл {program_name}_output.txt")

def client_main():
    while True:
        print("\n1. Добавить программу")
        print("2. Запустить программу")
        print("3. Получить вывод программы")
        print("4. Выйти")
        choice = input("Выберите опцию: ")

        if choice == "1":
            program_name = input("Введите имя программы: ")
            print("Введите код программы (завершите пустой строкой):")
            program_code = ""
            while True:
                line = input()
                if line == "":
                    break
                program_code += line + "\n"
            add_program(program_name, program_code)
        elif choice == "2":
            program_name = input("Введите имя программы: ")
            run_programc(program_name)
        elif choice == "3":
            program_name = input("Введите имя программы: ")
            get_program_output(program_name)
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    server_thread = Thread(target=server_main)
    server_thread.daemon = True
    server_thread.start()

    client_main()
