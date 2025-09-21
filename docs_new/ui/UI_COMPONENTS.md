# Компоненты пользовательского интерфейса

## Компоненты пользовательского интерфейса для аудио-взаимодействия

### Настройки аудио-обратной связи

#### Экран настроек
- **Управление частотой**:
  - Редко (один раз за тренировку)
  - Средне (каждые 10-15 минут)
  - Часто (каждые 5 минут или при значительном улучшении)

- **Управление громкостью**:
  - Ползунок для громкости аудио-обратной связи относительно музыки
  - Кнопка предварительного просмотра для проверки уровней громкости

- **Выбор голоса**:
  - Опция мужского голоса
  - Опция женского голоса
  - Воспроизведение образца голоса для каждой опции

- **Выбор языка**:
  - Список поддерживаемых языков
  - По умолчанию системный язык
  - Образцы голоса на каждом языке

#### Функции доступности
- Визуальные индикаторы для пользователей с нарушениями слуха
- Опции тактильной обратной связи
  - Резервный переход к преобразованию текста в речь

### Визуальная обратная связь во время аудио-взаимодействия

#### Индикатор распознавания речи
- Иконка микрофона с анимацией
- Визуализация звуковых волн во время прослушивания
- Текст статуса ("Слушаю", "Обрабатываю...", "Готово")

#### Отображение текста
- Отображение распознанной речи в реальном времени
- Выделение ключевых слов
- Редактируемое текстовое поле для корректировок

#### Анимация обработки
- Спinner или индикатор прогресса
- Сообщения статуса ("Анализирую ваши цели...", "Обновляю ваш план...")
- Приблизительное время обработки

### Интерфейс уточнения целей

#### Отображение аудио-подсказки
- Крупный, понятный текст аудио-подсказки
- Иконка динамика с анимацией
- Опция повторного воспроизведения подсказки

#### Сбор ответов
- Кнопка микрофона для голосового ответа
- Альтернатива ввода с клавиатуры
- Визуальная обратная связь во время записи

#### Визуализация обновления плана
- Сравнение плана до/после
- Выделенные изменения
- Приблизительное влияние на достижение цели

## Реализация мобильного пользовательского интерфейса

### Компоненты пользовательского интерфейса iOS

#### Представление настроек аудио
```swift
struct AudioSettingsView: View {
    @State private var frequency: Frequency = .medium
    @State private var volume: Double = 0.7
    @State private var voice: VoiceType = .female
    @State private var language: String = "en-US"
    
    var body: some View {
        Form {
            Section(header: Text("Частота обратной связи")) {
                Picker("Частота", selection: $frequency) {
                    ForEach(Frequency.allCases, id: \.self) { frequency in
                        Text(frequency.rawValue).tag(frequency)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
            }
            
            Section(header: Text("Громкость")) {
                HStack {
                    Image(systemName: "speaker")
                    Slider(value: $volume, in: 0...1, step: 0.1)
                    Text("\(Int(volume * 100))%")
                }
                Button("Предварительный просмотр громкости") {
                    // Воспроизвести тестовый звук
                }
            }
            
            Section(header: Text("Голос")) {
                Picker("Голос", selection: $voice) {
                    Text("Мужской").tag(VoiceType.male)
                    Text("Женский").tag(VoiceType.female)
                }
                .pickerStyle(SegmentedPickerStyle())
                Button("Прослушать образец") {
                    // Воспроизвести образец голоса
                }
            }
            
            Section(header: Text("Язык")) {
                Picker("Язык", selection: $language) {
                    ForEach(supportedLanguages, id: \.code) { language in
                        Text(language.name).tag(language.code)
                    }
                }
                Button("Прослушать образец") {
                    // Воспроизвести образец языка
                }
            }
        }
        .navigationTitle("Настройки аудио")
    }
}
```

#### Представление голосового взаимодействия
```swift
struct VoiceInteractionView: View {
    @State private var isListening = false
    @State private var recognizedText = ""
    @State private var showTextInput = false
    
    var body: some View {
        VStack(spacing: 20) {
            // Отображение аудио-подсказки
            VStack {
                Text("Вы прошли этот отрезок намного быстрее, чем на прошлой неделе!")
                    .font(.title2)
                    .multilineTextAlignment(.center)
                    .padding()
                
                Image(systemName: "speaker.wave.2")
                    .font(.largeTitle)
                    .foregroundColor(.blue)
            }
            
            // Индикатор распознавания речи
            if isListening {
                VStack {
                    Image(systemName: "mic.fill")
                        .font(.largeTitle)
                        .foregroundColor(.red)
                        .symbolEffect(.pulsing)
                    
                    Text("Слушаю...")
                        .font(.headline)
                }
            }
            
            // Отображение распознанного текста
            if !recognizedText.isEmpty {
                VStack(alignment: .leading) {
                    Text("Я услышал:")
                        .font(.headline)
                    Text(recognizedText)
                        .padding()
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(8)
                }
            }
            
            // Опции ответа
            VStack(spacing: 15) {
                Button(action: {
                    isListening.toggle()
                    // Начать/остановить распознавание речи
                }) {
                    HStack {
                        Image(systemName: isListening ? "stop.fill" : "mic.fill")
                        Text(isListening ? "Остановить запись" : "Записать ответ")
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(isListening ? Color.red : Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                
                Button("Ввести текст") {
                    showTextInput = true
                }
                .sheet(isPresented: $showTextInput) {
                    TextInputView(text: $recognizedText)
                }
                
                Button("Отправить") {
                    // Отправить ответ в бэкенд
                }
                .disabled(recognizedText.isEmpty)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.green)
                .foregroundColor(.white)
                .cornerRadius(10)
                .disabled(recognizedText.isEmpty)
            }
        }
        .padding()
    }
}
```