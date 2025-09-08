<template>
  <div class="importar-fullwidth">
    <div class="content-container">
      <div class="header-section">
        <h2 class="page-title">
          <el-icon class="title-icon"><Upload /></el-icon>
          Importar archivos de texto
        </h2>
        <p class="page-subtitle">Sube archivos .txt, .docx o .pdf para convertir a Braille</p>
      </div>

      <div class="upload-section">
        <el-upload
          ref="uploadRef"
          v-model:file-list="fileList"
          class="upload-demo"
          drag
          :action="uploadUrl"
          :before-upload="beforeUpload"
          :on-success="handleSuccess"
          :on-error="handleError"
          :on-remove="handleRemove"
          :accept="acceptedTypes"
          :limit="5"
          :on-exceed="handleExceed"
        >
          <div class="upload-area">
            <el-icon class="upload-icon"><DocumentAdd /></el-icon>
            <div class="upload-text">
              <h3>Arrastra tus archivos aquí</h3>
              <p>o <span class="upload-link">haz clic para seleccionar</span></p>
            </div>
            <div class="file-types">
              <span class="file-type">.TXT</span>
              <span class="file-type">.DOCX</span>
              <span class="file-type">.PDF</span>
            </div>
            <p class="upload-limit">Máximo 5 archivos, 10MB cada uno</p>
          </div>
        </el-upload>
      </div>

      <div class="files-section" v-if="processedFiles.length > 0">
        <h3 class="section-title">Archivos procesados</h3>
        <div class="files-grid">
          <div 
            v-for="file in processedFiles" 
            :key="file.id"
            class="file-card"
          >
            <div class="file-header">
              <el-icon class="file-icon"><Document /></el-icon>
              <div class="file-info">
                <h4 class="file-name">{{ file.name }}</h4>
                <p class="file-size">{{ formatFileSize(file.size) }}</p>
              </div>
              <el-button 
                type="danger" 
                size="small" 
                circle 
                @click="removeFile(file.id)"
              >
                <el-icon><Close /></el-icon>
              </el-button>
            </div>
            
            <div class="file-content">
              <h5>Contenido extraído:</h5>
              <div class="content-preview">
                {{ file.content.substring(0, 200) }}
                <span v-if="file.content.length > 200">...</span>
              </div>
            </div>

            <div class="file-actions">
              <el-button 
                type="primary" 
                @click="saveAsBook(file)"
                :loading="file.saving"
              >
                <el-icon><Edit /></el-icon>
                Guardar como libro
              </el-button>
              <el-button @click="showFullContent(file)">
                <el-icon><View /></el-icon>
                Ver completo
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para ver contenido completo -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="selectedFile?.name || 'Contenido del archivo'"
      width="80%"
      class="content-dialog"
    >
      <div class="dialog-content">
        <el-input
          v-model="selectedFile.content"
          type="textarea"
          :rows="20"
          placeholder="Contenido del archivo..."
          class="full-content-textarea"
        />
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">Cerrar</el-button>
        <el-button type="primary" @click="saveFromDialog">
          Guardar como libro
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { Close, Document, DocumentAdd, Edit, Upload, View } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ref } from 'vue'

const uploadRef = ref()
const fileList = ref([])
const processedFiles = ref([])
const dialogVisible = ref(false)
const selectedFile = ref(null)

const uploadUrl = 'http://127.0.0.1:8000/upload' // Tu endpoint de subida
const acceptedTypes = '.txt,.docx,.pdf'
const API_URL = 'http://127.0.0.1:8000/libros'

// Validación antes de subir
const beforeUpload = (file) => {
  const isValidType = /\.(txt|docx|pdf)$/i.test(file.name)
  const isValidSize = file.size / 1024 / 1024 < 10 // 10MB

  if (!isValidType) {
    ElMessage.error('Solo se permiten archivos .txt, .docx y .pdf')
    return false
  }
  if (!isValidSize) {
    ElMessage.error('El archivo no puede ser mayor a 10MB')
    return false
  }
  return true
}

// Manejo de éxito en la subida
const handleSuccess = (response, file) => {
  const processedFile = {
    id: Date.now() + Math.random(),
    name: file.name,
    size: file.size,
    content: response.content || 'Contenido extraído del archivo...',
    originalFile: file,
    saving: false
  }
  processedFiles.value.push(processedFile)
  ElMessage.success(`Archivo ${file.name} procesado correctamente`)
}

// Manejo de errores
const handleError = (error, file) => {
  console.error('Error al subir archivo:', error)
  ElMessage.error(`Error al procesar ${file.name}`)
}

// Remover archivo de la lista
const handleRemove = (file) => {
  const index = processedFiles.value.findIndex(f => f.originalFile.uid === file.uid)
  if (index > -1) {
    processedFiles.value.splice(index, 1)
  }
}

// Límite de archivos excedido
const handleExceed = (files, fileList) => {
  ElMessage.warning(`Solo puedes subir máximo 5 archivos. Seleccionaste ${files.length + fileList.length} archivos.`)
}

// Remover archivo procesado
const removeFile = (fileId) => {
  const index = processedFiles.value.findIndex(f => f.id === fileId)
  if (index > -1) {
    processedFiles.value.splice(index, 1)
  }
}

// Formatear tamaño de archivo
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Mostrar contenido completo
const showFullContent = (file) => {
  selectedFile.value = { ...file }
  dialogVisible.value = true
}

// Guardar como libro desde el modal
const saveFromDialog = async () => {
  await saveAsBook(selectedFile.value)
  dialogVisible.value = false
}

// Guardar archivo como libro
const saveAsBook = async (file) => {
  try {
    await ElMessageBox.prompt('Ingresa el título del libro:', 'Guardar como libro', {
      confirmButtonText: 'Guardar',
      cancelButtonText: 'Cancelar',
      inputPlaceholder: 'Título del libro...',
      inputValue: file.name.replace(/\.[^/.]+$/, '') // Quitar extensión
    }).then(async ({ value: titulo }) => {
      const autor = await ElMessageBox.prompt('Ingresa el autor del libro:', 'Información del libro', {
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        inputPlaceholder: 'Nombre del autor...'
      }).then(({ value }) => value)

      file.saving = true

      // Normalizar contenido (como en transcripción)
      let contenidoNormalizado = file.content
        .split("\n")
        .map(linea => linea.trim() === "" ? "⠿".repeat(29) : linea)
        .join("\n")
        .replace(/\r/g, "")

      const body = {
        titulo: titulo || file.name,
        autor: autor || 'Autor desconocido',
        contenido: file.content,
        traducido: contenidoNormalizado,
        estado: 1
      }

      const response = await $fetch(API_URL, {
        method: "POST",
        body
      })

      if (response.id) {
        ElMessage.success(`Libro "${titulo}" guardado correctamente`)
        removeFile(file.id)
      }
    })
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
      ElMessage.error('Error al guardar el libro')
    }
  } finally {
    file.saving = false
  }
}
</script>

<style scoped>
.importar-fullwidth {
  position: absolute;
  left: 270px;
  width: calc(100vw - 270px);
  background-color: #eff0f1;
  min-height: calc(100vh - 140px);
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-section {
  text-align: center;
  margin-bottom: 1rem;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding-top: 8%;
}

.title-icon {
  font-size: 2.5rem;
  color: #4e94c0;
}

.page-subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin: 0;
}

.upload-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.upload-area {
  text-align: center;
  padding: 3rem 2rem;
  border: 2px dashed #d0d7de;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #4e94c0;
  background-color: #f8f9fa;
}

.upload-icon {
  font-size: 4rem;
  color: #4e94c0;
  margin-bottom: 1rem;
}

.upload-text h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.upload-text p {
  color: #7f8c8d;
  margin: 0 0 1.5rem 0;
}

.upload-link {
  color: #4e94c0;
  font-weight: 600;
  cursor: pointer;
}

.file-types {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.file-type {
  background: #4e94c0;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.upload-limit {
  color: #a0a8b0;
  font-size: 0.9rem;
  margin: 0;
}

.files-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rg
}

.section-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
}

.files-grid {
  display: grid;
  gap: 1.5rem;
}

.file-card {
  border: 1px solid #e1e8ed;
  border-radius: 12px;
  padding: 1.5rem;
  background: #fafbfc;
}

.file-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.file-icon {
  font-size: 2rem;
  color: #4e94c0;
}

.file-info {
  flex: 1;
}

.file-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.file-size {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0.2rem 0 0 0;
}

.file-content h5 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.content-preview {
  background: white;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  padding: 1rem;
  color: #555;
  font-size: 0.9rem;
  line-height: 1.4;
  max-height: 100px;
  overflow-y: auto;
}

.file-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

/* Botones personalizados */
.importar-fullwidth :deep(.el-button--primary) {
  background-color: #27ae60;
  border-color: #27ae60;
}

.importar-fullwidth :deep(.el-button--primary:hover) {
  background-color: #2ecc71;
  border-color: #2ecc71;
}

/* Upload personalizado */
.importar-fullwidth :deep(.el-upload-dragger) {
  border: none;
  border-radius: 12px;
  background: transparent;
}

.importar-fullwidth :deep(.el-upload-dragger:hover) {
  border: none;
}

/* Dialog personalizado */
.full-content-textarea :deep(.el-textarea__inner) {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.5;
}

/* Responsive */
@media (max-width: 768px) {
  .importar-fullwidth {
    left: 200px;
    width: calc(100vw - 200px);
  }
  
  .content-container {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.8rem;
  }
  
  .file-actions {
    flex-direction: column;
  }
}
</style>