<template>
  <div class="p-4">
    <div class="flex justify-end mb-2">
      <el-button type="primary" size="small">
        <NuxtLink :to="`/`">Registrar</NuxtLink>
      </el-button>
    </div>

    <el-table :data="libros" style="width: 100%">
      <el-table-column prop="titulo" label="Título" />
      <el-table-column prop="autor" label="Autor" />
      <el-table-column prop="contenido" label="Contenido" />
      <el-table-column prop="traducido" label="Braille" />
      <el-table-column label="Acciones">
        <template #default="{ row }">
          <el-button type="primary" size="small">
            <NuxtLink :to="`/libro/${row.id}`">Editar</NuxtLink>
          </el-button>
          <el-button
            type="danger"
            size="small"
            @click="eliminar(row.id)"
          >
            Eliminar
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
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

// Eliminar libro
const eliminar = async (id) => {
  if (!confirm('¿Seguro que quieres eliminar este libro?')) return
  try {
    await $fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    ElMessage.success('Libro eliminado')
    cargarLibros()
  } catch (err) {
    console.error(err)
    ElMessage.error('Error al eliminar libro')
  }
}

onMounted(() => cargarLibros())
</script>
