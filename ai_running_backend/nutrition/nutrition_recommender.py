import json
from typing import Dict, List, Optional
from datetime import datetime

class NutritionRecommender:
    """Рекомендатель системы питания"""
    
    def __init__(self):
        """Инициализация рекомендателя питания"""
        # База данных предпочтений питания (в реальной системе это будет в БД)
        self.nutrition_database = {
            "weight_loss": {
                "daily_calories_reduction": 500,
                "macro_distribution": {"carbs": 0.4, "protein": 0.3, "fat": 0.3},
                "recommended_foods": ["vegetables", "lean_proteins", "whole_grains"],
                "foods_to_avoid": ["processed_foods", "sugary_drinks", "refined_carbs"]
            },
            "muscle_gain": {
                "daily_calories_increase": 300,
                "macro_distribution": {"carbs": 0.5, "protein": 0.25, "fat": 0.25},
                "recommended_foods": ["lean_proteins", "complex_carbs", "healthy_fats"],
                "foods_to_avoid": ["empty_calories", "trans_fats"]
            },
            "endurance": {
                "daily_calories_adjustment": 0,
                "macro_distribution": {"carbs": 0.6, "protein": 0.2, "fat": 0.2},
                "recommended_foods": ["complex_carbs", "moderate_proteins", "healthy_fats"],
                "foods_to_avoid": ["high_fat_meals_before_exercise"]
            },
            "general_health": {
                "daily_calories_adjustment": 0,
                "macro_distribution": {"carbs": 0.5, "protein": 0.25, "fat": 0.25},
                "recommended_foods": ["balanced_diet", "fruits", "vegetables", "whole_grains"],
                "foods_to_avoid": ["excessive_sugar", "processed_foods"]
            }
        }
        
        # Информация о кухнях
        self.cuisine_info = {
            "mediterranean": {
                "characteristics": "Rich in olive oil, vegetables, fruits, whole grains, fish, and poultry",
                "benefits": "Heart-healthy, anti-inflammatory",
                "sample_foods": ["olive_oil", "fish", "tomatoes", "leafy_greens"]
            },
            "asian": {
                "characteristics": "Emphasis on rice, noodles, vegetables, seafood, and soy products",
                "benefits": "Balanced nutrition, variety of flavors",
                "sample_foods": ["rice", "vegetables", "seafood", "tofu"]
            },
            "american": {
                "characteristics": "Diverse, includes grilled meats, potatoes, corn, and dairy",
                "benefits": "Familiar flavors, hearty meals",
                "sample_foods": ["grilled_chicken", "sweet_potatoes", "corn", "dairy"]
            }
        }
    
    def calculate_bmr(self, user_profile: Dict) -> float:
        """
        Расчет базовой метаболической скорости (BMR) по формуле Миффлина-Сан Жеора
        
        Args:
            user_profile (Dict): Профиль пользователя
            
        Returns:
            float: BMR в калориях
        """
        weight = user_profile.get('weight_kg', 70)
        height = user_profile.get('height_cm', 175)
        age = user_profile.get('age', 30)
        gender = user_profile.get('gender', 'male')
        
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
        return bmr
    
    def calculate_tdee(self, user_profile: Dict, activity_level: str = "moderate") -> float:
        """
        Расчет общего расхода энергии (TDEE)
        
        Args:
            user_profile (Dict): Профиль пользователя
            activity_level (str): Уровень активности
            
        Returns:
            float: TDEE в калориях
        """
        bmr = self.calculate_bmr(user_profile)
        
        # Коэффициенты активности
        activity_multipliers = {
            "sedentary": 1.2,      # Мало или нет физических нагрузок
            "light": 1.375,        # Легкие упражнения 1-3 дня в неделю
            "moderate": 1.55,      # Умеренные упражнения 3-5 дней в неделю
            "active": 1.725,       # Тяжелые упражнения 6-7 дней в неделю
            "very_active": 1.9     # Очень тяжелые упражнения и физическая работа
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.55)
        return bmr * multiplier
    
    def generate_nutrition_plan(self, user_profile: Dict, nutrition_goal: str, 
                              dietary_restrictions: Optional[List[str]] = None, 
                              preferred_cuisines: Optional[List[str]] = None) -> Dict:
        """
        Генерация персонализированного плана питания
        
        Args:
            user_profile (Dict): Профиль пользователя
            nutrition_goal (str): Цель питания
            dietary_restrictions (List[str]): Диетические ограничения
            preferred_cuisines (List[str]): Предпочтительные кухни
            
        Returns:
            Dict: План питания
        """
        if dietary_restrictions is None:
            dietary_restrictions = []
        if preferred_cuisines is None:
            preferred_cuisines = []
            
        # Получаем базовую информацию о цели питания
        goal_info = self.nutrition_database.get(nutrition_goal, self.nutrition_database["general_health"])
        
        # Рассчитываем TDEE
        tdee = self.calculate_tdee(user_profile)
        
        # Корректируем калории в зависимости от цели
        if nutrition_goal == "weight_loss":
            daily_calories = tdee - goal_info["daily_calories_reduction"]
        elif nutrition_goal == "muscle_gain":
            daily_calories = tdee + goal_info["daily_calories_increase"]
        else:
            daily_calories = tdee + goal_info["daily_calories_adjustment"]
        
        # Получаем распределение макронутриентов
        macro_dist = goal_info["macro_distribution"]
        
        # Рассчитываем граммы макронутриентов
        macros_in_grams = {
            "carbs": int((daily_calories * macro_dist["carbs"]) / 4),  # 4 калории на грамм углеводов
            "protein": int((daily_calories * macro_dist["protein"]) / 4),  # 4 калории на грамм белка
            "fat": int((daily_calories * macro_dist["fat"]) / 9)  # 9 калорий на грамм жира
        }
        
        # Формируем план питания
        nutrition_plan = {
            "daily_calories": int(daily_calories),
            "macronutrient_distribution": macro_dist,
            "macros_in_grams": macros_in_grams,
            "recommended_foods": goal_info["recommended_foods"],
            "foods_to_avoid": goal_info["foods_to_avoid"],
            "dietary_restrictions": dietary_restrictions,
            "preferred_cuisines": preferred_cuisines,
            "cuisine_recommendations": self._get_cuisine_recommendations(preferred_cuisines),
            "meal_plan": self._generate_meal_plan(daily_calories, macros_in_grams, 
                                                dietary_restrictions, preferred_cuisines),
            "recommendations": self._generate_nutrition_recommendations(nutrition_goal, 
                                                                     dietary_restrictions),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return nutrition_plan
    
    def _get_cuisine_recommendations(self, preferred_cuisines: List[str]) -> List[Dict]:
        """
        Получение рекомендаций по кухням
        
        Args:
            preferred_cuisines (List[str]): Предпочтительные кухни
            
        Returns:
            List[Dict]: Рекомендации по кухням
        """
        recommendations = []
        
        for cuisine in preferred_cuisines:
            if cuisine in self.cuisine_info:
                cuisine_info = self.cuisine_info[cuisine].copy()
                cuisine_info["name"] = cuisine
                recommendations.append(cuisine_info)
        
        return recommendations
    
    def _generate_meal_plan(self, daily_calories: float, macros_in_grams: Dict,
                          dietary_restrictions: List[str], preferred_cuisines: List[str]) -> List[Dict]:
        """
        Генерация плана питания на день
        
        Args:
            daily_calories (float): Дневная норма калорий
            macros_in_grams (Dict): Макронутриенты в граммах
            dietary_restrictions (List[str]): Диетические ограничения
            preferred_cuisines (List[str]): Предпочтительные кухни
            
        Returns:
            List[Dict]: План питания
        """
        # Простой пример плана питания на день
        meal_plan = [
            {
                "meal": "breakfast",
                "calories": int(daily_calories * 0.25),
                "description": "Сбалансированный завтрак с белками и углеводами",
                "timing": "7:00-9:00",
                "sample_foods": self._get_sample_foods("breakfast", dietary_restrictions, preferred_cuisines)
            },
            {
                "meal": "lunch",
                "calories": int(daily_calories * 0.35),
                "description": "Основной обед с белками, овощами и углеводами",
                "timing": "12:00-14:00",
                "sample_foods": self._get_sample_foods("lunch", dietary_restrictions, preferred_cuisines)
            },
            {
                "meal": "dinner",
                "calories": int(daily_calories * 0.30),
                "description": "Легкий ужин с белками и овощами",
                "timing": "18:00-20:00",
                "sample_foods": self._get_sample_foods("dinner", dietary_restrictions, preferred_cuisines)
            },
            {
                "meal": "snacks",
                "calories": int(daily_calories * 0.10),
                "description": "Полезные перекусы в течение дня",
                "timing": "10:00, 15:00, 17:00",
                "sample_foods": self._get_sample_foods("snacks", dietary_restrictions, preferred_cuisines)
            }
        ]
        
        return meal_plan
    
    def _get_sample_foods(self, meal_type: str, dietary_restrictions: List[str], 
                         preferred_cuisines: List[str]) -> List[str]:
        """
        Получение примеров продуктов для приема пищи
        
        Args:
            meal_type (str): Тип приема пищи
            dietary_restrictions (List[str]): Диетические ограничения
            preferred_cuisines (List[str]): Предпочтительные кухни
            
        Returns:
            List[str]: Примеры продуктов
        """
        # Базовые примеры продуктов (в реальной системе это будет более сложным)
        base_foods = {
            "breakfast": ["oatmeal", "eggs", "fruit", "yogurt"],
            "lunch": ["chicken", "rice", "vegetables", "salad"],
            "dinner": ["fish", "quinoa", "steamed_vegetables"],
            "snacks": ["nuts", "fruit", "protein_bar"]
        }
        
        foods = base_foods.get(meal_type, [])
        
        # Применяем диетические ограничения
        filtered_foods = self._apply_dietary_restrictions(foods, dietary_restrictions)
        
        return filtered_foods
    
    def _apply_dietary_restrictions(self, foods: List[str], 
                                  dietary_restrictions: List[str]) -> List[str]:
        """
        Применение диетических ограничений к списку продуктов
        
        Args:
            foods (List[str]): Список продуктов
            dietary_restrictions (List[str]): Диетические ограничения
            
        Returns:
            List[str]: Отфильтрованный список продуктов
        """
        # В реальной системе здесь будет более сложная логика
        # Для демонстрации просто возвращаем исходный список
        return foods
    
    def _generate_nutrition_recommendations(self, nutrition_goal: str, 
                                          dietary_restrictions: List[str]) -> List[str]:
        """
        Генерация рекомендаций по питанию
        
        Args:
            nutrition_goal (str): Цель питания
            dietary_restrictions (List[str]): Диетические ограничения
            
        Returns:
            List[str]: Рекомендации по питанию
        """
        recommendations = []
        
        if nutrition_goal == "weight_loss":
            recommendations.extend([
                "Создайте дефицит калорий в 500 калорий в день для потери 0.5 кг в неделю",
                "Увеличьте потребление белка для сохранения мышечной массы",
                "Пейте достаточное количество воды (2-3 литра в день)",
                "Ешьте больше клетчатки для улучшения сытости"
            ])
        elif nutrition_goal == "muscle_gain":
            recommendations.extend([
                "Создайте избыток калорий в 300-500 калорий в день для набора мышечной массы",
                "Увеличьте потребление белка до 1.6-2.2 г на кг веса тела",
                "Употребляйте углеводы до и после тренировок",
                "Регулярно принимайте пищу каждые 3-4 часа"
            ])
        elif nutrition_goal == "endurance":
            recommendations.extend([
                "Увеличьте потребление углеводов до 6-10 г на кг веса тела в день",
                "Употребляйте углеводы во время длительных тренировок (>60 минут)",
                "Поддерживайте гидратацию с электролитами",
                "Принимайте антиоксиданты для восстановления"
            ])
        else:
            recommendations.extend([
                "Следуйте принципам сбалансированного питания",
                "Ешьте разнообразные продукты для получения всех необходимых нутриентов",
                "Контролируйте размеры порций",
                "Ограничьте потребление обработанных продуктов"
            ])
        
        # Добавляем рекомендации по диетическим ограничениям
        if "vegetarian" in dietary_restrictions:
            recommendations.append("Убедитесь, что получаете достаточное количество белка из растительных источников")
        if "vegan" in dietary_restrictions:
            recommendations.append("Контролируйте уровень витамина B12, железа и цинка")
        if "gluten_free" in dietary_restrictions:
            recommendations.append("Выбирайте безглютеновые злаки, такие как киноа, гречка и рис")
        
        return recommendations