<template>
  <div class="libreria-container">
    <div class="content-wrapper">
       <div class="header-simple">
        <h2 class="page-title">
          <el-icon class="title-icon"><Reading /></el-icon>
          Biblioteca de libros
        </h2>
      </div>

      <div class="p-4">
        <el-table :data="libros" style="width: 100%" class="custom-table">
          <el-table-column prop="titulo" label="Título" />
          <el-table-column prop="autor" label="Autor" />
          <el-table-column prop="contenido" label="Contenido">
            <template #default="scope">
              <div class="line-clamp-3">
                {{ scope.row.contenido }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Traducido">
            <template #default="scope">
              <el-checkbox :checked="!!scope.row.traducido" disabled />
            </template>
          </el-table-column>

          <el-table-column label="Acciones">
            <template #default="{ row }">
              <div class="flex gap-3">
                <el-button type="primary" size="small">
                  <NuxtLink :to="`/libro/${row.id}`">Editar</NuxtLink>
                </el-button>
                <el-button type="danger" size="small" @click="eliminar(row.id)">
                  Eliminar
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Reading } from '@element-plus/icons-vue'; //import icono
import { ElMessage, ElMessageBox } from 'element-plus';
import { onMounted, ref } from 'vue';

const libros = ref([])
const API_URL = 'http://127.0.0.1:8000/libros'

// Cargar libros desde FastAPI
const cargarLibros = async () => {
  try {
    libros.value = await $fetch(API_URL)
  } catch (err) {
    console.error(err)
    ElMessage.error('Error al cargar libros')
  }
}

// Eliminar libro con confirmación
const eliminar = async (id) => {
  try {
    await ElMessageBox.confirm(
      '¿Seguro que quieres eliminar este libro?',
      'Confirmación',
      {
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        type: 'warning',
      }
    )

    // Si el usuario confirma
    await $fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    ElMessage.success('Libro eliminado')
    cargarLibros()
  } catch (err) {
    // Si se cancela, no hacemos nada
    if (err === 'cancel') {
      ElMessage.info('Eliminación cancelada')
    } else {
      console.error(err)
      ElMessage.error('Error al eliminar libro')
    }
  }
}

onMounted(() => cargarLibros())
</script>


<style scoped>
/* Centrado igual que otras páginas */
.libreria-container {
  position: absolute;
  left: 260px;
  width: calc(100vw - 260px);
  background-color: #eff0f1;
  min-height: calc(100vh - 180px);
}

.content-wrapper {
  max-width: 2000px;
  margin: 4% auto;
  padding: 2rem;
}

/* Título simple */
.header-simple {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #103656;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.title-icon {
  font-size: 2.5rem;
  color: #0b598a;
  box-shadow: 0 15px 10px rgba(3, 3, 3, 0.1);
}

/* Mejoras moderadas de tabla */
.custom-table {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Headers de tabla con gradiente sutil */
.libreria-container :deep(.el-table th) {
  background: linear-gradient(135deg, #4e94c0 0%, #427798 100%);
  color: white;
  font-size: 18px;
  font-weight: 600;
  padding: 22px 34px;
  border: none;
}

.libreria-container :deep(.el-table th .cell) {
  color: white;
}

/* Celdas con mejor espaciado */
.libreria-container :deep(.el-table td) {
  font-size: 15px;
  padding: 16px 12px;
  border-bottom: 1px solid #f0f0f0;
}

/* Efecto hover sutil */
.libreria-container :deep(.el-table__row:hover) {
  background-color: #f8f9fa;
}

/* Botones con colores consistentes */
.libreria-container :deep(.el-button--primary) {
  background-color: #27ae60;
  border-color: #27ae60;
  font-size: 15px;
  padding: 8px 16px;
}

.libreria-container :deep(.el-button--primary:hover) {
  background-color: #2ecc71;
  border-color: #2ecc71;
}

.libreria-container :deep(.el-button--danger) {
  font-size: 15px;
  padding: 8px 16px;
}

/* Links sin decoración */
.libreria-container :deep(a) {
  color: inherit;
  text-decoration: none;
}

/* Truncar contenido largo */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 60px;
  line-height: 1.4;
}

/* Responsive básico */
@media (max-width: 768px) {
  .libreria-container {
    left: 200px;
    width: calc(100vw - 200px);
  }
  
  .content-wrapper {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .libreria-container {
    left: 180px;
    width: calc(100vw - 180px);
  }
}
</style>