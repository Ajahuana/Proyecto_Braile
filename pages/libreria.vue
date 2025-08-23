<template>
  <div class="p-4">
    

    <el-table :data="libros" style="width: 100%">
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
</template>

<script setup>
import { ElMessage, ElMessageBox } from 'element-plus'
import { onMounted, ref } from 'vue'

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
