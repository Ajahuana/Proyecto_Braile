<template>
  <div class="transcripcion-fullwidth">
    <div class="header-section">
    <h2 class="page-title">
      <el-icon class="title-icon"><Edit /></el-icon>
      Edita tus libros aquí
    </h2>
    <p class="page-subtitle">Crea un texto nuevo o edita tus libros favoritos</p>
    </div>
    <div class="grid grid-cols-2 gap-2 p-2">
      <div class="label-text">Titulo</div>
      <div class="label-text">Autor</div>

      <el-input v-model="titulo" placeholder="Ingresa el título del libro..." />
      <el-input v-model="autor" placeholder="Ingresa el nombre del autor..." />

      <div class="label-text">Libro</div>
      <div class="label-text">Libro traducido</div>

      <el-input
        v-model="libro"
        type="textarea"
        :rows="20"
        class="w-full"
        placeholder="Escribe o pega aquí el contenido del libro que deseas transcribir..."
      />

      <el-input
        :value="traducido"
        type="textarea"
        :rows="20"
        class="w-full"
        readonly
        placeholder="La traducción a Braille aparecerá aquí automáticamente..."
      />

      <div class="col-span-2 flex justify-end mt-1">
        <el-button type="primary" @click="guardarLibro">Guardar</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Edit } from '@element-plus/icons-vue'
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
  padding: 3%;
  margin: 0;
  left: 280px;
  width: calc(100vw - 280px);
  background-color: #eff0f1;
}

.transcripcion-fullwidth .grid {
  min-height: calc(65vh - 10px); 
  padding: 1%;
  width: 100%;
  max-width: 2000px;
}

.transcripcion-fullwidth .grid {
  column-gap: 40px; /* Espacio horizontal entre columnas */
  row-gap: 8px;    /* Espacio vertical entre filas */
  background: #eff0f1;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(50, 49, 49, 0.1);
  margin: 0 auto;
}

.label-text {
  background: linear-gradient(135deg, #4e94c0 0%, #427798 100%);
  border-radius: 10px;
  font-weight: 750;
  color: #ffffff;
  font-size: 20px;
  margin-bottom: 0.2rem;
  display:flex ;
  align-items:center ;
  justify-content: start;
  padding-left: 20px;
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

.transcripcion-fullwidth :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.transcripcion-fullwidth :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.transcripcion-fullwidth :deep(.el-input__wrapper:focus-within) {
  box-shadow: 0 0 0 2px rgba(39, 174, 96, 0.2);
}

.transcripcion-fullwidth :deep(.el-textarea__inner) {
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
  transition: all 0.3s ease;
}

.transcripcion-fullwidth :deep(.el-textarea__inner:focus) {
  box-shadow: 0 0 0 2px rgba(55, 65, 59, 0.2);
}

/* Placeholder más visible */
.transcripcion-fullwidth :deep(.el-input__inner::placeholder),
.transcripcion-fullwidth :deep(.el-textarea__inner::placeholder) {
  padding-top: 15px;
  color: #93979c;
  font-style: italic;
}


.header-section {
  text-align: center;
  padding: 1.5rem 0;
  margin-bottom: 0.1rem;
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

.page-subtitle {
  font-size: 1.1rem;
  color: #7f8c8d;
  margin: 0.5rem 0 0 0;
  font-style: italic;
}

</style>