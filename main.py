from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path
import serial
import time
import json

app = FastAPI()

class ImpresoraBraile:
    def __init__(self, puerto="COM3", baudrate=115200):
        self.puerto = puerto
        self.baudrate = baudrate
        self.conexion_serie = None

    def conectar(self):
        try:
            # Si ya hay conexión y está abierta, no volver a abrir
            if self.conexion_serie and self.conexion_serie.is_open:
                print(f"⚡ El puerto {self.puerto} ya está abierto, usando la conexión existente.")
                return True

            print(f"🔌 Intentando conectar con impresora en {self.puerto}...")
            self.conexion_serie = serial.Serial(port=self.puerto, baudrate=self.baudrate, timeout=1)

            if self.conexion_serie.is_open:
                print(f"✅ Conexión establecida con {self.puerto}")
                time.sleep(1)  # Espera para estabilizar conexión
                return True
            else:
                print(f"❌ No se pudo abrir {self.puerto}")
                return False

        except Exception as e:
            print(f"⚠️ Error al conectar con {self.puerto}: {e}")
            return False


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = Path("libros.db")

# Inicializar DB y tabla
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

# -------------------------------
# 🚀 Instancia global de impresora
# -------------------------------
impresora = ImpresoraBraile()
impresora.conectar()

# --- Endpoints CRUD de libros (NO TOCADOS) ---
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

# --- Endpoint de impresión ---
@app.post("/imprimir")
async def imprimir_bloque(bloque: dict):
    """
    Recibe un bloque JSON, lo envía a la impresora
    y espera hasta recibir "TRUE".
    """
    print("📥 Recibido bloque:", bloque)

    if not impresora.conexion_serie or not impresora.conexion_serie.is_open:
        if not impresora.conectar():
            raise HTTPException(status_code=500, detail="No se pudo conectar con la impresora")

    # Enviar bloque como JSON
    json_str = json.dumps(bloque)
    impresora.conexion_serie.write(json_str.encode())

    print("⏳ Esperando respuesta de la impresora...")

    while True:
        if impresora.conexion_serie.in_waiting > 0:
            mensaje = impresora.conexion_serie.readline().decode(errors="ignore").strip()
            if mensaje == "TRUE":
                print("✅ Impresión confirmada")
                return {"status": "ok", "mensaje": "Bloque impreso correctamente"}
            else:
                print("📤 Mensaje recibido:", mensaje)
