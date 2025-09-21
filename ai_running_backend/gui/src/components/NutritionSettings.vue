<template>
  <div class="nutrition-settings">
    <h3>Настройки питания</h3>
    <div class="settings-form">
      <div class="form-group">
        <label for="nutrition-goal">Цель питания:</label>
        <select id="nutrition-goal" v-model="nutritionSettings.goal">
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
              v-model="nutritionSettings.restrictions"
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
              v-model="nutritionSettings.cuisines"
            >
            {{ cuisine.label }}
          </label>
        </div>
      </div>

      <button @click="saveSettings" class="btn btn-primary">
        Сохранить настройки питания
      </button>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'NutritionSettings',
  setup() {
    const store = useStore()
    
    const nutritionSettings = reactive({
      goal: 'general_health',
      restrictions: [],
      cuisines: []
    })
    
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
    
    // Load settings from localStorage on mount
    onMounted(() => {
      const savedSettings = localStorage.getItem('nutritionSettings')
      if (savedSettings) {
        try {
          const parsedSettings = JSON.parse(savedSettings)
          Object.assign(nutritionSettings, parsedSettings)
        } catch (e) {
          console.error('Error parsing saved nutrition settings:', e)
        }
      }
    })
    
    const saveSettings = () => {
      // Save to localStorage
      localStorage.setItem('nutritionSettings', JSON.stringify(nutritionSettings))
      
      // In a real app, you might also save to a backend
      // store.commit('setNutritionSettings', nutritionSettings)
      
      console.log('Nutrition settings saved:', nutritionSettings)
    }
    
    return {
      nutritionSettings,
      dietaryRestrictions,
      cuisines,
      saveSettings
    }
  }
}
</script>

<style scoped>
.nutrition-settings {
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin-bottom: 20px;
}

.settings-form .form-group {
  margin-bottom: 20px;
}

.settings-form label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.settings-form select {
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
</style>