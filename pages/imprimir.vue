<template>
  <div class="p-4">
    <el-transfer
      v-model="seleccionados"
      :data="opciones"
      filterable
      filter-placeholder="Buscar libro"
     
      :props="{ key: 'id', label: 'titulo' }"
      height="300"
    />
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'

const API_URL = 'http://127.0.0.1:8000/libros'
const libros = ref([])          // libros completos
const seleccionados = ref([])   // ids seleccionados

// Generamos la lista para ElTransfer
const opciones = ref([])

const cargarLibros = async () => {
  try {
    libros.value = await $fetch(API_URL)
    // Solo necesitamos id y titulo para ElTransfer
    opciones.value = libros.value.map(l => ({ id: l.id, titulo: l.titulo }))
    console.log('Libros cargados:', libros.value)
  } catch (err) {
    console.error(err)
    ElMessage.error('Error al cargar libros')
  }
}

onMounted(() => {
  cargarLibros()
})
</script>
