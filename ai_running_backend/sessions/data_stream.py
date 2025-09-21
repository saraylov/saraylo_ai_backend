import json
import redis
from typing import Dict, List, Optional
from datetime import datetime

class DataStreamManager:
    """Менеджер потока данных для сессий тренировок"""
    
    def __init__(self, redis_client, stream_ttl: int = 3600):
        """
        Инициализация менеджера потока данных
        
        Args:
            redis_client: Клиент Redis
            stream_ttl (int): Время жизни потока данных в секундах
        """
        self.redis_client = redis_client
        self.stream_ttl = stream_ttl
    
    def add_data_point(self, session_id: str, data_point: Dict) -> bool:
        """
        Добавление точки данных в поток
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            data_point (Dict): Данные точки
            
        Returns:
            bool: True если точка успешно добавлена, False в противном случае
        """
        try:
            # Добавляем метку времени
            data_point['timestamp'] = datetime.utcnow().isoformat()
            
            # Ключ для потока данных сессии
            stream_key = f"stream:{session_id}"
            
            # Добавляем точку данных в Redis Stream
            self.redis_client.xadd(stream_key, data_point)
            
            # Устанавливаем время жизни потока
            self.redis_client.expire(stream_key, self.stream_ttl)
            
            return True
        except Exception as e:
            print(f"Error adding data point: {e}")
            return False
    
    def get_data_stream(self, session_id: str, last_id: str = "0-0", count: int = 100) -> List[Dict]:
        """
        Получение потока данных сессии
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            last_id (str): ID последней полученной записи (для пагинации)
            count (int): Максимальное количество записей для получения
            
        Returns:
            List[Dict]: Список точек данных
        """
        try:
            # Ключ для потока данных сессии
            stream_key = f"stream:{session_id}"
            
            # Получаем данные из Redis Stream
            stream_data = self.redis_client.xrange(stream_key, min=last_id, max="+", count=count)
            
            # Преобразуем данные в удобный формат
            result = []
            for entry_id, entry_data in stream_data:
                # Преобразуем bytes в строки если необходимо
                processed_data = {}
                for key, value in entry_data.items():
                    processed_data[key.decode() if isinstance(key, bytes) else key] = \
                        value.decode() if isinstance(value, bytes) else value
                processed_data['id'] = entry_id.decode() if isinstance(entry_id, bytes) else entry_id
                result.append(processed_data)
            
            return result
        except Exception as e:
            print(f"Error getting data stream: {e}")
            return []
    
    def get_latest_data_point(self, session_id: str) -> Optional[Dict]:
        """
        Получение последней точки данных из потока
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            
        Returns:
            Optional[Dict]: Последняя точка данных или None если поток пуст
        """
        try:
            # Ключ для потока данных сессии
            stream_key = f"stream:{session_id}"
            
            # Получаем последнюю запись из Redis Stream
            latest_data = self.redis_client.xrevrange(stream_key, count=1)
            
            if latest_data:
                entry_id, entry_data = latest_data[0]
                # Преобразуем данные в удобный формат
                processed_data = {}
                for key, value in entry_data.items():
                    processed_data[key.decode() if isinstance(key, bytes) else key] = \
                        value.decode() if isinstance(value, bytes) else value
                processed_data['id'] = entry_id.decode() if isinstance(entry_id, bytes) else entry_id
                return processed_data
            
            return None
        except Exception as e:
            print(f"Error getting latest data point: {e}")
            return None
    
    def get_stream_length(self, session_id: str) -> int:
        """
        Получение длины потока данных
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            
        Returns:
            int: Длина потока данных
        """
        try:
            # Ключ для потока данных сессии
            stream_key = f"stream:{session_id}"
            
            # Получаем длину потока
            return self.redis_client.xlen(stream_key)
        except Exception as e:
            print(f"Error getting stream length: {e}")
            return 0
    
    def trim_stream(self, session_id: str, max_length: int) -> bool:
        """
        Обрезка потока данных до максимальной длины
        
        Args:
            session_id (str): Уникальный идентификатор сессии
            max_length (int): Максимальная длина потока
            
        Returns:
            bool: True если обрезка успешна, False в противном случае
        """
        try:
            # Ключ для потока данных сессии
            stream_key = f"stream:{session_id}"
            
            # Обрезаем поток
            self.redis_client.xtrim(stream_key, maxlen=max_length)
            
            return True
        except Exception as e:
            print(f"Error trimming stream: {e}")
            return False