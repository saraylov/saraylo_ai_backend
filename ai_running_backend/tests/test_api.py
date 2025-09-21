import unittest
import sys
import os
import json
from datetime import datetime

# Добавляем путь к корню проекта для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.workout_api import app

class TestWorkoutAPI(unittest.TestCase):
    """Тесты для RESTful API"""
    
    def setUp(self):
        """Подготовка к тестированию"""
        self.app = app.test_client()
        app.config['TESTING'] = True
        
    def test_login_endpoint(self):
        """Тест конечной точки аутентификации"""
        # Тест с валидным API ключом
        response = self.app.post('/v1/auth/login',
                                data=json.dumps({'api_key': 'test-key'}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('token_type', data)
        self.assertEqual(data['token_type'], 'Bearer')
        
    def test_login_endpoint_missing_key(self):
        """Тест конечной точки аутентификации с отсутствующим ключом"""
        response = self.app.post('/v1/auth/login',
                                data=json.dumps({}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
    def test_start_workout_endpoint(self):
        """Тест конечной точки начала тренировки"""
        # Сначала получаем токен
        login_response = self.app.post('/v1/auth/login',
                                      data=json.dumps({'api_key': 'test-key'}),
                                      content_type='application/json')
        token_data = json.loads(login_response.data)
        access_token = token_data['access_token']
        
        # Тест начала тренировки
        workout_data = {
            'user_id': 'test-user-123',
            'calibration_data': {'10%': 3.2, '20%': 4.1},
            'user_profile': {
                'age': 28,
                'gender': 'male',
                'weight_kg': 70,
                'height_cm': 175,
                'fitness_level': 2
            }
        }
        
        response = self.app.post('/v1/workout/start',
                                data=json.dumps(workout_data),
                                content_type='application/json',
                                headers={'Authorization': f'Bearer {access_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('session_id', data)
        self.assertIn('status', data)
        self.assertIn('timestamp', data)
        self.assertEqual(data['status'], 'initialized')
        
    def test_update_workout_endpoint(self):
        """Тест конечной точки обновления тренировки"""
        # Сначала получаем токен
        login_response = self.app.post('/v1/auth/login',
                                      data=json.dumps({'api_key': 'test-key'}),
                                      content_type='application/json')
        token_data = json.loads(login_response.data)
        access_token = token_data['access_token']
        
        # Сначала начинаем тренировку
        workout_data = {
            'user_id': 'test-user-123',
            'calibration_data': {'10%': 3.2, '20%': 4.1},
            'user_profile': {
                'age': 28,
                'gender': 'male',
                'weight_kg': 70,
                'height_cm': 175,
                'fitness_level': 2
            }
        }
        
        start_response = self.app.post('/v1/workout/start',
                                      data=json.dumps(workout_data),
                                      content_type='application/json',
                                      headers={'Authorization': f'Bearer {access_token}'})
        
        start_data = json.loads(start_response.data)
        session_id = start_data['session_id']
        
        # Тест обновления тренировки
        update_data = {
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat(),
            'hr': 152,
            'hrv': 42,
            'speed_mps': 3.8,
            'cadence': 178,
            'gps': {
                'lat': 55.7558,
                'lon': 37.6176,
                'elevation': 147,
                'inclination': 2.5
            },
            'accelerometer': {
                'x': 0.1,
                'y': 0.2,
                'z': 9.8
            }
        }
        
        response = self.app.post('/v1/workout/update',
                                data=json.dumps(update_data),
                                content_type='application/json',
                                headers={'Authorization': f'Bearer {access_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
        self.assertIn('current_load', data)
        self.assertIn('fatigue_level', data)
        self.assertIn('recovery_state', data)
        self.assertIn('training_effectiveness', data)
        self.assertIn('time_to_exhaustion', data)
        self.assertIn('recommendations', data)
        
    def test_end_workout_endpoint(self):
        """Тест конечной точки завершения тренировки"""
        # Сначала получаем токен
        login_response = self.app.post('/v1/auth/login',
                                      data=json.dumps({'api_key': 'test-key'}),
                                      content_type='application/json')
        token_data = json.loads(login_response.data)
        access_token = token_data['access_token']
        
        # Сначала начинаем тренировку
        workout_data = {
            'user_id': 'test-user-123',
            'calibration_data': {'10%': 3.2, '20%': 4.1},
            'user_profile': {
                'age': 28,
                'gender': 'male',
                'weight_kg': 70,
                'height_cm': 175,
                'fitness_level': 2
            }
        }
        
        start_response = self.app.post('/v1/workout/start',
                                      data=json.dumps(workout_data),
                                      content_type='application/json',
                                      headers={'Authorization': f'Bearer {access_token}'})
        
        start_data = json.loads(start_response.data)
        session_id = start_data['session_id']
        
        # Тест завершения тренировки
        end_data = {
            'session_id': session_id
        }
        
        response = self.app.post('/v1/workout/end',
                                data=json.dumps(end_data),
                                content_type='application/json',
                                headers={'Authorization': f'Bearer {access_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('session_id', data)
        self.assertIn('final_metrics', data)
        self.assertIn('timestamp', data)
        self.assertEqual(data['status'], 'completed')

if __name__ == '__main__':
    unittest.main()