<template>
  <div class="p-4">
    <el-transfer
      v-model="seleccionados"
      :data="opciones"
      filterable
      filter-placeholder="Buscar libro"
      :titles="['Libros', 'Para imprimir']"
      :props="{ key: 'id', label: 'titulo' }"
      height="300"
    />

    <div class="mt-4 flex justify-end">
      <el-button type="primary" @click="imprimir">
        Imprimir
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'

const API_URL = 'http://127.0.0.1:8000/libros'
const libros = ref([])          // todos los libros con datos completos
const seleccionados = ref([])   // ids que están en la lista derecha
const opciones = ref([])        // opciones para transfer

// Cargar libros desde FastAPI
const cargarLibros = async () => {
  try {
    libros.value = await $fetch(API_URL)
    opciones.value = libros.value.map(l => ({ id: l.id, titulo: l.titulo }))
  } catch (err) {
    console.error(err)
    ElMessage.error('Error al cargar libros')
  }
}

// Función imprimir
const imprimir = () => {
  if (seleccionados.value.length === 0) {
    ElMessage.warning('No hay libros en la lista de "Para imprimir"')
    return
  }

  // Obtener TODOS los que están en la lista derecha
  const paraImprimir = libros.value.filter(l =>
    seleccionados.value.includes(l.id)
  )

  // Construir JSON
  const resultado = paraImprimir.map(l => ({
    id: l.id,
    titulo: l.titulo,
    traducido: l.traducido
  }))

  console.log('📄 Libros para imprimir:', resultado)
  ElMessage.success(`Se enviaron ${resultado.length} libros a impresión`)
}

onMounted(() => {
  cargarLibros()
})
</script>
