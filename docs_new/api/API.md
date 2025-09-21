# Спецификация API

## Аутентификация
```
POST /v1/auth/login
```
**Тело запроса:**
```json
{
  "api_key": "your-api-key"
}
```

**Ответ:**
```json
{
  "access_token": "jwt-token",
  "token_type": "Bearer"
}
```

## Начало сессии тренировки
```
POST /v1/workout/start
```
**Тело запроса:**
```json
{
  "user_id": "uuid",
  "calibration_data": { "10%": 3.2, "20%": 4.1, ... },
  "user_profile": { 
    "age": 28, 
    "gender": "male", 
    "weight_kg": 70, 
    "height_cm": 175,
    "fitness_level": 2
  }
}
```

**Ответ:**
```json
{ 
  "session_id": "workout_123", 
  "status": "initialized",
  "timestamp": "2024-03-20T14:30:45Z"
}
```

## Обновление данных тренировки
```
POST /v1/workout/update
```
**Тело запроса:**
```json
{
  "session_id": "workout_123",
  "timestamp": "2024-03-20T14:30:45Z",
  "hr": 152,
  "hrv": 42,
  "speed_mps": 3.8,
  "cadence": 178,
  "gps": { 
    "lat": 55.7558, 
    "lon": 37.6176, 
    "elevation": 147,
    "inclination": 2.5
  },
  "accelerometer": {
    "x": 0.1,
    "y": 0.2,
    "z": 9.8
  }
}
```

**Ответ:**
```json
{
  "timestamp": "2024-03-20T14:30:45Z",
  "current_load": 72.5,
  "fatigue_level": "medium",
  "recovery_state": 85,
  "training_effectiveness": "optimal",
  "time_to_exhaustion": "12:30",
  "recommendations": [
    {
      "priority": 1, 
      "text": "Снизьте темп на 10% — вы в зоне перенагрузки"
    },
    {
      "priority": 2, 
      "text": "Поддерживайте текущий ритм — анаэробный порог достигнут"
    }
  ]
}
```

## Завершение сессии тренировки
```
POST /v1/workout/end
```
**Тело запроса:**
```json
{ 
  "session_id": "workout_123", 
  "final_metrics": { ... } 
}
```

**Ответ:**
```json
{ 
  "status": "completed", 
  "session_id": "workout_123", 
  "final_metrics": {
    "duration_minutes": 30.5,
    "average_load": 65.2,
    "peak_load": 82.7,
    "total_distance_km": 5.2,
    "next_workout_recommendations": [
      "Отдохните минимум 24 часа перед следующей интенсивной тренировкой",
      "Следующая тренировка может быть в зоне аэробного порога"
    ]
  },
  "timestamp": "2024-03-20T15:00:45Z"
}
```

## Установка предпочтений питания
```
POST /v1/nutrition/preferences
```
**Тело запроса:**
```json
{
  "user_id": "uuid",
  "nutrition_goal": "weight_loss",
  "dietary_restrictions": ["vegetarian"],
  "preferred_cuisines": ["mediterranean"],
  "cooking_time": 30
}
```

**Ответ:**
```json
{
  "status": "success",
  "message": "Nutrition preferences saved",
  "timestamp": "2024-03-20T14:30:45Z"
}
```

## Генерация плана питания
```
POST /v1/nutrition/plan
```
**Тело запроса:**
```json
{
  "user_id": "uuid",
  "session_id": "workout_123",
  "nutrition_goal": "muscle_gain"
}
```

**Ответ:**
```json
{
  "daily_calories": 2500,
  "macronutrient_distribution": {
    "carbs": 0.5,
    "protein": 0.25,
    "fat": 0.25
  },
  "macros_in_grams": {
    "carbs": 312,
    "protein": 156,
    "fat": 70
  },
  "meal_plan": [...],
  "recommendations": [...],
  "timestamp": "2024-03-20T14:30:45Z"
}
```