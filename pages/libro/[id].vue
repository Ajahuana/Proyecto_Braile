<template>
  <div class="grid grid-cols-2 gap-2 p-2">
    <div>Título</div>
    <div>Autor</div>

    <el-input v-model="titulo" />
    <el-input v-model="autor" />

    <div>Libro</div>
    <div>Libro traducido</div>

    <el-input
      v-model="contenido"
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
      <el-button type="primary" @click="actualizarLibro">Actualizar</el-button>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBraille } from '~/composables/useBraille'

const route = useRoute()
const router = useRouter()
const libroId = route.params.id
const API_URL = 'http://127.0.0.1:8000/libros'

// refs locales
const titulo = ref('')
const autor = ref('')
const contenido = ref('')
const { traducido } = useBraille(contenido)

// cargar un libro desde FastAPI
const cargarLibro = async () => {
  try {
    const libroData = await $fetch(`${API_URL}/${libroId}`)
    titulo.value = libroData.titulo
    autor.value = libroData.autor
    contenido.value = libroData.contenido
    console.log('Libro cargado:', libroData);
  } catch (err) {
    console.error(err)
    ElMessage.error('Error al cargar el libro')
  }
}

// actualizar libro en FastAPI
const actualizarLibro = async () => {
  try {
    // Normalizar traducción: reemplazar líneas vacías por ⠿
    let traduccionNormalizada = traducido.value
      .split("\n")
      .map(linea => linea.trim() === "" ? "⠿".repeat(29) : linea)
      .join("\n")
      .replace(/\r/g, "")

    const body = {
      titulo: titulo.value,
      autor: autor.value,
      contenido: contenido.value,
      traducido: traduccionNormalizada,
      estado: 1
    }

    await $fetch(`${API_URL}/${libroId}`, {
      method: 'PUT',
      body
    })

    ElMessage.success('Libro actualizado correctamente')
    router.push('/libreria')
  } catch (err) {
    console.error(err)
    ElMessage.error('Error al actualizar el libro')
  }
}

onMounted(() => cargarLibro())
</script>
