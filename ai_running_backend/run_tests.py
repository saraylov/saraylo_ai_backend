#!/usr/bin/env python3
"""
Скрипт для запуска всех тестов системы
"""

import unittest
import sys
import os

def run_all_tests():
    """Запуск всех тестов"""
    # Добавляем путь к корню проекта
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Создаем тестовый набор
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем все тесты
    suite.addTests(loader.discover('tests', pattern='test_*.py'))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Возвращаем код завершения
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)