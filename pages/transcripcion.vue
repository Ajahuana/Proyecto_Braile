<template>
  <div class="grid grid-cols-2 gap-2 p-2">
    <div>Titulo</div>
    <div>Autor</div>

    <el-input v-model="titulo" />
    <el-input v-model="autor" />

    <div>Libro</div>
    <div>Libro traducido</div>

    <el-input
      v-model="libro"
      type="textarea"
      :rows="20"
      class="w-full"
    />

    <el-input
      :value="traducido"
      type="textarea"
      :rows="20"
      class="w-full"
      readonly
    />

    <div class="col-span-2 flex justify-end mt-2">
      <el-button type="primary" @click="guardarLibro">Guardar</el-button>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { ref } from 'vue'
import { useBraille } from '~/composables/useBraille'

const titulo = ref('')
const autor = ref('')
const { libro, traducido } = useBraille('')

const API_URL = 'http://127.0.0.1:8000/libros'  // tu backend FastAPI

const guardarLibro = async () => {
  try {
    const body = {
      titulo: titulo.value,
      autor: autor.value,
      contenido: libro.value,
      traducido: traducido.value,
      estado: 1
    }

    const response = await $fetch(API_URL, {
      method: 'POST',
      body
    })

    if (response.id) { // en FastAPI devolvemos el libro con id
      ElMessage.success('Libro guardado correctamente')
      titulo.value = ''
      autor.value = ''
      libro.value = ''
    }
  } catch (err) {
    console.error(err)
    ElMessage.error('Error al guardar el libro')
  }
}
</script>
