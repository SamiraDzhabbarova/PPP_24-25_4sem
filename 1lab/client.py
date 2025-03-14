import socket

# Функция для добавления программы
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

# Функция для запуска программы
def run_program(program_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send(f"RUN {program_name}".encode())
    response = client_socket.recv(1024).decode()
    print(response)
    client_socket.close()

# Функция для получения вывода программы
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

# Основной цикл клиента
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
            run_program(program_name)
        elif choice == "3":
            program_name = input("Введите имя программы: ")
            get_program_output(program_name)
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    client_main()
