import unittest
import sys
import os

# Добавляем путь к корню проекта для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nutrition.nutrition_recommender import NutritionRecommender

class TestNutritionRecommender(unittest.TestCase):
    """Тесты для рекомендателя питания"""
    
    def setUp(self):
        """Подготовка к тестированию"""
        self.recommender = NutritionRecommender()
        
        # Тестовый профиль пользователя
        self.user_profile = {
            'age': 28,
            'gender': 'male',
            'weight_kg': 70,
            'height_cm': 175,
            'fitness_level': 2
        }
        
    def test_calculate_bmr(self):
        """Тест расчета базовой метаболической скорости"""
        bmr = self.recommender.calculate_bmr(self.user_profile)
        
        # Проверяем, что BMR рассчитан (примерное значение для мужчины 28 лет, 70 кг, 175 см)
        self.assertGreater(bmr, 1500)
        self.assertLess(bmr, 2500)
        
    def test_calculate_tdee(self):
        """Тест расчета общего расхода энергии"""
        tdee = self.recommender.calculate_tdee(self.user_profile, "moderate")
        
        # Проверяем, что TDEE рассчитан
        self.assertGreater(tdee, 2000)
        self.assertLess(tdee, 3500)
        
    def test_generate_nutrition_plan_weight_loss(self):
        """Тест генерации плана питания для потери веса"""
        plan = self.recommender.generate_nutrition_plan(
            self.user_profile, 
            "weight_loss",
            ["vegetarian"],
            ["mediterranean"]
        )
        
        # Проверяем наличие всех ключевых элементов плана
        self.assertIn('daily_calories', plan)
        self.assertIn('macronutrient_distribution', plan)
        self.assertIn('macros_in_grams', plan)
        self.assertIn('recommended_foods', plan)
        self.assertIn('foods_to_avoid', plan)
        self.assertIn('meal_plan', plan)
        self.assertIn('recommendations', plan)
        
        # Проверяем, что калории уменьшены для потери веса
        self.assertLess(plan['daily_calories'], 2500)  # Примерное значение
        
    def test_generate_nutrition_plan_muscle_gain(self):
        """Тест генерации плана питания для набора мышечной массы"""
        plan = self.recommender.generate_nutrition_plan(
            self.user_profile, 
            "muscle_gain"
        )
        
        # Проверяем наличие всех ключевых элементов плана
        self.assertIn('daily_calories', plan)
        self.assertIn('macronutrient_distribution', plan)
        self.assertIn('macros_in_grams', plan)
        
        # Проверяем, что калории увеличены для набора массы
        self.assertGreater(plan['daily_calories'], 2500)  # Примерное значение
        
    def test_generate_nutrition_plan_default(self):
        """Тест генерации плана питания по умолчанию"""
        plan = self.recommender.generate_nutrition_plan(self.user_profile, "general_health")
        
        # Проверяем наличие всех ключевых элементов плана
        self.assertIn('daily_calories', plan)
        self.assertIn('macronutrient_distribution', plan)
        self.assertIn('macros_in_grams', plan)
        self.assertIn('recommended_foods', plan)
        self.assertIn('foods_to_avoid', plan)
        
    def test_get_cuisine_recommendations(self):
        """Тест получения рекомендаций по кухням"""
        recommendations = self.recommender._get_cuisine_recommendations(["mediterranean", "asian"])
        
        # Проверяем, что возвращены рекомендации
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]['name'], 'mediterranean')
        self.assertEqual(recommendations[1]['name'], 'asian')
        
    def test_generate_nutrition_recommendations(self):
        """Тест генерации рекомендаций по питанию"""
        recommendations = self.recommender._generate_nutrition_recommendations(
            "weight_loss", 
            ["vegetarian"]
        )
        
        # Проверяем, что возвращены рекомендации
        self.assertGreater(len(recommendations), 0)
        self.assertIsInstance(recommendations, list)

if __name__ == '__main__':
    unittest.main()