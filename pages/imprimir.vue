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

    <el-dialog v-model="open" title="Impresion en proceso" :close-on-click-modal="false" >
      <div>Imprimiento.. {{page}}/{{total}}</div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'

const API_URL = 'http://127.0.0.1:8000/libros'
const API_PRINT = 'http://127.0.0.1:8000/imprimir'
const open = ref(false)
const page=ref(0)
const total=ref(0)

const libros = ref([])
const seleccionados = ref([])
const opciones = ref([])

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

