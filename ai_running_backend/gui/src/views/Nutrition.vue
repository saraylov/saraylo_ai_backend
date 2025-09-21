<template>
  <div class="nutrition-view">
    <div class="container">
      <div class="header">
        <h1>Питание</h1>
        <p>Персонализированный план питания на основе ваших целей и данных тренировок</p>
      </div>

      <!-- Nutrition Preferences Section -->
      <div class="card glass-effect">
        <h2>Предпочтения питания</h2>
        <div class="preferences-form">
          <div class="form-group">
            <label for="nutrition-goal">Цель питания:</label>
            <select id="nutrition-goal" v-model="preferences.nutritionGoal">
              <option value="general_health">Общее здоровье</option>
              <option value="weight_loss">Похудение</option>
              <option value="muscle_gain">Набор мышечной массы</option>
              <option value="endurance">Выносливость</option>
            </select>
          </div>

          <div class="form-group">
            <label>Диетические ограничения:</label>
            <div class="checkbox-group">
              <label v-for="restriction in dietaryRestrictions" :key="restriction.value">
                <input 
                  type="checkbox" 
                  :value="restriction.value" 
                  v-model="preferences.dietaryRestrictions"
                >
                {{ restriction.label }}
              </label>
            </div>
          </div>

          <div class="form-group">
            <label>Предпочитаемая кухня:</label>
            <div class="checkbox-group">
              <label v-for="cuisine in cuisines" :key="cuisine.value">
                <input 
                  type="checkbox" 
                  :value="cuisine.value" 
                  v-model="preferences.preferredCuisines"
                >
                {{ cuisine.label }}
              </label>
            </div>
          </div>

          <button @click="savePreferences" class="btn btn-primary">
            Сохранить предпочтения
          </button>
        </div>
      </div>

      <!-- Nutrition Plan Section -->
      <div class="card glass-effect" v-if="nutritionPlan">
        <div class="plan-header">
          <h2>Ваш персональный план питания</h2>
          <button @click="generatePlan" class="btn btn-secondary">
            Обновить план
          </button>
        </div>

        <div class="plan-summary">
          <div class="summary-item">
            <h3>{{ nutritionPlan.daily_calories }} ккал</h3>
            <p>Ежедневная норма калорий</p>
          </div>
          <div class="summary-item">
            <h3>{{ nutritionPlan.macros_in_grams.protein }}г</h3>
            <p>Белки</p>
          </div>
          <div class="summary-item">
            <h3>{{ nutritionPlan.macros_in_grams.carbs }}г</h3>
            <p>Углеводы</p>
          </div>
          <div class="summary-item">
            <h3>{{ nutritionPlan.macros_in_grams.fat }}г</h3>
            <p>Жиры</p>
          </div>
        </div>

        <!-- Meal Plan -->
        <div class="meal-plan">
          <h3>План питания на день</h3>
          <div class="meal" v-for="(meal, index) in nutritionPlan.meal_plan" :key="index">
            <div class="meal-header">
              <h4>{{ getMealName(meal.meal) }}</h4>
              <span>{{ meal.timing }}</span>
            </div>
            <p>{{ meal.description }}</p>
            <div class="sample-foods">
              <span 
                v-for="(food, foodIndex) in meal.sample_foods" 
                :key="foodIndex" 
                class="food-tag"
              >
                {{ food }}
              </span>
            </div>
            <div class="calories">{{ meal.calories }} ккал</div>
          </div>
        </div>

        <!-- Recommendations -->
        <div class="recommendations" v-if="nutritionPlan.recommendations.length > 0">
          <h3>Рекомендации</h3>
          <ul>
            <li v-for="(rec, index) in nutritionPlan.recommendations" :key="index">
              {{ rec }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Loading State -->
      <div class="loading" v-if="loading">
        <div class="spinner"></div>
        <p>Генерируем ваш персональный план питания...</p>
      </div>

      <!-- Error Message -->
      <div class="error-message" v-if="error">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'
import { useStore } from 'vuex'
import { computed, onMounted, reactive, ref } from 'vue'

export default {
  name: 'Nutrition',
  setup() {
    const store = useStore()
    const loading = ref(false)
    const error = ref('')
    
    const preferences = reactive({
      nutritionGoal: 'general_health',
      dietaryRestrictions: [],
      preferredCuisines: []
    })
    
    const nutritionPlan = ref(null)
    
    const dietaryRestrictions = [
      { value: 'vegetarian', label: 'Вегетарианство' },
      { value: 'vegan', label: 'Веганство' },
      { value: 'gluten_free', label: 'Без глютена' },
      { value: 'dairy_free', label: 'Без лактозы' }
    ]
    
    const cuisines = [
      { value: 'mediterranean', label: 'Средиземноморская' },
      { value: 'asian', label: 'Азиатская' },
      { value: 'american', label: 'Американская' }
    ]
    
    const userProfile = computed(() => store.state.userProfile)
    const nutritionSettings = computed(() => store.state.nutritionSettings)
    
    // Load saved nutrition settings
    onMounted(() => {
      preferences.nutritionGoal = nutritionSettings.value.goal
      preferences.dietaryRestrictions = [...nutritionSettings.value.restrictions]
      preferences.preferredCuisines = [...nutritionSettings.value.cuisines]
    })
    
    const getMealName = (mealType) => {
      const mealNames = {
        'breakfast': 'Завтрак',
        'lunch': 'Обед',
        'dinner': 'Ужин',
        'snacks': 'Перекусы'
      }
      return mealNames[mealType] || mealType
    }
    
    const savePreferences = async () => {
      try {
        loading.value = true
        error.value = ''
        
        const payload = {
          user_id: userProfile.value.user_id,
          nutrition_goal: preferences.nutritionGoal
        }
        
        await api.setNutritionPreferences(payload)
        
        // Save to store
        store.commit('SET_NUTRITION_SETTINGS', {
          goal: preferences.nutritionGoal,
          restrictions: [...preferences.dietaryRestrictions],
          cuisines: [...preferences.preferredCuisines]
        })
        
        // After saving preferences, generate a new plan
        await generatePlan()
      } catch (err) {
        error.value = 'Ошибка при сохранении предпочтений питания'
        console.error('Error saving nutrition preferences:', err)
      } finally {
        loading.value = false
      }
    }
    
    const generatePlan = async () => {
      try {
        loading.value = true
        error.value = ''
        
        const payload = {
          user_id: userProfile.value.user_id,
          session_id: 'current_session', // In a real app, this would be an actual session ID
          nutrition_goal: preferences.nutritionGoal,
          dietary_restrictions: preferences.dietaryRestrictions,
          preferred_cuisines: preferences.preferredCuisines
        }
        
        const response = await api.generateNutritionPlan(payload)
        nutritionPlan.value = response.data
      } catch (err) {
        error.value = 'Ошибка при генерации плана питания'
        console.error('Error generating nutrition plan:', err)
      } finally {
        loading.value = false
      }
    }
    
    return {
      preferences,
      nutritionPlan,
      loading,
      error,
      dietaryRestrictions,
      cuisines,
      getMealName,
      savePreferences,
      generatePlan
    }
  }
}
</script>

<style scoped>
.nutrition-view {
  padding: 20px 0;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header p {
  font-size: 1.1rem;
  opacity: 0.8;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.form-group select {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
}

.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-group input {
  margin-right: 8px;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.plan-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.summary-item {
  text-align: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.summary-item h3 {
  font-size: 1.5rem;
  margin-bottom: 5px;
  color: #00BFFF;
}

.meal-plan {
  margin-bottom: 30px;
}

.meal {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px;
}

.meal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.meal-header h4 {
  margin: 0;
  color: #00BFFF;
}

.meal-header span {
  background: rgba(0, 191, 255, 0.2);
  padding: 3px 8px;
  border-radius: 20px;
  font-size: 0.8rem;
}

.sample-foods {
  margin: 10px 0;
}

.food-tag {
  display: inline-block;
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 10px;
  border-radius: 15px;
  margin-right: 5px;
  margin-bottom: 5px;
  font-size: 0.85rem;
}

.calories {
  font-weight: bold;
  color: #FF1493;
}

.recommendations ul {
  padding-left: 20px;
}

.recommendations li {
  margin-bottom: 10px;
  line-height: 1.5;
}

.loading {
  text-align: center;
  padding: 30px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top: 4px solid #00BFFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background: rgba(255, 0, 0, 0.2);
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  margin-top: 20px;
}
</style>