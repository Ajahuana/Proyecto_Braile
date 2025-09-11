<template>
  <div class="imprimir-fullwidth">
    <div class="content-container">
      <div class="header-section">
        <h2 class="page-title">
          <el-icon class="title-icon"><Files /></el-icon>
          Seleccionar libros para imprimir</h2>
        <p class="page-subtitle">Arrastra los libros que deseas imprimir a la columna de la derecha</p>
      </div>

      <div class="transfer-section">
        <el-transfer
          v-model="seleccionados"
          :data="opciones"
          filterable
          filter-placeholder="Buscar libro"
          :titles="['Libros', 'Para imprimir']"
          :props="{ key: 'id', label: 'titulo' }"
          height="300"
        />
      </div>

      <div class="button-section">
        <el-button type="primary" size="large" @click="imprimir">
          Imprimir
        </el-button>
      </div>

  <div class="p-4">
    <el-select v-model="com" placeholder="Select" style="width: 240px">
      <el-option
          v-for="i in 15"
          :key="`COM${i}`"
          :label="`COM${i}`"
          :value="`COM${i}`"
      />
    </el-select>
    <el-button type="primary" @click="conectarImpresora">Conectar</el-button>
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

    <el-dialog v-model="open" title="Impresion en proceso" :close-on-click-modal="false" >
      <div>Imprimiento.. {{page}}/{{total}}</div>
    </el-dialog>
  </div>
</template>

<script setup>
import { Files } from '@element-plus/icons-vue';
import { onMounted, ref } from 'vue';

const API_URL = 'http://127.0.0.1:8000/libros'
const API_PRINT = 'http://127.0.0.1:8000/imprimir'
const open = ref(false)
const page=ref(0)
const total=ref(0)
const com = ref('')
const libros = ref([])
const seleccionados = ref([])
const opciones = ref([])

async function conectarImpresora() {
  try {
    const res = await $fetch('http://localhost:8000/conectar', {
      method: 'POST',
      body: { com: com.value }
    })

    ElMessage({
      message: res.mensaje,
      type: res.success ? 'success' : 'error',
      duration: 3000
    })
  } catch (err) {
    ElMessage({
      message: '❌ Error al conectar con la API',
      type: 'error',
      duration: 3000
    })
    console.error(err)
  }
}

function brailleADecimal(char) {
  // Obtener el código Unicode del caracter
  const code = char.charCodeAt(0) - 0x2800 // offset braille
  return code // es el decimal
}

function dividirEnLineas(texto) {
  const lineas = []
  // Eliminamos saltos de línea
  let cleanTexto = texto.replace(/\r?\n/g, '')
  let i = 0
  while (i < cleanTexto.length) {
    let chunk = cleanTexto.slice(i, i + 28)
    if (chunk.length < 28) {
      chunk = chunk.padEnd(28, ' ')
    }
    // Convertir cada caracter a decimal braille
    const lineaDecimal = chunk.split('').map(c => brailleADecimal(c)).join(',')
    lineas.push(lineaDecimal)
    i += 28
  }
  return lineas
}


function dividirEnBloques(lineas) {
  const bloques = []
  let i = 0
  while (i < lineas.length) {
    let bloque = lineas.slice(i, i + 30)
    while (bloque.length < 30) {
      bloque.push(' '.repeat(28).split('').join(','))
    }
    const bloqueConIds = bloque.map((linea, idx) => ({
      id: idx + 1,
      linea
    }))
    bloques.push(bloqueConIds)
    i += 30
  }
  return bloques
}

const cargarLibros = async () => {
  try {
    libros.value = await $fetch(API_URL)
    opciones.value = libros.value.map(l => ({ id: l.id, titulo: l.titulo }))
    console.log(libros.value)
  } catch (err) {
    console.error(err)
    ElMessage.error('Error al cargar libros')
  }
}

const enviarBloques = async (bloques) => {
  total.value = bloques.length
  open.value = true
  for (let i = 0; i < bloques.length; i++) {
    page.value = i
    try {
      const res = await fetch(API_PRINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bloque: bloques[i] })
      })
      const data = await res.json()
      console.log(`✅ Respuesta bloque ${i + 1}:`, data)
      ElMessage.success(`Bloque ${i + 1} impreso correctamente`)
    } catch (err) {
      console.error(err)
      ElMessage.error(`Error al imprimir bloque ${i + 1}`)
      break
    }
  }
  open.value = false
}

const imprimir = () => {
  if (seleccionados.value.length === 0) {
    ElMessage.warning('No hay libros en la lista de "Para imprimir"')
    return
  }
  const paraImprimir = libros.value.filter(l =>
    seleccionados.value.includes(l.id)
  )
  const resultadoFinal = []
  paraImprimir.forEach(libro => {
    const lineas = dividirEnLineas(libro.traducido || '')
    const bloques = dividirEnBloques(lineas)
    bloques.forEach(b => resultadoFinal.push(b))
  })
  console.log('📄 Resultado final para impresión:', resultadoFinal)

  enviarBloques(resultadoFinal)
}

onMounted(() => {
  cargarLibros()
})
</script>


<style scoped>
.imprimir-fullwidth {
  position: absolute;
  padding: 0;
  margin: 0;
  left: 270px;
  width: calc(100vw - 270px);
  background-color: #eff0f1;
  min-height: calc(100vh - 140px);
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-section {
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

.page-subtitle {
  font-size: 1.1rem;
  color: #7f8c8d;
  margin: 0;
}

.transfer-section {
  display: flex;
  justify-content: center;
  width: 100%;
}

.button-section {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

/* Personalizar el componente Transfer */
.imprimir-fullwidth :deep(.el-transfer) {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.imprimir-fullwidth :deep(.el-transfer-panel) {
  width: 460px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: white;
}

.imprimir-fullwidth :deep(.el-transfer-panel__header) {
  background: linear-gradient(135deg, #4e94c0 0%, #3a6885 140%);
  color: white;
  font-weight: 600;
  font-size: 20px !important;
  border-radius: 12px 12px 0 0;
  padding: 20px 16px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.imprimir-fullwidth :deep(.el-transfer-panel__body) {
  height: 480px;
}

.imprimir-fullwidth :deep(.el-transfer-panel__list) {
  height: 380px;
}

.imprimir-fullwidth :deep(.el-transfer-panel__item) {
  padding: 12px 16px;
  font-size: 15px;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.2s ease;
}

.imprimir-fullwidth :deep(.el-transfer-panel__item:hover) {
  background-color: #f8f9fa;
}

.imprimir-fullwidth :deep(.el-transfer-panel__filter .el-input__wrapper) {
  border-radius: 8px;
  margin: 10px;
  width: calc(100% - 32px);
}

.imprimir-fullwidth :deep(.el-transfer__buttons) {
  padding: 0 30px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.imprimir-fullwidth :deep(.el-transfer__button) {
  border-radius: 8px;
  font-weight: 500;
  padding: 18px; 
  height: 50px;
}

/* Botón personalizado */
.imprimir-fullwidth :deep(.el-button--primary) {
  background-color: #27ae60;
  border-color: #27ae60;
  padding: 20px; 
  height: 50px;
  font-size: 20px;
}

.imprimir-fullwidth :deep(.el-button--primary:hover) {
  background-color: #2ecc71;
  border-color: #2ecc71;
}

.imprimir-fullwidth :deep(.el-button--primary:disabled) {
  background-color: #bdc3c7;
  border-color: #bdc3c7;
  cursor: not-allowed;
}

/* Tamaño del cuadro de búsqueda */
.imprimir-fullwidth :deep(.el-transfer-panel__filter .el-input__wrapper) {
  border-radius: 12px;
  margin: 16px;
  width: calc(100% - 32px);
  height: 50px !important; 
}

/* Tamaño de letra del input y placeholder */
.imprimir-fullwidth :deep(.el-transfer-panel__filter .el-input__inner) {
  font-size: 18px !important; 
  height: 45px !important; 
  line-height: 45px !important;
}

/* Placeholder específico */
.imprimir-fullwidth :deep(.el-transfer-panel__filter .el-input__inner::placeholder) {
  font-size: 18px !important;
  color: #a0a0a0 !important; 
}

:deep(.el-transfer-panel__header) {
  font-size: 25px !important;
}

:deep(.el-transfer-panel__header span) {
  font-size: 20px !important;
  font-weight: 700 !important;
}

</style>
