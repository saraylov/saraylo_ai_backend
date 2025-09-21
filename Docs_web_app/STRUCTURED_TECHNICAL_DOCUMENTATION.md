# SARAYLO - Квантовый Беговой Тренер
## Структурированная техническая документация

## Содержание

1. [Обзор приложения](#обзор-приложения)
2. [Архитектура](#архитектура)
3. [Компоненты системы](#компоненты-системы)
4. [Интеграции API](#интеграции-api)
5. [Реализация функциональности тренировок](#реализация-функциональности-тренировок)
6. [Разработка и настройка](#разработка-и-настройка)
7. [Развертывание](#развертывание)
8. [Мобильная разработка](#мобильная-разработка)
9. [Безопасность](#безопасность)
10. [Документация для пользователей](#документация-для-пользователей)
11. [Решение проблем](#решение-проблем)

---

## Обзор приложения

SARAYLO - это современное веб-приложение с авторизацией через Telegram, использующее стиль "жидкое стекло" (glassmorphism) и цветовую схему Miami Hit. Приложение представляет собой систему для спорта и фитнеса, основанную на AI-технологии, которая совместно с пользователем создает революцию в восприятии спорта и фитнеса.

### Основные функции
- **Авторизация**: Через Telegram Web App и демо-режим для тестирования
- **Тренировки**: Оценочные тренировки и реальные тренировки с GPS-трекингом
- **Мониторинг здоровья**: Отслеживание показателей здоровья и анализ данных активности

### Техническая архитектура
- **Фронтенд**: Svelte 4 с TypeScript и Vite 5
- **Дизайн**: Glassmorphism с цветовой схемой Miami Hit
- **Интеграции**: Telegram Web App API, Mapbox GL JS, Web Speech API
- **Мобильная версия**: Сборка через Capacitor для Android и iOS

---

## Архитектура

### Компонентная структура
```
App.svelte
├── Header.svelte
├── MainContent.svelte
│   ├── Dashboard.svelte
│   ├── Training.svelte
│   │   ├── WorkoutButton.svelte
│   │   ├── CircularProgressBar.svelte
│   │   └── BottomNav.svelte
│   ├── AssessmentTraining.svelte
│   ├── Health.svelte
│   ├── Devices.svelte
│   ├── Profile.svelte
│   └── Settings.svelte
└── BottomNav.svelte
    └── WorkoutButton.svelte
```

### Центральное хранилище данных
Центральный элемент управления состоянием тренировки - Workout Store (src/utils/workoutStore.ts):
```typescript
interface WorkoutData {
  startTime: number | null;
  elapsedTime: number;
  totalDistance: number;
  currentSpeed: number;
  averageSpeed: number;
  maxSpeed: number;
  isWorkoutActive: boolean;
  workoutState: 'idle' | 'running' | 'paused';
  currentPosition: GeolocationPosition | null;
  locationError: string | null;
  isLocating: boolean;
  watchId: number | null;
}
```

### Состояния приложения

#### Жизненный цикл тренировки
1. **Idle State**: Пользователь в приложении, кнопка "Старт" активна
2. **Running State**: Тренировка активна, геолокация отслеживается
3. **Paused State**: Тренировка на паузе, геолокация приостановлена

#### Управление состоянием
Использование Svelte Stores для реактивного управления:
```typescript
// Создание store
export const workoutStore = writable<WorkoutData>(initialWorkoutData);

// Подписка на изменения
workoutStore.subscribe(data => {
  // Обновление UI
});

// Обновление данных
workoutStore.update(data => ({
  ...data,
  ...newStats
}));
```

---

## Компоненты системы

### WorkoutButton.svelte
Компонент кнопки тренировки с уникальной механикой удержания:
- **Старт** (синий градиент): Удержание 2.5 секунды для запуска
- **Стоп** (красный градиент): Немедленная остановка
- **Пауза** (желтый градиент): Немедленная пауза
- **Продолжить** (зеленый градиент): Немедленное возобновление

### Training.svelte
Основной компонент тренировки с интеграцией всех систем:
- Инициализация Mapbox карты
- Отслеживание геолокации
- Сбор статистики тренировки
- Интеграция с аудио-ассистентом

### AssessmentTraining.svelte
Компонент оценочной тренировки:
- 5 зон интенсивности (синяя, зеленая, желтая, оранжевая, красная)
- Сбор данных скорости во время тренировки
- Расчет персональных зон интенсивности

### CircularProgressBar.svelte
SVG-компонент визуальной индикации прогресса:
```svelte
<svg viewBox="0 0 120 120">
  <circle class="background" cx="60" cy="60" r="54" />
  <circle 
    class="progress" 
    cx="60" 
    cy="60" 
    r="54"
    stroke-dasharray="{circumference}"
    stroke-dashoffset="{offset}"
  />
</svg>
```

---

## Интеграции API

### Telegram Web App API
Интеграция с Telegram для авторизации:
```typescript
interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code: string;
  is_premium?: boolean;
}
```

#### Валидация данных
```typescript
function validateTelegramData(initData: string, token: string): boolean {
  // Создание секретного ключа
  const secret = crypto.createHmac('sha256', 'WebAppData')
    .update(token)
    .digest();
    
  // Парсинг параметров
  const params = new URLSearchParams(initData);
  const hash = params.get('hash');
  params.delete('hash');
  
  // Сортировка параметров
  const sortedParams = [...params.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}=${value}`)
    .join('\n');
    
  // Вычисление хэша
  const calculatedHash = crypto
    .createHmac('sha256', secret)
    .update(sortedParams)
    .digest('hex');
    
  return calculatedHash === hash;
}
```

### Mapbox GL JS API

#### Инициализация карты
```typescript
import mapboxgl from 'mapbox-gl';

// Установка токена доступа
mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';

// Создание карты
const map = new mapboxgl.Map({
  container: 'map-container', // ID элемента контейнера
  style: 'mapbox://styles/mapbox/streets-v12', // Стиль карты
  center: [30.3158, 59.9343], // Центр карты [долгота, широта]
  zoom: 10 // Уровень масштабирования
});
```

#### Работа с линиями (полилиниями)
Добавление источника данных:
```typescript
// Создание GeoJSON данных
const geojson = {
  type: 'Feature',
  properties: {},
  geometry: {
    type: 'LineString',
    coordinates: [
      [30.3158, 59.9343],
      [30.3258, 59.9443],
      [30.3358, 59.9543]
    ]
  }
};

// Добавление источника данных
map.addSource('route', {
  type: 'geojson',
  data: geojson
});
```

### Web Speech API

#### Синтез речи
Базовое использование:
```typescript
function speakText(text: string): void {
  // Проверка поддержки браузером
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Настройка параметров
    utterance.lang = 'ru-RU';     // Язык
    utterance.rate = 1.0;         // Скорость речи
    utterance.pitch = 1.0;        // Тональность
    utterance.volume = 1.0;       // Громкость
    
    // Воспроизведение
    window.speechSynthesis.speak(utterance);
  }
}
```

#### Расширенная реализация с очередью
```typescript
class AudioAssistant {
  private speechQueue: SpeechSynthesisUtterance[] = [];
  private isSpeaking = false;
  
  speak(text: string): void {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ru-RU';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    
    // Обработчики событий
    utterance.onstart = () => {
      this.isSpeaking = true;
    };
    
    utterance.onend = () => {
      this.isSpeaking = false;
      this.processQueue();
    };
    
    utterance.onerror = (event) => {
      console.error('Ошибка синтеза речи:', event.error);
      this.isSpeaking = false;
      this.processQueue();
    };
    
    this.speechQueue.push(utterance);
    this.processQueue();
  }
  
  private processQueue(): void {
    if (this.isSpeaking || this.speechQueue.length === 0) {
      return;
    }
    
    const utterance = this.speechQueue.shift();
    if (utterance) {
      window.speechSynthesis.speak(utterance);
    }
  }
  
  // Проверка поддержки
  isSupported(): boolean {
    return 'speechSynthesis' in window;
  }
}
```

### Capacitor Plugins API

#### Геолокация (@capacitor/geolocation)
Получение текущей позиции:
```typescript
import { Geolocation } from '@capacitor/geolocation';

async function getCurrentPosition(): Promise<GeolocationPosition> {
  const coordinates = await Geolocation.getCurrentPosition({
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 3000
  });
  
  return coordinates;
}
```

---

## Реализация функциональности тренировок

### Удержание кнопки (2.5 секунды)
- При touchstart/mousedown запускается таймер
- Каждые 50 мс обновляется визуальный прогресс
- При touchend/mouseup до завершения 2.5 секунд прогресс сбрасывается
- При достижении 2.5 секунд выполняется соответствующее действие

### Визуальная индикация
- Использование SVG для создания кругового прогресс-бара
- Динамическое вычисление параметров stroke-dasharray и stroke-dashoffset
- Плавная анимация заполнения
- Разные цвета для разных состояний (синий - старт, красный - стоп, желтый - пауза, зеленый - продолжить)

### Процессы тренировки

#### Сбор данных
- Время: отсчет с момента запуска через performance.now() с точностью до 100 мс
- Дистанция и скорость: вычисляются на основе координат GPS/Glonass
- Расстояние рассчитывается по формуле Хаверсина между последовательными точками
- Скорость — как производная дистанции по времени
- Геолокация: данные обновляются каждые 1-2 секунды

#### Аудио-ассистент
- Реализация через Web Speech API (SpeechSynthesis)
- Для Android-версии используется capacitor-audio для фонового воспроизведения
- Генерация голосовых подсказок ("Пройдено 500 метров", "Скорость 12 км/ч")

#### Трекинг пути на Mapbox
- Интеграция Mapbox GL JS для отображения реального маршрута
- Построение polyline на карте с динамическим обновлением координат
- Использование capacitor-maps для совместимости с Android-устройствами

#### Инициализация локации
- Запрос разрешений на доступ к геолокации только при активации тренировки
- Блокировка запросов к геоданным до момента запуска тренировки
- Использование navigator.geolocation.watchPosition() после запуска

### Мобильные особенности (Capacitor)
- Компиляция Svelte-приложения в Android через Capacitor
- Использование @capacitor/geolocation для точного GPS/Glonass-трекинга
- @capacitor/background-task для поддержки фоновых процессов
- @capacitor/permissions для динамического запроса разрешений
- Адаптивный CSS-дизайн и использование touch-событий

---

## Разработка и настройка

### Требования к системе
- Node.js версии 20 или выше
- npm (поставляется с Node.js)
- Git (для управления версиями)
- Android Studio (для Android)
- Xcode (для iOS, только на macOS)

### Установка и настройка

#### Клонирование репозитория
```bash
git clone https://github.com/saraylov/saraylo_web_app.git
cd saraylo_web_app
```

#### Установка зависимостей
```bash
npm install
```

#### Конфигурация переменных окружения
1. Скопируйте файл .env.example в `.env`:
   ```bash
   cp .env.example .env
   ```

2. Откройте файл .env и замените `your_telegram_bot_token_here` на реальный токен вашего Telegram бота

### Структура проекта
```
saraylo_web_app/
├── src/                    # Исходный код приложения
│   ├── components/         # Компоненты Svelte
│   ├── utils/              # Утилиты и хранилища
│   ├── styles/             # Стили CSS
│   ├── assets/             # Статические ресурсы
│   ├── App.svelte          # Главный компонент приложения
│   ├── main.ts             # Точка входа в приложение
│   └── app.css             # Глобальные статили приложения
├── public/                 # Публичные файлы
├── Documentation/          # Документация проекта
├── android/                # Android проект (Capacitor)
├── ios/                    # iOS проект (Capacitor)
├── dist/                   # Сборка для веба
├── distWebAuth/            # Сборка с авторизацией
├── .env.example            # Пример файла переменных окружения
├── .gitignore              # Файл игнорирования Git
├── Dockerfile              # Конфигурация Docker
├── docker-compose.yml      # Конфигурация Docker Compose
├── index.html              # Главная HTML страница
├── package.json            # Конфигурация npm
├── tsconfig.json           # Конфигурация TypeScript
├── vite.config.ts          # Конфигурация Vite
└── viteWebAuth.config.ts   # Конфигурация Vite для WebAuth
```

### Локальный запуск
```bash
# Основное приложение
npm run dev

# Приложение с авторизацией через Telegram
npm run dev:webauth

# Использование PowerShell скриптов
.\run_dev.ps1
```

### Сборка для продакшена
```bash
# Сборка основного приложения
npm run build

# Сборка приложения с авторизацией
npm run build:webauth

# Предварительный просмотр сборки
npm run preview
npm run preview:webauth
```

### Лучшие практики

#### Структура кода
1. Разделяйте логику и представление
2. Используйте строгую типизацию
3. Комментируйте сложную логику
4. Следуйте единому стилю кодирования

#### Производительность
1. Минимизируйте количество DOM элементов
2. Используйте реактивные переменные только когда это необходимо
3. Избегайте тяжелых вычислений в компонентах
4. Оптимизируйте анимации (предпочтительно CSS вместо JavaScript)

#### Безопасность
1. Не храните чувствительные данные в коде
2. Используйте переменные окружения для токенов
3. Валидируйте все входные данные
4. Следите за обновлениями зависимостей

---

## Развертывание

### Развертывание на GitHub Pages

#### Подготовка
1. Убедитесь, что у вас установлена последняя версия Node.js (20 или выше)
2. Установите зависимости:
   ```bash
   npm install
   ```

3. Соберите приложение:
   ```bash
   npm run build:webauth
   ```

#### Ручное развертывание
1. Закоммитьте содержимое папки `distWebAuth` в ваш репозиторий:
   ```bash
   git add distWebAuth
   git commit -m "Добавление веб-приложения с авторизацией через Telegram"
   git push origin main
   ```

2. Перейдите в настройки репозитория на GitHub:
   - Откройте вкладку "Settings"
   - Прокрутите до раздела "Pages"

3. Настройте GitHub Pages:
   - В разделе "Source" выберите "Deploy from a branch"
   - В выпадающем списке "Branch" выберите ветку (обычно `main`)
   - В поле "Folder" выберите `/distWebAuth`
   - Нажмите "Save"

#### Автоматическое развертывание с GitHub Actions
Создайте файл `.github/workflows/deploy-webauth.yml`:
```yaml
name: Deploy WebAuth App to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build
        run: npm run build:webauth
        
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./distWebAuth
```

### Docker развертывание

#### Локальная сборка и запуск
1. Соберите и запустите приложение:
   ```bash
   docker-compose up -d
   ```

2. Откройте браузер и перейдите по адресу: http://localhost:3003

#### Остановка приложения
```bash
docker-compose down
```

---

## Мобильная разработка

### Подготовка
1. Убедитесь, что установлены необходимые инструменты:
   - Android Studio для Android
   - Xcode для iOS (только на macOS)
   - JDK 11 или выше

2. Установите зависимости:
   ```bash
   npm install
   ```

3. Соберите веб-приложение:
   ```bash
   npm run build
   ```

4. Синхронизируйте веб-ресурсы с нативными проектами:
   ```bash
   npm run cap:sync
   ```

### Работа с Android
1. Добавьте Android платформу (если еще не добавлена):
   ```bash
   npm run cap:add:android
   ```

2. Откройте проект в Android Studio:
   ```bash
   npm run cap:open:android
   ```

3. Для запуска на устройстве или эмуляторе:
   ```bash
   npm run cap:run:android
   ```

### Разрешения для мобильных приложений
Для корректной работы мобильного приложения на Android были добавлены необходимые разрешения в файл `android/app/src/main/AndroidManifest.xml`:
- `ACCESS_COARSE_LOCATION` и `ACCESS_FINE_LOCATION` - для определения местоположения
- `ACCESS_BACKGROUND_LOCATION` - для работы с геолокацией в фоновом режиме
- `POST_NOTIFICATIONS` - для отправки уведомлений
- `WAKE_LOCK` и `SCHEDULE_EXACT_ALARM` - для фоновых задач
- `ACCESS_NETWORK_STATE` - для проверки состояния сети

---

## Безопасность

### Переменные окружения
- Токен Telegram хранится в .env файле
- .env добавлен в .gitignore для безопасности
- Использование .env.example как шаблона

### Валидация данных
- Проверка подписи данных от Telegram
- Использование HMAC-SHA256 для валидации
- Ограничение по времени действия данных

### Защита токенов
Переменные окружения:
```bash
# .env (добавлен в .gitignore)
VITE_TELEGRAM_TOKEN=ваш_токен_здесь
VITE_MAPBOX_TOKEN=ваш_токен_здесь
```

Пример .env.example:
```bash
# .env.example (в репозитории)
VITE_TELEGRAM_TOKEN=your_telegram_token_here
VITE_MAPBOX_TOKEN=your_mapbox_token_here
```

---

## Документация для пользователей

### Начало работы

#### Авторизация
Приложение предлагает два способа входа:
1. **Авторизация через Telegram**: Откройте приложение через Telegram Web App и подтвердите авторизацию
2. **Демо-режим**: Нажмите кнопку "Демо-режим" для тестирования функциональности без сохранения данных

#### Интерфейс приложения
Приложение имеет интуитивно понятный интерфейс с навигацией в нижней части экрана:
- **Главная**: Обзор приложения и быстрый доступ к функциям
- **Тренировки**: Основной экран для отслеживания тренировок
- **Здоровье**: Мониторинг показателей здоровья
- **Устройства**: Управление подключенными устройствами
- **Профиль**: Настройки профиля и приложения

### Тренировки

#### Оценочная тренировка
Перед началом реальных тренировок рекомендуется пройти оценочную тренировку для определения персональных зон интенсивности:
1. Перейдите на экран "Тренировки"
2. Выберите "Оценочная тренировка"
3. Следуйте инструкциям аудио-ассистента:
   - Подготовка (6 минут синяя зона)
   - Легкая нагрузка (5 минут зеленая зона)
   - Умеренная нагрузка (5 минут желтая зона)
   - Высокая нагрузка (3 минуты оранжевая зона)
   - Максимальная нагрузка (1 минута красная зона)

#### Реальные тренировки
1. Перейдите на экран "Тренировки"
2. Нажмите и удерживайте кнопку "Старт" в течение 2.5 секунд
3. Дождитесь определения местоположения
4. Начните движение

#### Управление тренировкой
- **Пауза**: Нажмите кнопку "Пауза" для временной остановки тренировки
- **Продолжить**: Нажмите кнопку "Продолжить" для возобновления тренировки
- **Стоп**: Нажмите кнопку "Стоп" для завершения тренировки

### Аудио-ассистент
Приложение предоставляет голосовые подсказки во время тренировки:
- Уведомления о начале и завершении тренировки
- Информация о текущих показателях (время, дистанция, скорость)
- Напоминания о смене зон интенсивности (во время оценочной тренировки)

Для отключения аудио-ассистента:
1. Перейдите в "Профиль"
2. Выберите "Настройки"
3. Отключите опцию "Аудио-ассистент"

### Мобильное приложение
Мобильное приложение доступно для Android (через Google Play Store) и iOS (через App Store) с возможностью работы в фоновом режиме и точного определения местоположения.

---

## Решение проблем

### Белый экран при загрузке
1. Проверьте консоль браузера (F12) на наличие ошибок
2. Убедитесь, что пути к ресурсам в index.html начинаются с "./", а не с "/"
3. Проверьте, что все необходимые файлы были загружены на GitHub Pages

### Ошибки загрузки ресурсов (404)
1. Убедитесь, что папка `distWebAuth` содержит все необходимые файлы
2. Проверьте, что GitHub Pages настроен на правильную папку
3. Убедитесь, что в конфигурации Vite установлен параметр `base: './'`

### Проблемы с маршрутизацией
Если вы используете клиентскую маршрутизацию, создайте файл `404.html` в папке `distWebAuth` с содержимым `index.html`:
```bash
cp distWebAuth/index.html distWebAuth/404.html
```

### Ошибки геолокации
1. Проверьте разрешения на геолокацию в браузере
2. Убедитесь, что используется HTTPS (кроме localhost)
3. Проверьте настройки конфиденциальности устройства

### Проблемы с Telegram авторизацией
1. Убедитесь, что токен бота установлен в переменных окружения
2. Проверьте, что Web App URL правильно настроен в @BotFather
3. Убедитесь, что приложение открывается внутри Telegram

### Мобильные проблемы
#### Android
1. **Gradle sync failed**: Попробуйте "File" → "Sync Project with Gradle Files" в Android Studio
2. **Build errors**: Проверьте, что вы используете совместимую версию Android Studio и SDK
3. **Permission dialog not showing**: Убедитесь, что разрешения правильно объявлены в AndroidManifest.xml

#### iOS
1. **CocoaPods errors**: Выполните `cd ios && pod install` для обновления pods
2. **Signing errors**: Убедитесь, что ваша учетная запись Apple Developer правильно настроена в Xcode

### Частые ошибки и их решения
#### "Port already in use"
```bash
# Найдите процесс, использующий порт
netstat -ano | findstr :5173
# Завершите процесс
taskkill /PID <номер_процесса> /F
```

#### "Node.js not found"
1. Убедитесь, что Node.js установлен
2. Проверьте, что Node.js добавлен в PATH
3. Перезапустите терминал после установки

#### "npm install fails"
1. Проверьте подключение к интернету
2. Очистите кэш npm: `npm cache clean --force`
3. Попробуйте использовать другой реестр: `npm config set registry https://registry.npmjs.org/`