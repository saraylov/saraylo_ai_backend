import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class TemporalFusionTransformer(nn.Module):
    """Модуль временной обработки (Temporal Fusion Transformer)"""
    def __init__(self, input_size=11, hidden_size=64, num_heads=4, num_layers=2, dropout=0.2):
        super(TemporalFusionTransformer, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.dropout = dropout
        
        # LSTM слои для обработки временных последовательностей
        self.lstm1 = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.lstm2 = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        
        # Слои нормализации и регуляризации
        self.layer_norm = nn.LayerNorm(hidden_size)
        self.dropout_layer = nn.Dropout(dropout)
        
        # Механизм многоголовочного внимания
        self.multihead_attention = nn.MultiheadAttention(
            embed_dim=hidden_size, 
            num_heads=num_heads, 
            dropout=dropout,
            batch_first=True
        )
        
        # Полносвязная сеть прямого распространения
        self.feed_forward = nn.Sequential(
            nn.Linear(hidden_size, hidden_size * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size * 2, hidden_size),
            nn.Dropout(dropout)
        )
        
    def forward(self, x):
        # x shape: (batch_size, sequence_length, input_size)
        batch_size, seq_len, _ = x.size()
        
        # Обработка через LSTM слои
        lstm_out, _ = self.lstm1(x)
        lstm_out, _ = self.lstm2(lstm_out)
        
        # Применение нормализации и dropout
        lstm_out = self.layer_norm(lstm_out)
        lstm_out = self.dropout_layer(lstm_out)
        
        # Применение многоголовочного внимания
        attn_out, _ = self.multihead_attention(lstm_out, lstm_out, lstm_out)
        attn_out = self.dropout_layer(attn_out)
        
        # Применение feed forward сети
        ff_out = self.feed_forward(attn_out)
        ff_out = self.dropout_layer(ff_out)
        
        # Возвращаем последний временной шаг
        return ff_out[:, -1, :]  # shape: (batch_size, hidden_size)


class StaticFeatureProcessor(nn.Module):
    """Модуль обработки статических признаков (Static Feature Processor)"""
    def __init__(self, input_size=15, hidden_sizes=[64, 128, 64], dropout=0.3):
        super(StaticFeatureProcessor, self).__init__()
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.dropout = dropout
        
        # Создание MLP слоев
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.BatchNorm1d(hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_size = hidden_size
            
        self.mlp = nn.Sequential(*layers)
        
    def forward(self, x):
        # x shape: (batch_size, input_size)
        return self.mlp(x)  # shape: (batch_size, hidden_sizes[-1])


class AttentionFusionModule(nn.Module):
    """Модуль фузии с механизмом внимания (Attention Fusion Module)"""
    def __init__(self, temporal_size=64, static_size=64, output_size=64):
        super(AttentionFusionModule, self).__init__()
        self.temporal_size = temporal_size
        self.static_size = static_size
        self.output_size = output_size
        
        # Слой объединения признаков
        self.fusion_layer = nn.Linear(temporal_size + static_size, output_size)
        
        # Механизм внимания для взвешивания признаков
        self.attention = nn.MultiheadAttention(
            embed_dim=output_size,
            num_heads=4,
            dropout=0.1,
            batch_first=True
        )
        
        # Слой нормализации
        self.layer_norm = nn.LayerNorm(output_size)
        
    def forward(self, temporal_features, static_features):
        # temporal_features shape: (batch_size, temporal_size)
        # static_features shape: (batch_size, static_size)
        
        # Объединение признаков
        combined = torch.cat([temporal_features, static_features], dim=1)
        fused = self.fusion_layer(combined)
        fused = F.relu(fused)
        
        # Добавление размерности для применения внимания
        fused = fused.unsqueeze(1)  # shape: (batch_size, 1, output_size)
        
        # Применение механизма внимания
        attn_out, _ = self.attention(fused, fused, fused)
        attn_out = self.layer_norm(attn_out)
        
        # Удаление дополнительной размерности
        return attn_out.squeeze(1)  # shape: (batch_size, output_size)


class MultiHeadOutputModule(nn.Module):
    """Многоголовый выходной модуль (Multi-head Output Module)"""
    def __init__(self, input_size=64):
        super(MultiHeadOutputModule, self).__init__()
        self.input_size = input_size
        
        # Голова нагрузки (Load Head)
        self.load_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
        # Голова усталости (Fatigue Head)
        self.fatigue_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 4),
            nn.Softmax(dim=1)
        )
        
        # Голова восстановления (Recovery Head)
        self.recovery_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
        # Голова эффективности тренировки (Effectiveness Head)
        self.effectiveness_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
            nn.Softmax(dim=1)
        )
        
        # Голова времени до истощения (Exhaustion Head)
        self.exhaustion_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.ReLU()
        )
        
        # Голова аудио-триггеров (Audio Trigger Head)
        self.audio_trigger_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
        # Голова улучшения производительности (Improvement Head)
        self.improvement_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.ReLU()
        )
        
        # Голова рекомендаций (Recommendations Head)
        self.recommendations_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 16)
        )
        
        # Голова нутрицевтических признаков (Nutrition Features Head)
        self.nutrition_head = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 32)
        )
        
    def forward(self, x):
        outputs = {}
        outputs['current_load'] = self.load_head(x) * 100  # Преобразуем в проценты
        outputs['fatigue_level'] = self.fatigue_head(x)
        outputs['recovery_state'] = self.recovery_head(x) * 100  # Преобразуем в проценты
        outputs['training_effectiveness'] = self.effectiveness_head(x)
        outputs['time_to_exhaustion'] = self.exhaustion_head(x)
        outputs['audio_trigger_probability'] = self.audio_trigger_head(x)
        outputs['performance_improvement'] = self.improvement_head(x)
        outputs['recommendations_features'] = self.recommendations_head(x)
        outputs['nutrition_features'] = self.nutrition_head(x)
        
        return outputs


class PhysiologicalStateModel(nn.Module):
    """Основная модель физиологического состояния"""
    def __init__(self):
        super(PhysiologicalStateModel, self).__init__()
        
        # Инициализация всех компонентов
        self.temporal_processor = TemporalFusionTransformer()
        self.static_processor = StaticFeatureProcessor()
        self.fusion_module = AttentionFusionModule()
        self.output_module = MultiHeadOutputModule()
        
    def forward(self, temporal_data, static_data):
        # Обработка временных данных
        temporal_features = self.temporal_processor(temporal_data)
        
        # Обработка статических данных
        static_features = self.static_processor(static_data)
        
        # Фузия признаков
        fused_features = self.fusion_module(temporal_features, static_features)
        
        # Генерация выходов
        outputs = self.output_module(fused_features)
        
        return outputs