# Авторизация через Telegram

## Обзор

Система SARAYLO AI Workout поддерживает авторизацию через Telegram, что позволяет пользователям быстро и безопасно войти в приложение, используя свои учетные записи Telegram.

## Настройка Telegram бота

### 1. Создание бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания нового бота:
   - Введите имя бота (например, "Saraylo Workout")
   - Введите имя пользователя бота (например, `saraylov_bot`)
4. После создания бота вы получите **Token доступа** - сохраните его

### 2. Настройка домена

1. В [@BotFather](https://t.me/BotFather) отправьте команду `/setdomain`
2. Выберите своего бота
3. Введите домен вашего приложения: `https://07964add0b7e.ngrok-free.app/`

### 3. Настройка кнопки авторизации

1. В [@BotFather](https://t.me/BotFather) отправьте команду `/setmenubutton`
2. Выберите своего бота
3. Введите текст кнопки: "Авторизация"
4. Введите URL: `https://07964add0b7e.ngrok-free.app/login`

## Техническая реализация

### Виджет авторизации Telegram

В веб-приложении используется официальный виджет авторизации Telegram:

```html
<script async src="https://telegram.org/js/telegram-widget.js?22" 
        data-telegram-login="Saraylov_bot" 
        data-size="large" 
        data-radius="20" 
        data-auth-url="https://07964add0b7e.ngrok-free.app/auth/telegram"
        data-request-access="write">
</script>
```

### Параметры виджета

- `data-telegram-login`: Имя пользователя вашего бота (@Saraylov_bot)
- `data-auth-url`: URL для обработки данных авторизации
- `data-request-access`: Запрос доступа к данным пользователя

### Обработка авторизации на бэкенде

Бэкенд обрабатывает данные авторизации через эндпоинт `/auth/telegram`:

```python
@app.route('/auth/telegram', methods=['POST'])
def telegram_auth():
    # Получаем данные от Telegram
    telegram_data = request.form.to_dict()
    
    # Проверяем подлинность данных
    if verify_telegram_data(telegram_data):
        # Создаем JWT токен для пользователя
        token = jwt.encode({
            'user': telegram_data,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'access_token': token}), 200
    
    return jsonify({'error': 'Invalid data'}), 400
```

### Верификация данных Telegram

Для обеспечения безопасности все данные от Telegram проверяются с использованием HMAC-SHA256:

```python
def verify_telegram_data(telegram_data):
    received_hash = telegram_data.pop('hash', None)
    data_check_string = '\n'.join(sorted([f"{k}={v}" for k, v in telegram_data.items()]))
    secret_key = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(calculated_hash, received_hash)
```

## Интеграция с Vuex

Во фронтенде данные пользователя Telegram хранятся в хранилище Vuex:

```javascript
state: {
  user: null,
  isAuthenticated: false,
  isTelegramUser: false
}

mutations: {
  SET_USER(state, user) {
    state.user = user
    state.isAuthenticated = true
    state.isTelegramUser = user.isTelegramUser || false
  }
}
```

## Отображение информации о пользователе

Компонент `UserProfile.vue` отображает информацию о пользователе Telegram:

```vue
<div class="user-avatar" v-if="user && user.photo_url">
  <img :src="user.photo_url" :alt="user.username || user.first_name" />
</div>
<div class="user-info">
  <h2>{{ getUserName }}</h2>
  <p v-if="user && user.username" class="username">@{{ user.username }}</p>
  <p class="user-type">
    <span v-if="isTelegramUser" class="type-badge telegram">Telegram пользователь</span>
  </p>
</div>
```

## Безопасность

### Защита данных

1. Все данные от Telegram проверяются перед использованием
2. JWT токены используются для аутентификации пользователей
3. Секретный ключ хранится в конфигурации приложения

### Рекомендации по безопасности

1. Храните `TELEGRAM_BOT_TOKEN` в переменных окружения
2. Используйте HTTPS для всех эндпоинтов авторизации
3. Регулярно обновляйте зависимости приложения

## Устранение неполадок

### Распространенные проблемы

1. **Ошибка "Invalid Telegram data"**:
   - Проверьте правильность `TELEGRAM_BOT_TOKEN`
   - Убедитесь, что домен настроен правильно в [@BotFather](https://t.me/BotFather)

2. **Виджет не отображается**:
   - Проверьте подключение к интернету
   - Убедитесь, что скрипт виджета загружается корректно

3. **Ошибка CORS**:
   - Проверьте настройки CORS в конфигурации бэкенда
   - Убедитесь, что домен указан правильно

### Логирование

Для диагностики проблем включите логирование:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Тестирование

### Ручное тестирование

1. Откройте страницу входа в приложении
2. Нажмите на кнопку авторизации через Telegram
3. Выполните вход в Telegram (если требуется)
4. Подтвердите авторизацию
5. Проверьте, что вы успешно вошли в приложение

### Автоматическое тестирование

```python
def test_telegram_auth():
    # Тест проверки данных Telegram
    data = {
        'id': '123456789',
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'auth_date': '1234567890'
    }
    
    assert verify_telegram_data(data) == True
```

## Дополнительные возможности

### Персонализация

Используйте данные пользователя Telegram для персонализации:

- Отображение аватара пользователя
- Персональное приветствие
- Использование имени пользователя в уведомлениях

### Уведомления

Интеграция с Telegram Bot API для отправки уведомлений:

```python
import requests

def send_telegram_notification(user_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': user_id,
        'text': message
    }
    requests.post(url, data=data)
```

## Поддержка

Если у вас возникли проблемы с настройкой авторизации через Telegram, обратитесь к:

- Документации Telegram: https://core.telegram.org/widgets/login
- Поддержке Telegram: https://telegram.org/faq
- Разработчикам SARAYLO AI Workout