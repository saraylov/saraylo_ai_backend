<template>
  <div class="audio-assistant" v-if="isEnabled">
    <div class="assistant-controls">
      <button 
        @click="toggleAssistant" 
        :class="['btn', 'btn-toggle', { active: isAssistantActive }]"
        title="Включить/выключить аудио-ассистента"
      >
        <span class="icon">🔊</span>
        Аудио-ассистент
      </button>
      
      <button 
        v-if="isAssistantActive" 
        @click="holdToTalk" 
        @mouseup="stopHoldToTalk"
        @mouseleave="stopHoldToTalk"
        :class="['btn', 'btn-hold', { active: isListening }]"
        title="Удерживайте для разговора"
      >
        <span class="icon">🎤</span>
        {{ isListening ? 'Отпустите' : 'Удерживать' }}
      </button>
    </div>
    
    <div v-if="isAssistantActive" class="assistant-status">
      <div v-if="isSpeaking" class="status speaking">
        <span class="indicator"></span>
        Произношение...
      </div>
      <div v-else-if="isListening" class="status listening">
        <span class="indicator"></span>
        Слушаю...
      </div>
      <div v-else class="status ready">
        Готов к работе
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'AudioAssistant',
  setup() {
    const store = useStore()
    
    // Reactive state
    const isEnabled = ref(true)
    const isAssistantActive = ref(false)
    const isSpeaking = ref(false)
    const isListening = ref(false)
    const speechQueue = reactive([])
    
    // Get audio settings from store
    const audioSettings = computed(() => store.getters.audioSettings)
    
    // Check if Web Speech API is supported
    const isSupported = ref('speechSynthesis' in window && 'webkitSpeechRecognition' in window)
    
    let recognition = null
    
    // Initialize speech recognition if available
    if ('webkitSpeechRecognition' in window) {
      recognition = new webkitSpeechRecognition()
      recognition.continuous = false
      recognition.interimResults = false
      recognition.lang = 'ru-RU'
      
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript
        console.log('Recognized speech:', transcript)
        // Process the recognized speech
        processSpeechInput(transcript)
      }
      
      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error)
        isListening.value = false
      }
      
      recognition.onend = () => {
        isListening.value = false
      }
    }
    
    // Toggle assistant on/off
    const toggleAssistant = () => {
      isAssistantActive.value = !isAssistantActive.value
    }
    
    // Hold to talk functionality
    const holdToTalk = () => {
      if (!isAssistantActive.value || !recognition) return
      
      isListening.value = true
      recognition.lang = audioSettings.value.language
      recognition.start()
    }
    
    // Stop hold to talk
    const stopHoldToTalk = () => {
      if (!isListening.value) return
      
      isListening.value = false
      if (recognition) {
        recognition.stop()
      }
    }
    
    // Process speech input
    const processSpeechInput = (text) => {
      // In a real app, this would send the text to your backend for processing
      console.log('Processing speech input:', text)
      
      // Provide a sample response
      speak(`Вы сказали: ${text}. Это демонстрация функции распознавания речи.`)
    }
    
    // Speak text using Web Speech API
    const speak = (text) => {
      if (!isEnabled.value || !isAssistantActive.value || !isSupported.value) return
      
      const utterance = new SpeechSynthesisUtterance(text)
      
      // Configure voice settings from store
      utterance.rate = audioSettings.value.voiceRate
      utterance.volume = audioSettings.value.voiceVolume
      utterance.lang = audioSettings.value.language
      
      // Set voice based on preference
      speechSynthesis.getVoices().forEach(voice => {
        if (
          (audioSettings.value.voiceType === 'female' && voice.name.includes('female')) ||
          (audioSettings.value.voiceType === 'male' && voice.name.includes('male'))
        ) {
          utterance.voice = voice
        }
      })
      
      // Event handlers
      utterance.onstart = () => {
        isSpeaking.value = true
      }
      
      utterance.onend = () => {
        isSpeaking.value = false
        processQueue()
      }
      
      utterance.onerror = (event) => {
        console.error('Speech synthesis error:', event.error)
        isSpeaking.value = false
        processQueue()
      }
      
      // Add to queue and start speaking
      speechQueue.push(utterance)
      if (!isSpeaking.value) {
        processQueue()
      }
    }
    
    // Process speech queue
    const processQueue = () => {
      if (speechQueue.length > 0 && !isSpeaking.value) {
        const utterance = speechQueue.shift()
        speechSynthesis.speak(utterance)
      }
    }
    
    // Cleanup on unmount
    onUnmounted(() => {
      if (isSpeaking.value) {
        speechSynthesis.cancel()
      }
    })
    
    // Expose methods for external use
    const sayHello = () => {
      speak('Привет! Я ваш аудио-ассистент. Как я могу вам помочь?')
    }
    
    const provideWorkoutUpdate = (data) => {
      speak(`Текущая нагрузка: ${data.load}%. Уровень усталости: ${data.fatigue}.`)
    }
    
    const provideRecommendation = (recommendation) => {
      speak(`Рекомендация: ${recommendation}`)
    }
    
    return {
      isEnabled,
      isAssistantActive,
      isSpeaking,
      isListening,
      isSupported,
      toggleAssistant,
      holdToTalk,
      stopHoldToTalk,
      speak,
      sayHello,
      provideWorkoutUpdate,
      provideRecommendation
    }
  }
}
</script>

<style scoped>
.audio-assistant {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.assistant-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.btn-toggle.active {
  background: linear-gradient(45deg, #00BFFF, #1E90FF);
}

.btn-hold.active {
  background: linear-gradient(45deg, #FF4500, #FF6347);
}

.assistant-status {
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 10px 15px;
  text-align: center;
  font-size: 0.9rem;
}

.status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.speaking .indicator {
  background: #00BFFF;
}

.listening .indicator {
  background: #FF4500;
  animation: pulse 1.5s infinite;
}

.ready .indicator {
  background: #32CD32;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.4; }
  100% { opacity: 1; }
}
</style>