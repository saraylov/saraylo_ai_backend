import unittest
import sys
import os
import json
import redis
from datetime import datetime
from unittest.mock import Mock, patch

# Добавляем путь к корню проекта для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sessions.session_manager import SessionManager

class TestSessionManager(unittest.TestCase):
    """Тесты для менеджера сессий"""
    
    def setUp(self):
        """Подготовка к тестированию"""
        # Создаем mock для Redis клиента
        self.mock_redis = Mock()
        self.session_manager = SessionManager(self.mock_redis, session_ttl=3600)
        
        # Тестовые данные сессии
        self.session_id = "test_session_123"
        self.session_data = {
            'user_id': 'test_user',
            'calibration_data': {'10%': 3.2, '20%': 4.1},
            'user_profile': {
                'age': 28,
                'gender': 'male',
                'weight_kg': 70,
                'height_cm': 175,
                'fitness_level': 2
            }
        }
        
    def test_create_session(self):
        """Тест создания сессии"""
        # Настраиваем mock для успешного создания сессии
        self.mock_redis.setex.return_value = True
        
        result = self.session_manager.create_session(self.session_id, self.session_data)
        
        # Проверяем, что метод вернул True
        self.assertTrue(result)
        
        # Проверяем, что был вызван метод setex с правильными аргументами
        self.mock_redis.setex.assert_called_once()
        
    def test_get_session(self):
        """Тест получения данных сессии"""
        # Настраиваем mock для возврата данных сессии
        session_data_with_timestamp = self.session_data.copy()
        session_data_with_timestamp['created_at'] = datetime.utcnow().isoformat()
        self.mock_redis.get.return_value = json.dumps(session_data_with_timestamp)
        
        result = self.session_manager.get_session(self.session_id)
        
        # Проверяем, что метод вернул правильные данные
        self.assertIsNotNone(result)
        if result is not None:
            self.assertEqual(result['user_id'], 'test_user')
            self.assertIn('created_at', result)
        
    def test_get_nonexistent_session(self):
        """Тест получения несуществующей сессии"""
        # Настраиваем mock для возврата None
        self.mock_redis.get.return_value = None
        
        result = self.session_manager.get_session(self.session_id)
        
        # Проверяем, что метод вернул None
        self.assertIsNone(result)
        
    def test_update_session(self):
        """Тест обновления данных сессии"""
        # Настраиваем mock для успешного обновления сессии
        self.mock_redis.setex.return_value = True
        
        updated_data = self.session_data.copy()
        updated_data['status'] = 'in_progress'
        
        result = self.session_manager.update_session(self.session_id, updated_data)
        
        # Проверяем, что метод вернул True
        self.assertTrue(result)
        
        # Проверяем, что был вызван метод setex
        self.mock_redis.setex.assert_called_once()
        
    def test_delete_session(self):
        """Тест удаления сессии"""
        # Настраиваем mock для успешного удаления сессии
        self.mock_redis.delete.return_value = 1
        
        result = self.session_manager.delete_session(self.session_id)
        
        # Проверяем, что метод вернул True
        self.assertTrue(result)
        
        # Проверяем, что был вызван метод delete
        self.mock_redis.delete.assert_called_once_with(self.session_id)
        
    def test_extend_session(self):
        """Тест продления времени жизни сессии"""
        # Настраиваем mock для существующей сессии
        session_data_with_timestamp = self.session_data.copy()
        session_data_with_timestamp['created_at'] = datetime.utcnow().isoformat()
        self.mock_redis.get.return_value = json.dumps(session_data_with_timestamp)
        self.mock_redis.expire.return_value = True
        
        result = self.session_manager.extend_session(self.session_id, 1800)
        
        # Проверяем, что метод вернул True
        self.assertTrue(result)
        
        # Проверяем, что был вызван метод expire
        self.mock_redis.expire.assert_called_once_with(self.session_id, 1800)

if __name__ == '__main__':
    unittest.main()