import time
import redis
from typing import Dict, Optional

class RateLimiter:
    """Ограничитель скорости запросов для сессий тренировок"""
    
    def __init__(self, redis_client, requests_per_minute: int = 6):
        """
        Инициализация ограничителя скорости
        
        Args:
            redis_client: Клиент Redis
            requests_per_minute (int): Максимальное количество запросов в минуту
        """
        self.redis_client = redis_client
        self.requests_per_minute = requests_per_minute
        self.window_size = 60  # 60 секунд
    
    def is_allowed(self, session_id: str) -> bool:
        """
        Проверка, разрешен ли запрос для данной сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            
        Returns:
            bool: True если запрос разрешен, False если превышен лимит
        """
        try:
            # Ключ для хранения времени запросов
            key = f"rate_limit:{session_id}"
            
            # Текущее время
            now = time.time()
            
            # Удаляем устаревшие записи (старше window_size секунд)
            self.redis_client.zremrangebyscore(key, 0, now - self.window_size)
            
            # Подсчитываем количество запросов в текущем окне
            request_count = self.redis_client.zcard(key)
            
            # Проверяем, превышен ли лимит
            if request_count >= self.requests_per_minute:
                return False
            
            # Добавляем текущий запрос
            self.redis_client.zadd(key, {str(now): now})
            
            # Устанавливаем время жизни ключа
            self.redis_client.expire(key, self.window_size)
            
            return True
            
        except Exception as e:
            print(f"Error in rate limiting: {e}")
            # В случае ошибки разрешаем запрос (fail-open подход)
            return True
    
    def get_remaining_requests(self, session_id: str) -> int:
        """
        Получение количества оставшихся запросов для сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            
        Returns:
            int: Количество оставшихся запросов
        """
        try:
            key = f"rate_limit:{session_id}"
            
            # Текущее время
            now = time.time()
            
            # Удаляем устаревшие записи
            self.redis_client.zremrangebyscore(key, 0, now - self.window_size)
            
            # Подсчитываем количество запросов в текущем окне
            request_count = self.redis_client.zcard(key)
            
            return max(0, self.requests_per_minute - request_count)
            
        except Exception as e:
            print(f"Error getting remaining requests: {e}")
            return self.requests_per_minute
    
    def reset_rate_limit(self, session_id: str) -> bool:
        """
        Сброс ограничения скорости для сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            
        Returns:
            bool: True если сброс успешен, False в противном случае
        """
        try:
            key = f"rate_limit:{session_id}"
            result = self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Error resetting rate limit: {e}")
            return False