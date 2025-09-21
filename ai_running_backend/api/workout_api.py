import os
import hashlib
import hmac
import uuid
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from functools import wraps
import jwt  # Import jwt directly

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Включаем CORS для всех маршрутов
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ваш Telegram Bot Token
TELEGRAM_BOT_TOKEN = "8133563995:AAHgcsZ7S3vmYWb6XYx3SbcQa1I_ldOV_1E"

# Хранилище для API ключей (в реальном приложении используйте базу данных)
api_keys = {}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Убираем "Bearer " из токена
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Аутентификация по API ключу"""
    data = request.get_json()
    api_key = data.get('api_key')
    
    # В реальной системе здесь будет проверка API ключа
    if not api_key:
        return jsonify({'error': 'API key is required'}), 400
    
    # Генерируем JWT токен
    token = jwt.encode({
        'user_id': 'user123',
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'access_token': token,
        'token_type': 'Bearer'
    }), 200

@app.route('/auth/telegram', methods=['GET', 'POST'])
def telegram_auth():
    """Обработка авторизации через Telegram"""
    if request.method == 'GET':
        # Перенаправляем POST запросы
        return redirect(url_for('telegram_auth'), code=307)
    
    # Получаем данные от Telegram
    telegram_data = request.form.to_dict()
    
    # Проверяем подлинность данных от Telegram
    if not verify_telegram_data(telegram_data):
        return jsonify({'error': 'Invalid Telegram data'}), 400
    
    # Извлекаем информацию о пользователе
    user_id = telegram_data.get('id')
    username = telegram_data.get('username', f'user_{user_id}')
    
    # Генерируем персональный API ключ для пользователя
    if user_id not in api_keys:
        api_key = str(uuid.uuid4())
        api_keys[user_id] = {
            'api_key': api_key,
            'username': username,
            'created_at': datetime.utcnow().isoformat()
        }
    else:
        api_key = api_keys[user_id]['api_key']
    
    # Создаем JWT токен для пользователя
    user_data = {
        'id': user_id,
        'first_name': telegram_data.get('first_name'),
        'last_name': telegram_data.get('last_name'),
        'username': username,
        'photo_url': telegram_data.get('photo_url'),
        'auth_date': telegram_data.get('auth_date'),
        'api_key': api_key
    }
    
    token = jwt.encode({
        'user': user_data,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    # Возвращаем токен и перенаправляем на фронтенд
    return jsonify({
        'access_token': token,
        'user': user_data,
        'api_key': api_key
    }), 200

def verify_telegram_data(telegram_data):
    """Проверка подлинности данных от Telegram"""
    # Удаляем hash из данных для проверки
    received_hash = telegram_data.pop('hash', None)
    
    if not received_hash:
        return False
    
    # Создаем строку данных для проверки
    data_check_string = '\n'.join(sorted([f"{k}={v}" for k, v in telegram_data.items() if k != 'hash']))
    
    # Создаем секретный ключ
    secret_key = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()
    
    # Вычисляем хэш
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    # Сравниваем хэши
    return hmac.compare_digest(calculated_hash, received_hash)

@app.route('/api/v1/workout/start', methods=['POST'])
@token_required
def start_workout_session():
    """Начало тренировочной сессии"""
    data = request.get_json()
    
    # В реальной системе здесь будет логика начала тренировки
    session_id = f"session_{int(datetime.utcnow().timestamp())}"
    
    return jsonify({
        'status': 'started',
        'session_id': session_id,
        'start_time': datetime.utcnow().isoformat(),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/v1/workout/update', methods=['POST'])
@token_required
def update_workout_session():
    """Обновление данных тренировочной сессии"""
    data = request.get_json()
    
    # В реальной системе здесь будет логика обновления данных
    return jsonify({
        'status': 'updated',
        'session_id': data.get('session_id'),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/v1/workout/end', methods=['POST'])
@token_required
def end_workout_session():
    """Завершение тренировочной сессии"""
    data = request.get_json()
    
    # В реальной системе здесь будет логика завершения тренировки
    final_metrics = {
        'distance_km': 5.2,
        'duration_minutes': 32,
        'avg_load': 72,
        'calories_burned': 420
    }
    
    return jsonify({
        'status': 'completed',
        'session_id': data.get('session_id'),
        'final_metrics': final_metrics,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/v1/nutrition/preferences', methods=['POST'])
@token_required
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

@app.route('/api/v1/nutrition/plan', methods=['POST'])
@token_required
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