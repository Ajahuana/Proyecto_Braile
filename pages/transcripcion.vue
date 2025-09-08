<template>
  <div class="transcripcion-fullwidth">
    <div class="grid grid-cols-2 gap-2 p-2">
      <div class="label-text">Titulo</div>
      <div class="label-text">Autor</div>

      <el-input v-model="titulo" />
      <el-input v-model="autor" />

      <div class="label-text">Libro</div>
      <div class="label-text">Libro traducido</div>

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

      <div class="col-span-2 flex justify-end mt-1">
        <el-button type="primary" @click="guardarLibro">Guardar</el-button>
      </div>
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
    // Normalizar traducción: quitar saltos de línea vacíos
    let traduccionNormalizada = traducido.value
      .split("\n")              // separar por líneas
      .map(linea => {
        // Si la línea está vacía o solo espacios, rellenar con ⠿
        return linea.trim() === "" ? "⠿".repeat(29) : linea
      })
      .join("\n")               // volver a unir
      .replace(/\r/g, "")       // quitar \r si existe

    const body = {
      titulo: titulo.value,
      autor: autor.value,
      contenido: libro.value,
      traducido: traduccionNormalizada,
      estado: 1
    }

    const response = await $fetch(API_URL, {
      method: "POST",
      body
    })

    if (response.id) {
      ElMessage.success("Libro guardado correctamente")
      titulo.value = ""
      autor.value = ""
      libro.value = ""
    }
  } catch (err) {
    console.error(err)
    ElMessage.error("Error al guardar el libro")
  }
}

</script>

<style scoped>
.transcripcion-fullwidth {
  /* Ocupa todo el espacio disponible sin márgenes */
  position: absolute;
  padding: 0;
  margin: 0;
  left: 280px;
  width: calc(100vw - 280px);
  background-color: #eff0f1;
}

.transcripcion-fullwidth .grid {
  min-height: calc(80vh - 10px); 
  padding: 2%;
  width: 100%;
  max-width: 2000px;
}

.transcripcion-fullwidth .grid {
  column-gap: 40px; /* Espacio horizontal entre columnas */
  row-gap: 5px;    /* Espacio vertical entre filas */
}

.label-text {
  font-weight: 750;
  color: #2c3e50;
  font-size: 20px;
  margin-bottom: 0.2rem;
  display:flex ;
  align-items:end ;
}

/* Personalizar el botón */
.transcripcion-fullwidth :deep(.el-button--primary) {
  background-color: #27ae60; /* Verde */
  border-color: #27ae60;
  font-size: 20px; /* Aumentar tamaño de letra */
  font-weight: 500; /* Hacer la letra más gruesa */
  padding: 20px 34px; /* Hacer el botón más grande */
}

.transcripcion-fullwidth :deep(.el-button--primary:hover) {
  background-color: #38df7e; /* Verde más claro al hacer hover */
  border-color: #2ecc71;
}
</style>