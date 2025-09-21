import os
import sys
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import uuid
from datetime import datetime, timedelta
import redis
import json

# Добавляем путь к корню проекта для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем модели и модули
from models import PhysiologicalStateModel
from sessions.session_manager import SessionManager

# Создаем Flask приложение
app = Flask(__name__)

# Конфигурация JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # В production использовать безопасный ключ
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# Инициализируем Redis для управления сессиями
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Инициализируем менеджер сессий
session_manager = SessionManager(redis_client)

# Инициализируем модель
model = PhysiologicalStateModel()

@app.route('/v1/auth/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    data = request.get_json()
    
    # В реальной системе здесь должна быть проверка api_key
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'API key is required'}), 400
    
    # В данном примере принимаем любой ключ (для демонстрации)
    access_token = create_access_token(identity=api_key)
    
    return jsonify({
        'access_token': access_token,
        'token_type': 'Bearer'
    }), 200

@app.route('/v1/workout/start', methods=['POST'])
@jwt_required()
def start_workout():
    """Начало сессии тренировки"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    calibration_data = data.get('calibration_data')
    user_profile = data.get('user_profile')
    
    if not user_id or not calibration_data or not user_profile:
        return jsonify({'error': 'user_id, calibration_data, and user_profile are required'}), 400
    
    # Генерируем уникальный ID сессии
    session_id = f"workout_{str(uuid.uuid4())[:8]}"
    
    # Создаем сессию
    session_data = {
        'user_id': user_id,
        'calibration_data': calibration_data,
        'user_profile': user_profile,
        'start_time': datetime.utcnow().isoformat(),
        'status': 'initialized'
    }
    
    # Сохраняем сессию в Redis
    session_manager.create_session(session_id, session_data)
    
    return jsonify({
        'session_id': session_id,
        'status': 'initialized',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/v1/workout/update', methods=['POST'])
@jwt_required()
def update_workout():
    """Обновление данных тренировки"""
    data = request.get_json()
    
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400
    
    # Проверяем существование сессии
    session_data = session_manager.get_session(session_id)
    if not session_data:
        return jsonify({'error': 'Session not found'}), 404
    
    # Извлекаем данные
    timestamp = data.get('timestamp')
    hr = data.get('hr')
    hrv = data.get('hrv')
    speed_mps = data.get('speed_mps')
    cadence = data.get('cadence')
    gps = data.get('gps')
    accelerometer = data.get('accelerometer')
    
    # В реальной системе здесь будет обработка данных и вызов модели
    # Для демонстрации возвращаем фиктивные данные
    
    # Формируем входные данные для модели
    # В реальной системе здесь будет более сложная обработка
    temporal_data = [hr, hrv, speed_mps, cadence]  # Упрощенный пример
    static_data = [
        session_data['user_profile'].get('age', 30),
        1 if session_data['user_profile'].get('gender', 'male') == 'male' else 0,
        session_data['user_profile'].get('weight_kg', 70),
        session_data['user_profile'].get('height_cm', 175),
        session_data['user_profile'].get('fitness_level', 2)
    ]
    
    # В реальной системе здесь будет вызов модели:
    # outputs = model(temporal_data, static_data)
    
    # Фиктивные результаты для демонстрации
    outputs = {
        'current_load': 72.5,
        'fatigue_level': 'medium',
        'recovery_state': 85,
        'training_effectiveness': 'optimal',
        'time_to_exhaustion': '12:30',
        'recommendations': [
            {
                'priority': 1, 
                'text': 'Снизьте темп на 10% — вы в зоне перенагрузки'
            },
            {
                'priority': 2, 
                'text': 'Поддерживайте текущий ритм — анаэробный порог достигнут'
            }
        ]
    }
    
    return jsonify({
        'timestamp': timestamp,
        'current_load': outputs['current_load'],
        'fatigue_level': outputs['fatigue_level'],
        'recovery_state': outputs['recovery_state'],
        'training_effectiveness': outputs['training_effectiveness'],
        'time_to_exhaustion': outputs['time_to_exhaustion'],
        'recommendations': outputs['recommendations']
    }), 200

@app.route('/v1/workout/end', methods=['POST'])
@jwt_required()
def end_workout():
    """Завершение сессии тренировки"""
    data = request.get_json()
    
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400
    
    # Проверяем существование сессии
    session_data = session_manager.get_session(session_id)
    if not session_data:
        return jsonify({'error': 'Session not found'}), 404
    
    # Обновляем статус сессии
    session_data['status'] = 'completed'
    session_data['end_time'] = datetime.utcnow().isoformat()
    session_manager.update_session(session_id, session_data)
    
    # Фиктивные финальные метрики для демонстрации
    final_metrics = {
        'duration_minutes': 30.5,
        'average_load': 65.2,
        'peak_load': 82.7,
        'total_distance_km': 5.2,
        'next_workout_recommendations': [
            'Отдохните минимум 24 часа перед следующей интенсивной тренировкой',
            'Следующая тренировка может быть в зоне аэробного порога'
        ]
    }
    
    return jsonify({
        'status': 'completed',
        'session_id': session_id,
        'final_metrics': final_metrics,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/v1/nutrition/preferences', methods=['POST'])
@jwt_required()
def set_nutrition_preferences():
    """Установка предпочтений питания"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    nutrition_goal = data.get('nutrition_goal')
    
    if not user_id or not nutrition_goal:
        return jsonify({'error': 'user_id and nutrition_goal are required'}), 400
    
    # В реальной системе здесь будет сохранение предпочтений
    
    return jsonify({
        'status': 'success',
        'message': 'Nutrition preferences saved',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/v1/nutrition/plan', methods=['POST'])
@jwt_required()
def generate_nutrition_plan():
    """Генерация плана питания"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    
    if not user_id or not session_id:
        return jsonify({'error': 'user_id and session_id are required'}), 400
    
    # В реальной системе здесь будет генерация плана питания
    
    nutrition_plan = {
        'daily_calories': 2500,
        'macronutrient_distribution': {
            'carbs': 0.5,
            'protein': 0.25,
            'fat': 0.25
        },
        'macros_in_grams': {
            'carbs': 312,
            'protein': 156,
            'fat': 70
        },
        'meal_plan': [],  # В реальной системе здесь будет детальный план питания
        'recommendations': [],  # В реальной системе здесь будут рекомендации
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return jsonify(nutrition_plan), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)