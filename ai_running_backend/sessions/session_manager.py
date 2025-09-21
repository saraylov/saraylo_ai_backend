import json
import redis
from datetime import datetime, timedelta

class SessionManager:
    """Менеджер сессий тренировок"""
    
    def __init__(self, redis_client, session_ttl=3600):
        """
        Инициализация менеджера сессий
        
        Args:
            redis_client: Клиент Redis
            session_ttl: Время жизни сессии в секундах (по умолчанию 1 час)
        """
        self.redis_client = redis_client
        self.session_ttl = session_ttl
    
    def create_session(self, session_id, session_data):
        """
        Создание новой сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            session_data (dict): Данные сессии
            
        Returns:
            bool: True если сессия успешно создана, False в противном случае
        """
        try:
            # Добавляем метку времени создания
            session_data['created_at'] = datetime.utcnow().isoformat()
            
            # Сохраняем сессию в Redis
            self.redis_client.setex(
                session_id, 
                self.session_ttl, 
                json.dumps(session_data)
            )
            return True
        except Exception as e:
            print(f"Error creating session: {e}")
            return False
    
    def get_session(self, session_id):
        """
        Получение данных сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            
        Returns:
            dict: Данные сессии или None если сессия не найдена
        """
        try:
            session_data = self.redis_client.get(session_id)
            if session_data:
                return json.loads(session_data)
            return None
        except Exception as e:
            print(f"Error getting session: {e}")
            return None
    
    def update_session(self, session_id, session_data):
        """
        Обновление данных сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            session_data (dict): Обновленные данные сессии
            
        Returns:
            bool: True если сессия успешно обновлена, False в противном случае
        """
        try:
            # Добавляем метку времени обновления
            session_data['updated_at'] = datetime.utcnow().isoformat()
            
            # Обновляем сессию в Redis
            self.redis_client.setex(
                session_id, 
                self.session_ttl, 
                json.dumps(session_data)
            )
            return True
        except Exception as e:
            print(f"Error updating session: {e}")
            return False
    
    def delete_session(self, session_id):
        """
        Удаление сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            
        Returns:
            bool: True если сессия успешно удалена, False в противном случае
        """
        try:
            result = self.redis_client.delete(session_id)
            return result > 0
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def extend_session(self, session_id, additional_time=None):
        """
        Продление времени жизни сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            additional_time (int): Дополнительное время в секундах (по умолчанию используется session_ttl)
            
        Returns:
            bool: True если время жизни успешно продлено, False в противном случае
        """
        try:
            if additional_time is None:
                additional_time = self.session_ttl
                
            # Получаем текущие данные сессии
            session_data = self.get_session(session_id)
            if session_data:
                # Продляем время жизни ключа
                self.redis_client.expire(session_id, additional_time)
                return True
            return False
        except Exception as e:
            print(f"Error extending session: {e}")
            return False