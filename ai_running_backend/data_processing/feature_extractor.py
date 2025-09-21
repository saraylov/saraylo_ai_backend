import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Any

class FeatureExtractor:
    """Класс для извлечения признаков из данных тренировки"""
    
    def __init__(self):
        """Инициализация экстрактора признаков"""
        pass
    
    def extract_temporal_features(self, workout_data: List[Dict]) -> np.ndarray:
        """
        Извлечение временных признаков из потока данных тренировки
        
        Args:
            workout_data (List[Dict]): Список словарей с данными тренировки
            
        Returns:
            np.ndarray: Массив временных признаков размерности (sequence_length, num_features)
        """
        if not workout_data:
            return np.array([])
        
        # Определяем временные признаки
        temporal_features = []
        
        for data_point in workout_data:
            features = []
            
            # Частота сердечных сокращений
            features.append(data_point.get('hr', 0))
            
            # Вариабельность ЧСС
            features.append(data_point.get('hrv', 0))
            
            # Скорость бега
            features.append(data_point.get('speed_mps', 0))
            
            # Каденс
            features.append(data_point.get('cadence', 0))
            
            # Данные GPS
            gps = data_point.get('gps', {})
            features.append(gps.get('lat', 0))
            features.append(gps.get('lon', 0))
            features.append(gps.get('elevation', 0))
            features.append(gps.get('inclination', 0))
            
            # Данные акселерометра
            accelerometer = data_point.get('accelerometer', {})
            features.append(accelerometer.get('x', 0))
            features.append(accelerometer.get('y', 0))
            features.append(accelerometer.get('z', 0))
            
            temporal_features.append(features)
        
        return np.array(temporal_features)
    
    def extract_static_features(self, user_profile: Dict, calibration_data: Dict) -> np.ndarray:
        """
        Извлечение статических признаков из профиля пользователя и калибровочных данных
        
        Args:
            user_profile (Dict): Профиль пользователя
            calibration_data (Dict): Калибровочные данные
            
        Returns:
            np.ndarray: Массив статических признаков размерности (num_features,)
        """
        static_features = []
        
        # Демографические данные
        static_features.append(user_profile.get('age', 30))
        
        # Пол (мужской = 1, женский = 0)
        gender = user_profile.get('gender', 'male')
        static_features.append(1 if gender == 'male' else 0)
        
        # Вес
        static_features.append(user_profile.get('weight_kg', 70))
        
        # Рост
        static_features.append(user_profile.get('height_cm', 175))
        
        # Уровень физической подготовки
        static_features.append(user_profile.get('fitness_level', 2))
        
        # Калибровочные данные (10 точек скорости для процентилей от 10% до 100%)
        percentiles = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        for percentile in percentiles:
            key = f"{percentile}%"
            static_features.append(calibration_data.get(key, 0))
        
        return np.array(static_features)
    
    def normalize_features(self, features: np.ndarray, feature_type: str = 'temporal') -> np.ndarray:
        """
        Нормализация признаков для входа в нейронную сеть
        
        Args:
            features (np.ndarray): Массив признаков
            feature_type (str): Тип признаков ('temporal' или 'static')
            
        Returns:
            np.ndarray: Нормализованный массив признаков
        """
        if features.size == 0:
            return features
        
        # Для демонстрации используем простую мин-макс нормализацию
        # В реальной системе можно использовать более сложные методы
        
        if feature_type == 'temporal':
            # Нормализация временных признаков
            min_vals = np.min(features, axis=0)
            max_vals = np.max(features, axis=0)
            
            # Избегаем деления на ноль
            range_vals = np.where(max_vals - min_vals == 0, 1, max_vals - min_vals)
            
            normalized = (features - min_vals) / range_vals
            return normalized
        
        elif feature_type == 'static':
            # Для статических признаков можно использовать z-score нормализацию
            mean_vals = np.mean(features)
            std_vals = np.std(features)
            
            # Избегаем деления на ноль
            if std_vals == 0:
                std_vals = 1
                
            normalized = (features - mean_vals) / std_vals
            return normalized
        
        return features
    
    def calculate_hrv_metrics(self, hrv_data: List[float]) -> Dict[str, float]:
        """
        Расчет метрик HRV (Вариабельность сердечного ритма)
        
        Args:
            hrv_data (List[float]): Список значений HRV
            
        Returns:
            Dict[str, float]: Словарь с метриками HRV
        """
        if not hrv_data:
            return {}
        
        hrv_array = np.array(hrv_data)
        
        metrics = {
            'mean_hrv': np.mean(hrv_array),
            'std_hrv': np.std(hrv_array),
            'min_hrv': np.min(hrv_array),
            'max_hrv': np.max(hrv_array),
            'rmssd': self._calculate_rmssd(hrv_data) if len(hrv_data) > 1 else 0,
            'nn50': self._calculate_nn50(hrv_data) if len(hrv_data) > 1 else 0
        }
        
        return metrics
    
    def calculate_speed_metrics(self, speed_data: List[float]) -> Dict[str, float]:
        """
        Расчет метрик скорости
        
        Args:
            speed_data (List[float]): Список значений скорости
            
        Returns:
            Dict[str, float]: Словарь с метриками скорости
        """
        if not speed_data:
            return {}
        
        speed_array = np.array(speed_data)
        
        metrics = {
            'mean_speed': np.mean(speed_array),
            'max_speed': np.max(speed_array),
            'min_speed': np.min(speed_array),
            'std_speed': np.std(speed_array),
            'total_distance': np.sum(speed_array) * 60  # Предполагаем 1 минуту на точку данных
        }
        
        return metrics
    
    def _calculate_rmssd(self, hrv_data: List[float]) -> float:
        """
        Расчет RMSSD (Root Mean Square of Successive Differences)
        
        Args:
            hrv_data (List[float]): Список значений HRV
            
        Returns:
            float: Значение RMSSD
        """
        if len(hrv_data) < 2:
            return 0
            
        differences = np.diff(hrv_data)
        squared_diff = np.square(differences)
        mean_squared_diff = np.mean(squared_diff)
        rmssd = np.sqrt(mean_squared_diff)
        
        return rmssd
    
    def _calculate_nn50(self, hrv_data: List[float]) -> int:
        """
        Расчет NN50 (Number of pairs of successive NNs that differ by more than 50 ms)
        
        Args:
            hrv_data (List[float]): Список значений HRV
            
        Returns:
            int: Значение NN50
        """
        if len(hrv_data) < 2:
            return 0
            
        differences = np.abs(np.diff(hrv_data))
        nn50 = np.sum(differences > 50)
        
        return int(nn50)

def prepare_model_input(workout_data: List[Dict], user_profile: Dict, calibration_data: Dict) -> Tuple[np.ndarray, np.ndarray]:
    """
    Подготовка входных данных для модели нейронной сети
    
    Args:
        workout_data (List[Dict]): Список словарей с данными тренировки
        user_profile (Dict): Профиль пользователя
        calibration_data (Dict): Калибровочные данные
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Кортеж из временных и статических признаков
    """
    extractor = FeatureExtractor()
    
    # Извлечение временных признаков
    temporal_features = extractor.extract_temporal_features(workout_data)
    
    # Извлечение статических признаков
    static_features = extractor.extract_static_features(user_profile, calibration_data)
    
    # Нормализация признаков
    normalized_temporal = extractor.normalize_features(temporal_features, 'temporal')
    normalized_static = extractor.normalize_features(static_features, 'static')
    
    return normalized_temporal, normalized_static