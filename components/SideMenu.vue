<template>
  <div class="common-layout">
    <el-header class="braille-header">
      <div class="header-content">
        <h2 class="header-title">
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
            background-color="#008080"
            text-color="#ecf0f1"
            active-text-color="#3498db"
          >
            <el-menu-item index="1" class="menu-item">
              <el-icon><House /></el-icon>
              <NuxtLink to="/" class="menu-link">
                <span>Inicio</span>
              </NuxtLink>
            </el-menu-item>
            
            <el-menu-item index="2" class="menu-item">
              <el-icon><Edit /></el-icon>
              <NuxtLink to="/transcripcion" class="menu-link">
                <span>Transcripción</span>
              </NuxtLink>
            </el-menu-item>
            
            <el-menu-item index="3" class="menu-item">
              <el-icon><Printer /></el-icon>
              <NuxtLink to="/imprimir" class="menu-link">
                <span>Impresión</span>
              </NuxtLink>
            </el-menu-item>
            
            <el-menu-item index="4" class="menu-item">
              <el-icon><Collection /></el-icon>
              <NuxtLink to="/libreria" class="menu-link">
                <span>Biblioteca de libros</span>
              </NuxtLink>
            </el-menu-item>
            
            <el-menu-item index="5" class="menu-item">
              <el-icon><Upload /></el-icon>
              <NuxtLink to="/importar" class="menu-link">
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

    <el-footer class="braille-footer">
      <div class="footer-content">
        <p class="footer-text">
          Sistema Braille - Transcriptor v2.0.0 © 2025 - Centro de Rehabilitacion Manuela Gandarillas
        </p>
      </div>
    </el-footer>
  </div>
</template>

<script lang="ts" setup>
import { Collection, Edit, House, Printer, Upload } from '@element-plus/icons-vue';
</script>

<style scoped>
.common-layout {
  height: 100vh;
  width: 100vw;
}

.braille-header {
  background: linear-gradient(135deg, #78b9d3 0%, #4e94c0 40%, #87CEEB 100%);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  height: 85px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1001;
}

.header-content {
  width: 100%;
  text-align: center;
  padding: 0 20px;
}

.header-title {
  color: rgb(41, 38, 38);
  font-size: 28px;
  font-weight: 600;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  letter-spacing: 0.5px;
}

.body-container {
  flex: 1;
  height: calc(100vh - 140px);
  margin-top: 80px;
}

.sidebar-aside {
  overflow: hidden;
}

.sidebar-container {
  height: 100%;
  width: 250px;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
}

.custom-sidebar-menu {
  height: 100%;
  border-right: none;
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
}

.menu-item {
  margin: 12px 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
  padding: 0 16px;
  height: 60px;
  line-height: 50px;
}

.menu-item:hover {
  background-color: rgba(52, 152, 219, 0.1);
  transform: translateX(5px);
}

.menu-link {
  color: inherit;
  text-decoration: none;
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  padding-left: 4px;
  font-size: 17px;
}

.menu-link:hover {
  color: #3498db;
}

.main-content {
  background-color: #eff0f1;
  padding: 0px;
  overflow-y: auto;
  width: 100%;
}

.braille-footer {
  background-color: #c8f8f9;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  height: 80px;
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
  font-size: 15px;
  color: #060606;
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

:deep(.el-menu-item:hover) {
  background-color: rgba(52, 152, 219, 0.1) !important;
  color: #3498db !important;
}

:deep(.el-menu-item) {
  border-bottom: none !important;
}

/* Responsive */
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
    margin-top: 70px;
  }
  
  .sidebar-aside {
    width: 180px !important;
  }
  
  .sidebar-container {
    width: 180px;
  }
}

/* Scrollbar customization */
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