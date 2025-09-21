import unittest
import torch
import sys
import os

# Добавляем путь к корню проекта для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import PhysiologicalStateModel

class TestPhysiologicalStateModel(unittest.TestCase):
    """Тесты для модели физиологического состояния"""
    
    def setUp(self):
        """Подготовка к тестированию"""
        self.model = PhysiologicalStateModel()
        self.temporal_input = torch.rand(1, 30, 11)  # batch_size=1, sequence_length=30, features=11
        self.static_input = torch.rand(1, 25)  # batch_size=1, features=25 (15 user profile + 10 calibration points)
        
    def test_model_initialization(self):
        """Тест инициализации модели"""
        self.assertIsInstance(self.model, PhysiologicalStateModel)
        self.assertIsNotNone(self.model.temporal_processor)
        self.assertIsNotNone(self.model.static_processor)
        self.assertIsNotNone(self.model.fusion_module)
        self.assertIsNotNone(self.model.output_module)
        
    def test_forward_pass(self):
        """Тест прямого прохода через модель"""
        outputs = self.model(self.temporal_input, self.static_input)
        
        # Проверяем наличие всех выходов
        self.assertIn('current_load', outputs)
        self.assertIn('fatigue_level', outputs)
        self.assertIn('recovery_state', outputs)
        self.assertIn('training_effectiveness', outputs)
        self.assertIn('time_to_exhaustion', outputs)
        self.assertIn('audio_trigger_probability', outputs)
        self.assertIn('performance_improvement', outputs)
        self.assertIn('recommendations_features', outputs)
        self.assertIn('nutrition_features', outputs)
        
    def test_output_shapes(self):
        """Тест форм выходов модели"""
        outputs = self.model(self.temporal_input, self.static_input)
        
        # Проверяем формы выходов
        self.assertEqual(outputs['current_load'].shape, torch.Size([1, 1]))
        self.assertEqual(outputs['fatigue_level'].shape, torch.Size([1, 4]))
        self.assertEqual(outputs['recovery_state'].shape, torch.Size([1, 1]))
        self.assertEqual(outputs['training_effectiveness'].shape, torch.Size([1, 3]))
        self.assertEqual(outputs['time_to_exhaustion'].shape, torch.Size([1, 1]))
        self.assertEqual(outputs['audio_trigger_probability'].shape, torch.Size([1, 1]))
        self.assertEqual(outputs['performance_improvement'].shape, torch.Size([1, 1]))
        self.assertEqual(outputs['recommendations_features'].shape, torch.Size([1, 16]))
        self.assertEqual(outputs['nutrition_features'].shape, torch.Size([1, 32]))
        
    def test_output_ranges(self):
        """Тест диапазонов выходов модели"""
        outputs = self.model(self.temporal_input, self.static_input)
        
        # Проверяем диапазоны значений (где применимо)
        # current_load должен быть в диапазоне [0, 100]
        self.assertTrue(torch.all(outputs['current_load'] >= 0))
        self.assertTrue(torch.all(outputs['current_load'] <= 100))
        
        # fatigue_level должен быть распределением вероятностей (сумма = 1)
        fatigue_probs = outputs['fatigue_level']
        self.assertTrue(torch.all(fatigue_probs >= 0))
        self.assertTrue(torch.all(fatigue_probs <= 1))
        self.assertAlmostEqual(torch.sum(fatigue_probs).item(), 1.0, places=5)
        
        # recovery_state должен быть в диапазоне [0, 100]
        self.assertTrue(torch.all(outputs['recovery_state'] >= 0))
        self.assertTrue(torch.all(outputs['recovery_state'] <= 100))
        
        # training_effectiveness должен быть распределением вероятностей (сумма = 1)
        effectiveness_probs = outputs['training_effectiveness']
        self.assertTrue(torch.all(effectiveness_probs >= 0))
        self.assertTrue(torch.all(effectiveness_probs <= 1))
        self.assertAlmostEqual(torch.sum(effectiveness_probs).item(), 1.0, places=5)
        
        # audio_trigger_probability должен быть в диапазоне [0, 1]
        self.assertTrue(torch.all(outputs['audio_trigger_probability'] >= 0))
        self.assertTrue(torch.all(outputs['audio_trigger_probability'] <= 1))

if __name__ == '__main__':
    unittest.main()