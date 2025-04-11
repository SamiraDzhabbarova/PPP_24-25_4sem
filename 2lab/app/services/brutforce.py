import uuid
import itertools
import os
from typing import Dict, Optional
from fastapi import HTTPException
import time
import threading

# Хранилище задач (в памяти)
tasks: Dict[str, dict] = {}

# Функция для генерации всех возможных паролей
def generate_passwords(charset: str, max_length: int, output_file: str):
    with open(output_file, "w", encoding="utf-8") as f:
        for length in range(1, max_length + 1):
            for combination in itertools.product(charset, repeat=length):
                password = "".join(combination)
                f.write(password + "\n")

# Эмуляция проверки хеша (в реальном проекте здесь будет hashcat или другой инструмент)
def check_hash(hash_value: str, password: str) -> bool:

    return password == "pass123"

# Функция для выполнения брутфорс-атаки
def brutforce_task(task_id: str, hash_value: str, charset: str, max_length: int):
    try:
        # Обновляем статус задачи
        tasks[task_id]["status"] = "running"
        tasks[task_id]["progress"] = 0
        tasks[task_id]["result"] = None

        # Генерируем файл с паролями
        output_file = f"passwords_{task_id}.txt"
        generate_passwords(charset, max_length, output_file)

        # Подсчитаем общее количество паролей для прогресса
        total_passwords = sum(len(charset) ** i for i in range(1, max_length + 1))
        checked_passwords = 0

        # Читаем пароли из файла и проверяем
        with open(output_file, "r", encoding="utf-8") as f:
            for password in f:
                password = password.strip()
                checked_passwords += 1

                # Обновляем прогресс
                progress = int((checked_passwords / total_passwords) * 100)
                tasks[task_id]["progress"] = progress

                # Проверяем пароль
                if check_hash(hash_value, password):
                    tasks[task_id]["status"] = "completed"
                    tasks[task_id]["result"] = password
                    break

        # Если пароль не найден
        if tasks[task_id]["status"] != "completed":
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["result"] = None

        # Удаляем временный файл
        if os.path.exists(output_file):
            os.remove(output_file)

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["result"] = None
        tasks[task_id]["progress"] = 0
        print(f"Error in task {task_id}: {str(e)}")

# Функция для запуска задачи брутфорса
def start_brutforce(hash_value: str, charset: str, max_length: int) -> str:
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "pending",
        "progress": 0,
        "result": None
    }

    # Запускаем задачу в отдельном потоке
    thread = threading.Thread(
        target=brutforce_task,
        args=(task_id, hash_value, charset, max_length)
    )
    thread.start()

    return task_id

# Функция для получения статуса задачи
def get_task_status(task_id: str) -> dict:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]
