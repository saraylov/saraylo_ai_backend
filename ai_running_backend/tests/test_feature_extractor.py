import unittest
import sys
import os
import numpy as np

# Добавляем путь к корню проекта для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing.feature_extractor import FeatureExtractor, prepare_model_input

class TestFeatureExtractor(unittest.TestCase):
    """Тесты для экстрактора признаков"""
    
    def setUp(self):
        """Подготовка к тестированию"""
        self.extractor = FeatureExtractor()
        
        # Тестовые данные тренировки
        self.workout_data = [
            {
                'hr': 150,
                'hrv': 40,
                'speed_mps': 3.5,
                'cadence': 175,
                'gps': {'lat': 55.75, 'lon': 37.62, 'elevation': 150, 'inclination': 2.0},
                'accelerometer': {'x': 0.1, 'y': 0.2, 'z': 9.8}
            },
            {
                'hr': 155,
                'hrv': 42,
                'speed_mps': 3.8,
                'cadence': 178,
                'gps': {'lat': 55.76, 'lon': 37.63, 'elevation': 152, 'inclination': 2.5},
                'accelerometer': {'x': 0.2, 'y': 0.1, 'z': 9.7}
            }
        ]
        
        # Тестовый профиль пользователя
        self.user_profile = {
            'age': 28,
            'gender': 'male',
            'weight_kg': 70,
            'height_cm': 175,
            'fitness_level': 2
        }
        
        # Тестовые калибровочные данные
        self.calibration_data = {
            '10%': 2.5, '20%': 3.0, '30%': 3.5, '40%': 4.0, '50%': 4.5,
            '60%': 5.0, '70%': 5.5, '80%': 6.0, '90%': 6.5, '100%': 7.0
        }
        
    def test_extract_temporal_features(self):
        """Тест извлечения временных признаков"""
        features = self.extractor.extract_temporal_features(self.workout_data)
        
        # Проверяем форму результата
        self.assertEqual(features.shape, (2, 9))  # 2 точки данных, 9 признаков
        
        # Проверяем значения (первая точка данных)
        self.assertEqual(features[0, 0], 150)  # hr
        self.assertEqual(features[0, 1], 40)   # hrv
        self.assertEqual(features[0, 2], 3.5)  # speed_mps
        self.assertEqual(features[0, 3], 175)  # cadence
        self.assertEqual(features[0, 4], 55.75)  # lat
        self.assertEqual(features[0, 5], 37.62)  # lon
        self.assertEqual(features[0, 6], 150)    # elevation
        self.assertEqual(features[0, 7], 2.0)    # inclination
        self.assertEqual(features[0, 8], 0.1)    # accelerometer x
        
    def test_extract_static_features(self):
        """Тест извлечения статических признаков"""
        features = self.extractor.extract_static_features(self.user_profile, self.calibration_data)
        
        # Проверяем форму результата
        self.assertEqual(features.shape, (25,))  # 15 признаков профиля + 10 калибровочных точек
        
        # Проверяем значения
        self.assertEqual(features[0], 28)    # age
        self.assertEqual(features[1], 1)     # gender (male = 1)
        self.assertEqual(features[2], 70)    # weight
        self.assertEqual(features[3], 175)   # height
        self.assertEqual(features[4], 2)     # fitness_level
        self.assertEqual(features[5], 2.5)   # 10% calibration
        self.assertEqual(features[14], 7.0)  # 100% calibration
        
    def test_normalize_features(self):
        """Тест нормализации признаков"""
        # Тест нормализации временных признаков
        temporal_features = self.extractor.extract_temporal_features(self.workout_data)
        normalized_temporal = self.extractor.normalize_features(temporal_features, 'temporal')
        
        # Проверяем, что нормализованные значения находятся в диапазоне [0, 1]
        self.assertTrue(np.all(normalized_temporal >= 0))
        self.assertTrue(np.all(normalized_temporal <= 1))
        
        # Тест нормализации статических признаков
        static_features = self.extractor.extract_static_features(self.user_profile, self.calibration_data)
        normalized_static = self.extractor.normalize_features(static_features, 'static')
        
        # Для z-score нормализации проверяем, что среднее близко к 0
        self.assertAlmostEqual(np.mean(normalized_static), 0, places=1)
        
    def test_calculate_hrv_metrics(self):
        """Тест расчета метрик HRV"""
        hrv_data = [40.0, 42.0, 38.0, 45.0, 41.0]
        metrics = self.extractor.calculate_hrv_metrics(hrv_data)
        
        # Проверяем наличие всех метрик
        self.assertIn('mean_hrv', metrics)
        self.assertIn('std_hrv', metrics)
        self.assertIn('min_hrv', metrics)
        self.assertIn('max_hrv', metrics)
        self.assertIn('rmssd', metrics)
        self.assertIn('nn50', metrics)
        
        # Проверяем значения
        self.assertEqual(metrics['mean_hrv'], 41.2)
        self.assertEqual(metrics['min_hrv'], 38)
        self.assertEqual(metrics['max_hrv'], 45)
        
    def test_calculate_speed_metrics(self):
        """Тест расчета метрик скорости"""
        speed_data = [3.5, 3.8, 3.6, 4.0, 3.7]
        metrics = self.extractor.calculate_speed_metrics(speed_data)
        
        # Проверяем наличие всех метрик
        self.assertIn('mean_speed', metrics)
        self.assertIn('max_speed', metrics)
        self.assertIn('min_speed', metrics)
        self.assertIn('std_speed', metrics)
        self.assertIn('total_distance', metrics)
        
        # Проверяем значения
        self.assertEqual(metrics['min_speed'], 3.5)
        self.assertEqual(metrics['max_speed'], 4.0)
        
    def test_prepare_model_input(self):
        """Тест подготовки входных данных для модели"""
        temporal_features, static_features = prepare_model_input(
            self.workout_data, self.user_profile, self.calibration_data)
        
        # Проверяем формы
        self.assertEqual(temporal_features.shape, (2, 9))  # 2 точки данных, 9 признаков
        self.assertEqual(static_features.shape, (25,))     # 25 статических признаков

if __name__ == '__main__':
    unittest.main()