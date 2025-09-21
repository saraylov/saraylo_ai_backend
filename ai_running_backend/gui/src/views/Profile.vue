<template>
  <div class="profile-view">
    <div class="container">
      <div class="header">
        <h1>Профиль</h1>
        <p>Управление вашими персональными данными и настройками</p>
      </div>

      <div class="profile-content">
        <!-- User Info Card -->
        <div class="card glass-effect">
          <h2>Персональная информация</h2>
          <div class="profile-form">
            <div class="form-group">
              <label for="age">Возраст:</label>
              <input 
                id="age" 
                type="number" 
                v-model="profileData.age" 
                :disabled="!isEditing"
              >
            </div>

            <div class="form-group">
              <label for="gender">Пол:</label>
              <select 
                id="gender" 
                v-model="profileData.gender" 
                :disabled="!isEditing"
              >
                <option value="male">Мужской</option>
                <option value="female">Женский</option>
              </select>
            </div>

            <div class="form-group">
              <label for="weight">Вес (кг):</label>
              <input 
                id="weight" 
                type="number" 
                v-model="profileData.weight_kg" 
                :disabled="!isEditing"
              >
            </div>

            <div class="form-group">
              <label for="height">Рост (см):</label>
              <input 
                id="height" 
                type="number" 
                v-model="profileData.height_cm" 
                :disabled="!isEditing"
              >
            </div>

            <div class="form-group">
              <label for="fitness-level">Уровень фитнеса:</label>
              <select 
                id="fitness-level" 
                v-model="profileData.fitness_level" 
                :disabled="!isEditing"
              >
                <option value="1">Начинающий</option>
                <option value="2">Средний</option>
                <option value="3">Продвинутый</option>
              </select>
            </div>

            <div class="form-actions" v-if="isEditing">
              <button @click="saveProfile" class="btn btn-primary">Сохранить</button>
              <button @click="cancelEdit" class="btn btn-secondary">Отмена</button>
            </div>

            <div class="form-actions" v-else>
              <button @click="startEditing" class="btn btn-primary">Редактировать</button>
            </div>
          </div>
        </div>

        <!-- Calibration Data Card -->
        <div class="card glass-effect">
          <h2>Калибровочные данные</h2>
          <div class="calibration-info" v-if="!isEditingCalibration">
            <div class="calibration-grid">
              <div 
                v-for="(value, key) in calibrationData" 
                :key="key" 
                class="calibration-item"
              >
                <span class="percentage">{{ key }}</span>
                <span class="value">{{ value }} м/с</span>
              </div>
            </div>
            <button @click="editCalibration" class="btn btn-primary">Редактировать калибровку</button>
          </div>

          <div class="calibration-form" v-else>
            <div 
              v-for="(value, key) in calibrationData" 
              :key="key" 
              class="form-group"
            >
              <label :for="`cal-${key}`">{{ key }}:</label>
              <input 
                :id="`cal-${key}`" 
                type="number" 
                step="0.1" 
                v-model="calibrationData[key]"
              >
            </div>
            <div class="form-actions">
              <button @click="saveCalibration" class="btn btn-primary">Сохранить</button>
              <button @click="cancelCalibrationEdit" class="btn btn-secondary">Отмена</button>
            </div>
          </div>
        </div>

        <!-- Audio Assistant Settings -->
        <div class="card glass-effect">
          <h2>Настройки аудио-ассистента</h2>
          <router-link to="/audio-settings" class="btn btn-primary">
            Настроить аудио-ассистента
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'
import { useStore } from 'vuex'
import { computed, onMounted, reactive, ref } from 'vue'

export default {
  name: 'Profile',
  setup() {
    const store = useStore()
    const isEditing = ref(false)
    const isEditingCalibration = ref(false)
    
    // Create a copy of the profile data for editing
    const profileData = reactive({
      age: 30,
      gender: 'male',
      weight_kg: 70,
      height_cm: 175,
      fitness_level: 2
    })
    
    const originalProfileData = reactive({})
    
    const calibrationData = reactive({
      "10%": 2.8,
      "20%": 3.2,
      "30%": 3.6,
      "40%": 4.0,
      "50%": 4.4,
      "60%": 4.8,
      "70%": 5.2,
      "80%": 5.6,
      "90%": 6.0,
      "100%": 6.4
    })
    
    const originalCalibrationData = reactive({})
    
    const userProfile = computed(() => store.state.userProfile)
    
    // Update profile data when user profile changes
    onMounted(() => {
      Object.assign(profileData, userProfile.value)
      Object.assign(originalProfileData, userProfile.value)
      
      // Load calibration data
      loadCalibrationData()
    })
    
    const loadCalibrationData = async () => {
      try {
        const response = await api.getCalibrationData()
        Object.assign(calibrationData, response.data)
        Object.assign(originalCalibrationData, response.data)
      } catch (err) {
        console.error('Error loading calibration data:', err)
      }
    }
    
    const startEditing = () => {
      // Save current state for potential cancellation
      Object.assign(originalProfileData, profileData)
      isEditing.value = true
    }
    
    const cancelEdit = () => {
      // Restore original data
      Object.assign(profileData, originalProfileData)
      isEditing.value = false
    }
    
    const saveProfile = async () => {
      try {
        // In a real app, you would send the data to the backend
        await api.updateUserProfile(profileData)
        
        // Update the store
        store.commit('setUserProfile', profileData)
        
        isEditing.value = false
        
        // Show success message (in a real app)
        console.log('Profile saved successfully')
      } catch (err) {
        console.error('Error saving profile:', err)
        // Show error message (in a real app)
      }
    }
    
    const editCalibration = () => {
      // Save current state for potential cancellation
      Object.assign(originalCalibrationData, calibrationData)
      isEditingCalibration.value = true
    }
    
    const cancelCalibrationEdit = () => {
      // Restore original data
      Object.assign(calibrationData, originalCalibrationData)
      isEditingCalibration.value = false
    }
    
    const saveCalibration = async () => {
      try {
        // In a real app, you would send the data to the backend
        await api.saveCalibrationData(calibrationData)
        
        isEditingCalibration.value = false
        
        // Show success message (in a real app)
        console.log('Calibration data saved successfully')
      } catch (err) {
        console.error('Error saving calibration data:', err)
        // Show error message (in a real app)
      }
    }
    
    return {
      profileData,
      calibrationData,
      isEditing,
      isEditingCalibration,
      startEditing,
      cancelEdit,
      saveProfile,
      editCalibration,
      cancelCalibrationEdit,
      saveCalibration
    }
  }
}
</script>

<style scoped>
.profile-view {
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

.profile-form .form-group {
  margin-bottom: 20px;
}

.profile-form label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.profile-form input,
.profile-form select {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
}

.profile-form input:disabled,
.profile-form select:disabled {
  background: rgba(255, 255, 255, 0.05);
  opacity: 0.7;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.calibration-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.calibration-item {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 10px;
  text-align: center;
}

.percentage {
  display: block;
  font-weight: bold;
  color: #00BFFF;
  margin-bottom: 5px;
}

.value {
  display: block;
  font-size: 1.1rem;
}

.calibration-form .form-group {
  margin-bottom: 15px;
}

.calibration-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.calibration-form input {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
}
</style>