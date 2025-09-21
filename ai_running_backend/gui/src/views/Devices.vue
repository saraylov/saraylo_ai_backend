<template>
  <div class="devices-screen">
    <div class="devices-panel glass-panel">
      <h2>Подключенные устройства</h2>
      <div class="device-list">
        <div class="device-item">
          <img src="/images/smartwatch.png" alt="Смарт-часы" class="device-icon">
          <div class="device-info">
            <span class="device-name">Смарт-часы</span>
            <span class="device-status connected">Подключено</span>
          </div>
        </div>
        <div class="device-item">
          <img src="/images/heart-monitor.png" alt="Пульсометр" class="device-icon">
          <div class="device-info">
            <span class="device-name">Пульсометр</span>
            <span class="device-status disconnected">Не подключено</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Devices'
}
</script>

<style scoped>
.devices-screen {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.devices-panel {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
}

.devices-panel h2 {
  color: #00BFFF;
  margin-top: 0;
  text-align: center;
}

.device-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.device-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  transition: all 0.3s ease;
}

.device-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.device-icon {
  width: 48px;
  height: 48px;
  margin-right: 15px;
}

.device-info {
  display: flex;
  flex-direction: column;
}

.device-name {
  color: white;
  font-size: 16px;
  font-weight: bold;
}

.device-status {
  font-size: 14px;
  margin-top: 5px;
}

.device-status.connected {
  color: #32CD32;
}

.device-status.disconnected {
  color: #FF4500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .device-item {
    padding: 10px;
  }
  
  .device-icon {
    width: 36px;
    height: 36px;
  }
  
  .device-name {
    font-size: 14px;
  }
  
  .device-status {
    font-size: 12px;
  }
}
</style>