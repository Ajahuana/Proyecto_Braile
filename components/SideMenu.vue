<template>
  <div class="common-layout">
    <el-header class="braille-header" height="80px">
      <div class="header-content">
        <h2 class="header-title" >
          Interfaz de transcripción, traducción e interpretación de textos Braille
        </h2>
      </div>
    </el-header>

    <el-container class="body-container">
      <el-aside class="sidebar-aside" width="250px">
        <div class="sidebar-container">
          <el-menu 
            default-active="2" 
            class="custom-sidebar-menu"
            :collapse="false"
            background-color="#008080"
            text-color="#ecf0f1"
            active-text-color="#3498db"
          >
            <el-menu-item index="1" class="menu-item">
              <el-icon><House /></el-icon>
              <NuxtLink :to="`/`" class="menu-link">
                <span>Inicio</span>
              </NuxtLink>
            </el-menu-item>
            
            <el-menu-item index="2" class="menu-item">
              <el-icon><Edit /></el-icon>
              <NuxtLink :to="`/transcripcion`" class="menu-link">
                <span>Transcripción</span>
              </NuxtLink>
            </el-menu-item>
            
            <el-menu-item index="3" class="menu-item">
              <el-icon><Printer /></el-icon>
              <NuxtLink :to="`/imprimir`" class="menu-link">
                <span>Impresión</span>
              </NuxtLink>
            </el-menu-item>
            
            <el-menu-item index="4" class="menu-item">
              <el-icon><Collection /></el-icon>
              <NuxtLink :to="`/libreria`" class="menu-link">
                <span>Biblioteca de libros</span>
              </NuxtLink>
            </el-menu-item>
            
            <el-menu-item index="5" class="menu-item">
              <el-icon><Upload /></el-icon>
              <NuxtLink :to="`/importar`" class="menu-link">
                <span>Importar texto Word</span>
              </NuxtLink>
            </el-menu-item>
          </el-menu>
        </div>
      </el-aside>

      <el-main class="main-content">
        <slot />
      </el-main>
    </el-container>

    <el-footer class="braille-footer" height="60px">
      <div class="footer-content">
        <p class="footer-text">
          Centro de Rehabilitación Manuela Gandarillas - Contacto: 71717171 - © 2025
        </p>
      </div>
    </el-footer>
  </div>
</template>

<script lang="ts" setup>
import { House, Edit, Printer, Collection, Upload } from '@element-plus/icons-vue'

const index = ref('1');
</script>

<style scoped>
.common-layout {
  height: 100vh;
  width: 100vw;
}

.braille-header {
  background: linear-gradient(135deg, #87CEEB 0%, #4A90E2 50%, #6BB6FF 100%);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 0;
  z-index: 1001;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.header-content {
  width: 100%;
  text-align: center;
  padding: 0 20px;
}

.header-title {
  color: rgb(41, 38, 38);
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  letter-spacing: 0.5px;
}

.body-container {
  flex: 1;
  height: calc(100vh - 140px); 
  margin-top: 70px; 
  margin-bottom: 60px; 
}

.sidebar-aside {
  padding: 0;
  overflow: hidden;
}

.sidebar-container {
  height: calc(100vh - 140px); /* Altura total menos header y footer */
  width: 250px;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
}

.custom-sidebar-menu {
  height: 100%;
  border-right: none;
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
}

.menu-item {
  margin: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  padding: 0 16px;
  height: 50px;
  line-height: 50px;
}

.menu-item:hover {
  background-color: rgba(52, 152, 219, 0.1);
  transform: translateX(5px);
}

.menu-item.is-active {
  background-color: rgba(52, 152, 219, 0.2);
  border-left: 4px solid #3498db;
}

.menu-link {
  color: inherit;
  text-decoration: none;
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  padding-left: 8px;
}

.menu-link:hover {
  color: #3498db;
}

/* Main Content Styles */
.main-content {
  background-color: #f8f9fa;
  padding: 20px;
  overflow-y: auto;
}

.braille-footer {
  background-color: #2c3e50;
  color: #ecf0f1;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 0;
  width: 100%;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1001;
}

.footer-content {
  width: 100%;
  text-align: center;
  padding: 0 20px;
}

.footer-text {
  margin: 0;
  font-size: 14px;
  color: #bdc3c7;
}

:deep(.el-icon) {
  margin-right: 12px;
  font-size: 18px;
  color: #bdc3c7;
}

:deep(.is-active .el-icon) {
  color: #3498db;
}

:deep(.el-menu-item.is-active) {
  background-color: rgba(52, 152, 219, 0.15) !important;
  color: #3498db !important;
  border-left: 4px solid #3498db;
  margin-left: 8px;
  border-radius: 0 8px 8px 0;
}

/* Hover effects - Manteniendo tu código */
:deep(.el-menu-item:hover) {
  background-color: rgba(52, 152, 219, 0.1) !important;
  color: #3498db !important;
}

/* Remover estilos por defecto de Element Plus */
:deep(.el-menu-item) {
  border-bottom: none !important;
}

/* Remove default Element Plus padding */
:deep(.el-header) {
  padding: 0;
}

:deep(.el-footer) {
  padding: 0;
}

:deep(.el-aside) {
  padding: 0;
}

:deep(.el-main) {
  padding: 0;
}

/* Responsive - Manteniendo tu código original */
@media (max-width: 768px) {
  .sidebar-container {
    width: 200px;
  }
  
  .sidebar-aside {
    width: 200px !important;
  }
  
  .menu-item {
    margin: 6px 8px;
    padding: 0 12px;
    height: 45px;
    line-height: 45px;
  }
  
  .header-title {
    font-size: 18px;
  }
  
  .footer-text {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .header-title {
    font-size: 16px;
    line-height: 1.3;
  }
  
  .braille-header {
    height: 70px !important;
  }
  
  .braille-footer {
    height: 50px !important;
  }
  
  .body-container {
    height: calc(100vh - 120px);
  }
  
  .sidebar-aside {
    width: 180px !important;
  }
  
  .sidebar-container {
    width: 180px;
  }
}

/* Scrollbar customization for main content */
.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.main-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>