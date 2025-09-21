#!/usr/bin/env python3
"""
Скрипт для запуска разработческого окружения
Запускает одновременно бэкенд (Flask) и фронтенд (Vite)
"""

import subprocess
import sys
import os
import signal

# Глобальные переменные для процессов
backend_process = None
frontend_process = None

def signal_handler(sig, frame):
    """Обработчик сигналов для корректного завершения процессов"""
    print("\nЗавершение работы...")
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()
    sys.exit(0)

def run_backend():
    """Запуск бэкенда (Flask)"""
    global backend_process
    try:
        print("Запуск бэкенда (Flask)...")
        backend_process = subprocess.Popen([
            sys.executable, 
            "api/workout_api.py"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        print("Бэкенд запущен на http://localhost:5000")
    except Exception as e:
        print(f"Ошибка запуска бэкенда: {e}")
        return False
    return True

def run_frontend():
    """Запуск фронтенда (Vite)"""
    global frontend_process
    try:
        print("Запуск фронтенда (Vite)...")
        frontend_process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui"))
        print("Фронтенд запущен на http://localhost:3000")
    except Exception as e:
        print(f"Ошибка запуска фронтенда: {e}")
        return False
    return True

def main():
    """Основная функция"""
    # Регистрация обработчика сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Запуск разработческого окружения SARAYLO AI Workout System")
    print("=" * 60)
    
    # Проверка наличия необходимых файлов
    if not os.path.exists("api/workout_api.py"):
        print("Ошибка: Не найден файл api/workout_api.py")
        return 1
    
    if not os.path.exists("gui/package.json"):
        print("Ошибка: Не найден файл gui/package.json")
        return 1
    
    # Запуск сервисов
    if not run_backend():
        return 1
    
    if not run_frontend():
        # Останавливаем бэкенд, если не удалось запустить фронтенд
        if backend_process:
            backend_process.terminate()
        return 1
    
    print("\n" + "=" * 60)
    print("Разработческое окружение запущено успешно!")
    print("Бэкенд:  http://localhost:5000")
    print("Фронтенд: http://localhost:3000")
    print("Нажмите Ctrl+C для остановки")
    print("=" * 60)
    
    # Ожидание завершения процессов
    try:
        # Ждем завершения одного из процессов
        while True:
            if backend_process and backend_process.poll() is not None:
                print("Бэкенд процесс завершен")
                break
            if frontend_process and frontend_process.poll() is not None:
                print("Фронтенд процесс завершен")
                break
    except KeyboardInterrupt:
        pass
    finally:
        signal_handler(None, None)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())