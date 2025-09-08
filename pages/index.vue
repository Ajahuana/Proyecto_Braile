<template>
  <div class="welcome-message">
    <div class="icon-container">
      <el-icon class="celebration-icon"><Platform /></el-icon>
    </div>
    
    <h2 class="welcome-text">¡Bienvenido al Sistema Braille!</h2>
    
    <div class="description">
      <p>La aplicación se ha iniciado correctamente.</p>
      <p>Navega por las diferentes secciones usando el menú lateral.</p>
    </div>
  </div>
</template>

<script setup>
import { Platform } from '@element-plus/icons-vue';

</script>

<style scoped>
.welcome-message {
  background: rgb(246, 245, 245);
  border-radius: 40px;
  padding: 4rem;
  text-align: center;
  box-shadow: 0 10px 20px rgba(94, 93, 93, 0.1);
  max-width: 800px;
  margin: 10rem auto;
}

.icon-container {
  margin-bottom: 1rem;
}

.celebration-icon {
  font-size: 4rem;
  color: #4e94c0; /* Color azul consistente con tu app */
}

.welcome-text {
  font-size: 2.2rem;
  color: #333;
  margin-bottom: 1.5rem;
  font-weight: bold;
}

.description {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
}

.description p {
  margin-bottom: 0.5rem;
}
</style>