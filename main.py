from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path
from pydantic import BaseModel
import serial
import time
import json
from fastapi import UploadFile, File, HTTPException
import tempfile
import os
import docx2txt
import fitz  # PyMuPDF para PDF
app = FastAPI()

# -------------------------------
# 🔐 CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 📡 Modelos
# -------------------------------
class ConexionRequest(BaseModel):
    com: str

# -------------------------------
# 🖨️ Clase impresora
# -------------------------------
class ImpresoraBraile:
    def __init__(self, puerto="COM7", baudrate=115200):
        self.puerto = puerto
        self.baudrate = baudrate
        self.conexion_serie = None

    def conectar(self):
        try:
            if self.conexion_serie and self.conexion_serie.is_open:
                return {
                    "success": True,
                    "mensaje": f"⚡ El puerto {self.puerto} ya está abierto."
                }

            self.conexion_serie = serial.Serial(
                port=self.puerto,
                baudrate=self.baudrate,
                timeout=1
            )

            if self.conexion_serie.is_open:
                time.sleep(1)
                return {
                    "success": True,
                    "mensaje": f"✅ Conexión establecida con {self.puerto}"
                }
            else:
                return {
                    "success": False,
                    "mensaje": f"❌ No se pudo abrir {self.puerto}"
                }

        except Exception as e:
            return {
                "success": False,
                "mensaje": f"⚠️ Error al conectar con {self.puerto}: {e}"
            }

# -------------------------------
# 🚀 Endpoints
# -------------------------------

@app.post("/conectar")
def conectar_impresora(data: ConexionRequest):
    impresora.puerto = data.com  # actualizar puerto dinámicamente
    return impresora.conectar()

# -------------------------------
# 📚 Base de datos
# -------------------------------
DB_PATH = Path("libros.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            contenido TEXT,
            traducido TEXT,
            estado INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Instancia global de impresora
impresora = ImpresoraBraile()

# -------------------------------
# 📚 Endpoints CRUD Libros
# -------------------------------
@app.get("/libros")
def get_libros():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM libros")
    rows = c.fetchall()
    conn.close()
    return [
        {"id": r[0], "titulo": r[1], "autor": r[2], "contenido": r[3], "traducido": r[4], "estado": r[5]}
        for r in rows
    ]

@app.post("/libros")
def add_libro(libro: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO libros (titulo, autor, contenido, traducido, estado) VALUES (?, ?, ?, ?, ?)",
        (
            libro.get("titulo"),
            libro.get("autor"),
            libro.get("contenido"),
            libro.get("traducido"),
            libro.get("estado", 1)
        )
    )
    conn.commit()
    libro_id = c.lastrowid
    conn.close()
    return {"success": True, "id": libro_id}

@app.put("/libros/{libro_id}")
def update_libro(libro_id: int, libro: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        UPDATE libros
        SET titulo=?, autor=?, contenido=?, traducido=?, estado=?
        WHERE id=?
        """,
        (
            libro.get("titulo"),
            libro.get("autor"),
            libro.get("contenido"),
            libro.get("traducido"),
            libro.get("estado", 1),
            libro_id,
        )
    )
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    conn.commit()
    conn.close()
    return {"success": True}

@app.delete("/libros")
def delete_libro(libro: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM libros WHERE id=?", (libro.get("id"),))
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    conn.commit()
    conn.close()
    return {"success": True}

@app.get("/libros/{libro_id}")
def get_libro(libro_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM libros WHERE id=?", (libro_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {
        "id": row[0],
        "titulo": row[1],
        "autor": row[2],
        "contenido": row[3],
        "traducido": row[4],
        "estado": row[5],
    }

# -------------------------------
# 🖨️ Endpoint de impresión
# -------------------------------
@app.post("/imprimir")
async def imprimir_bloque(bloque: dict):
    """
    Recibe un bloque JSON, lo envía a la impresora
    y espera hasta recibir "TRUE".
    """
    print("📥 Recibido bloque:", bloque)

    if not impresora.conexion_serie or not impresora.conexion_serie.is_open:
        result = impresora.conectar()
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("mensaje"))

    if not impresora.conexion_serie or not impresora.conexion_serie.is_open:
        raise HTTPException(status_code=500, detail="No hay conexión con la impresora")

    try:
        # Enviar bloque como JSON
        json_str = json.dumps(bloque)
        impresora.conexion_serie.write(json_str.encode())
        impresora.conexion_serie.write("|\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar datos: {e}")

    print("⏳ Esperando respuesta de la impresora...")

    while True:
        if impresora.conexion_serie.in_waiting > 0:
            mensaje = impresora.conexion_serie.readline().decode(errors="ignore").strip()
            if mensaje == "TRUE":
                print("✅ Impresión confirmada")
                return {"status": "ok", "mensaje": "Bloque impreso correctamente"}
            else:
                print("📤 Mensaje recibido:", mensaje)

# -------------------------------
#  Endpoint de cargado de archivos
# -------------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Guardar archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        content = ""

        # Procesar según la extensión
        if file.filename.lower().endswith(".txt"):
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

        elif file.filename.lower().endswith(".docx"):
            content = docx2txt.process(tmp_path)

        elif file.filename.lower().endswith(".pdf"):
            doc = fitz.open(tmp_path)
            for page in doc:
                content += page.get_text()

        else:
            raise HTTPException(status_code=400, detail="Formato no soportado")

        # Eliminar archivo temporal
        os.remove(tmp_path)

        return {
            "success": True,
            "filename": file.filename,
            "content": content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar archivo: {str(e)}")