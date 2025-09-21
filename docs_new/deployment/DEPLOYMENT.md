# Развертывание системы

## Технологический стек

- **Python 3.8+**
- **Flask** для RESTful API
- **PyTorch** для реализации нейронной сети
- **Redis** для кэширования сессий
- **RabbitMQ** для потоковой обработки
- **Docker** для контейнеризации
- **Kubernetes** для оркестрации (конфигурация развертывания включена)
- **Prometheus + Grafana** для мониторинга
- **ELK Stack** для логирования

## Установка

### Предварительные требования

- Python 3.8+
- Docker и Docker Compose
- Сервер Redis
- RabbitMQ

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd ios_ai_running
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # В Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите сервер Redis (если не используете Docker):
```bash
redis-server
```

5. Запустите приложение:
```bash
python api/workout_api.py
```

### Развертывание Docker

1. Соберите и запустите сервисы:
```bash
cd docker
docker-compose up -d
```

2. Доступ к API по адресу `http://localhost:5000`

3. Доступ к интерфейсу управления RabbitMQ: `http://localhost:15672`
   - Логин: appuser
   - Пароль: apppass

4. Доступ к Grafana: `http://localhost:3000`
   - Логин: admin
   - Пароль: admin

5. Доступ к Kibana: `http://localhost:5601`

## Менеджер графического интерфейса

Проект включает графический пользовательский интерфейс для управления сервером:

### Предварительные требования для GUI

- Node.js 18+
- Python 3.10+ (такие же требования, как и для сервера)
- Все зависимости из requirements.txt установлены

### Установка GUI

1. Перейдите в каталог gui:
```bash
cd gui
```

2. Установите зависимости:
```bash
npm install
```

### Запуск GUI

Для запуска графического интерфейса используйте один из следующих скриптов:

**В Windows:**
```bash
# Запуск всех сервисов с RabbitMQ
docker\start-with-rabbitmq.bat

# Остановка всех сервисов
docker\stop-all.bat

# Просмотр журналов
docker\view-logs.bat
```

**В Linux/Mac:**
```bash
# Запуск всех сервисов с RabbitMQ
chmod +x docker/start-with-rabbitmq.sh
./docker/start-with-rabbitmq.sh

# Остановка всех сервисов
chmod +x docker/stop-all.sh
./docker/stop-all.sh

# Просмотр журналов
chmod +x docker/view-logs.sh
./docker/view-logs.sh
```