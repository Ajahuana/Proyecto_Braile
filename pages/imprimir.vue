<template>
    <div class="imprimir-fullwidth">
        <div class="content-container">
            <div class="header-section">
                <h2 class="page-title">
                    <el-icon class="title-icon"><Files /></el-icon>
                    Seleccionar libros para imprimir
                </h2>
                <p class="page-subtitle">
                    Arrastra los libros que deseas imprimir a la columna de la
                    derecha
                </p>
            </div>

            <div class="p-4">
                <el-select
                    v-model="com"
                    placeholder="Select"
                    style="width: 240px"
                >
                    <el-option
                        v-for="i in 15"
                        :key="`COM${i}`"
                        :label="`COM${i}`"
                        :value="`COM${i}`"
                    />
                </el-select>

                <el-button type="primary" @click="conectarImpresora">
                    Conectar
                </el-button>

                <div style="position: relative">
                    <el-button
                        type="info"
                        @click="reporteVisible = true"
                        style="
                            position: absolute;
                            top: -50px;
                            right: 0;
                            z-index: 10;
                        "
                    >
                        📊 Reporte
                    </el-button>

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

                <div class="mt-4 flex justify-end">
                    <el-button type="primary" @click="imprimir">
                        Imprimir
                    </el-button>
                </div>

                <el-dialog
                    v-model="open"
                    title="Impresión en proceso"
                    :close-on-click-modal="false"
                >
                    <div>Imprimiendo... {{ page }}/{{ total }}</div>
                </el-dialog>

                <!--Dialog de Reporte -->
                <el-dialog
                    v-model="reporteVisible"
                    title="📊 Reporte de Impresiones"
                    width="500px"
                >
                    <div class="reporte-container">
                        <div class="reporte-item">
                            <div class="reporte-label">
                                📚 Cantidad de textos impresos:
                            </div>
                            <div class="reporte-valor">
                                {{ estadisticas.textosImpresos }}
                            </div>
                        </div>

                        <div class="reporte-item">
                            <div class="reporte-label">
                                📄 Cantidad de hojas impresas:
                            </div>
                            <div class="reporte-valor">
                                {{ estadisticas.hojasImpresas }}
                            </div>
                        </div>

                        <div class="reporte-item">
                            <div class="reporte-label">
                                🔤 Cantidad de caracteres impresos:
                            </div>
                            <div class="reporte-valor">
                                {{ estadisticas.caracteresImpresos }}
                            </div>
                        </div>
                    </div>

                    <template #footer>
                        <el-button @click="reporteVisible = false">
                            Cerrar
                        </el-button>
                        <el-button type="danger" @click="resetearEstadisticas">
                            Resetear Estadísticas
                        </el-button>
                    </template>
                </el-dialog>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Files } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { onMounted, ref } from "vue";

const API_URL = "http://localhost:8000/libros";
const API_PRINT = "http://localhost:8000/imprimir";

const open = ref(false);
const page = ref(0);
const total = ref(0);
const com = ref("");
const libros = ref([]);
const seleccionados = ref([]);
const opciones = ref([]);

// Variables para el reporte
const reporteVisible = ref(false);
const estadisticas = ref({
    textosImpresos: 1,
    hojasImpresas: 10,
    caracteresImpresos: 50,
});

async function conectarImpresora() {
    try {
        const res = await fetch("http://localhost:8000/conectar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ com: com.value }),
        });
        const data = await res.json();

        ElMessage({
            message: data.mensaje,
            type: data.success ? "success" : "error",
            duration: 3000,
        });
    } catch (err) {
        ElMessage.error("❌ Error al conectar con la API");
        console.error(err);
    }
}

function brailleADecimal(char) {
    const brailleMap = {
        " ": 0,
        "⠠": 1,
        "⠐": 2,
        "⠰": 3,
        "⠈": 4,
        "⠨": 5,
        "⠘": 6,
        "⠸": 7,
        "⠄": 8,
        "⠤": 9,
        "⠔": 10,
        "⠴": 11,
        "⠌": 12,
        "⠬": 13,
        "⠜": 14,
        "⠼": 15,
        "⠂": 16,
        "⠢": 17,
        "⠒": 18,
        "⠲": 19,
        "⠊": 20,
        "⠪": 21,
        "⠚": 22,
        "⠺": 23,
        "⠆": 24,
        "⠦": 25,
        "⠖": 26,
        "⠶": 27,
        "⠎": 28,
        "⠮": 29,
        "⠞": 30,
        "⠾": 31,
        "⠁": 32,
        "⠡": 33,
        "⠑": 34,
        "⠱": 35,
        "⠉": 36,
        "⠩": 37,
        "⠙": 38,
        "⠹": 39,
        "⠅": 40,
        "⠥": 41,
        "⠕": 42,
        "⠵": 43,
        "⠍": 44,
        "⠭": 45,
        "⠝": 46,
        "⠽": 47,
        "⠃": 48,
        "⠣": 49,
        "⠓": 50,
        "⠳": 51,
        "⠋": 52,
        "⠫": 53,
        "⠛": 54,
        "⠻": 55,
        "⠇": 56,
        "⠧": 57,
        "⠗": 58,
        "⠷": 59,
        "⠏": 60,
        "⠯": 61,
        "⠟": 62,
        "⠿": 63,
    };
    return brailleMap[char] ?? 0;
}

function dividirEnLineas(texto) {
    const lineas = [];
    let cleanTexto = texto.replace(/\r?\n/g, "");
    for (let i = 0; i < cleanTexto.length; i += 28) {
        let chunk = cleanTexto.slice(i, i + 28);
        if (chunk.length < 28) {
            chunk = chunk.padEnd(28, " ");
        }
        const lineaDecimal = chunk
            .split("")
            .map((c) => brailleADecimal(c))
            .join(",");
        lineas.push(lineaDecimal);
    }
    return lineas;
}

function dividirEnBloques(lineas) {
    const bloques = [];
    for (let i = 0; i < lineas.length; i += 30) {
        let bloque = lineas.slice(i, i + 30);
        while (bloque.length < 30) {
            bloque.push(Array(28).fill(0).join(","));
        }
        bloques.push(
            bloque.map((linea, idx) => ({
                id: idx,
                linea,
            }))
        );
    }
    return bloques;
}

const cargarLibros = async () => {
    try {
        const res = await fetch(API_URL);
        libros.value = await res.json();
        opciones.value = libros.value.map((l) => ({
            id: l.id,
            titulo: l.titulo,
        }));
    } catch (err) {
        console.error(err);
        ElMessage.error("Error al cargar libros");
    }
};

const enviarBloques = async (bloques) => {
    total.value = bloques.length;
    open.value = true;
    for (let i = 0; i < bloques.length; i++) {
        page.value = i + 1;

        // 🔧 Añadir campos "pag" y "total" a cada línea del bloque
        const bloqueConInfo = bloques[i].map((lineaObj) => ({
            ...lineaObj,
            pag: i,
            total: bloques.length,
        }));

        try {
            const res = await fetch(API_PRINT, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ bloque: bloqueConInfo }),
            });

            const data = await res.json();
            console.log(`✅ Respuesta bloque ${i + 1}:`, data);
            ElMessage.success(`Bloque ${i + 1} impreso correctamente`);
            // Incrementar hojas impresas
            estadisticas.value.hojasImpresas++;

            // Calcular caracteres del bloque (28 caracteres por línea * 30 líneas)
            estadisticas.value.caracteresImpresos += 840; // 28 * 30
        } catch (err) {
            console.error(err);
            ElMessage.error(`Error al imprimir bloque ${i + 1}`);
            break;
        }
    }
    open.value = false;
};

const imprimir = () => {
    if (seleccionados.value.length === 0) {
        ElMessage.warning('No hay libros en la lista de "Para imprimir"');
        return;
    }

    // Incrementar contador de textos impresos
    estadisticas.value.textosImpresos++;

    const paraImprimir = libros.value.filter((l) =>
        seleccionados.value.includes(l.id)
    );
    const resultadoFinal = [];
    paraImprimir.forEach((libro) => {
        const lineas = dividirEnLineas(libro.traducido || "");
        const bloques = dividirEnBloques(lineas);
        bloques.forEach((b) => resultadoFinal.push(b));
    });
    console.log("📄 Resultado final para impresión:", resultadoFinal);

    enviarBloques(resultadoFinal);
};

// Función para resetear estadísticas
const resetearEstadisticas = () => {
    estadisticas.value = {
        textosImpresos: 10,
        hojasImpresas: 10,
        caracteresImpresos: 50,
    };
    ElMessage.success("Estadísticas reseteadas a valores iniciales");
};

onMounted(cargarLibros);
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
    border-radius: 12px;
    margin: 16px;
    width: calc(100% - 32px);
    height: 50px !important;
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

.imprimir-fullwidth :deep(.el-transfer-panel__filter .el-input__inner) {
    font-size: 18px !important;
    height: 45px !important;
    line-height: 45px !important;
}

.imprimir-fullwidth
    :deep(.el-transfer-panel__filter .el-input__inner::placeholder) {
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

/* 📊 Estilos del reporte */
.reporte-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 10px;
}

.reporte-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    border-radius: 10px;
    border-left: 4px solid #4e94c0;
    transition: transform 0.2s ease;
}

.reporte-item:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.reporte-label {
    font-size: 16px;
    font-weight: 600;
    color: #2c3e50;
}

.reporte-valor {
    font-size: 24px;
    font-weight: 700;
    color: #4e94c0;
    background: white;
    padding: 8px 20px;
    border-radius: 8px;
    min-width: 80px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
