from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from datetime import datetime

app = FastAPI(
    title="Leaderboard API",
    description="API REST para el marcador de puntajes",
    version="1.0.0",
)

# Permitir CORS para que el frontend pueda llamar al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta del archivo JSON (base de datos)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puntajes.json")


def leer_puntajes() -> list:
    """Lee los puntajes desde el archivo JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_puntajes(puntajes: list) -> None:
    """Guarda la lista de puntajes en el archivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(puntajes, f, ensure_ascii=False, indent=2)


def calcular_nivel(puntaje: int) -> int:
    """Calcula el nivel del jugador basado en su puntaje."""
    if puntaje < 3000:
        return 1
    elif puntaje < 7000:
        return 2
    else:
        return 3


class NuevoPuntaje(BaseModel):
    jugador: str
    tiempo: str
    puntaje: int


@app.get("/puntajes", summary="Obtener todos los puntajes")
def get_puntajes():
    """Retorna la lista de puntajes ordenada de mayor a menor."""
    puntajes = leer_puntajes()
    return sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)


@app.post("/puntajes", summary="Registrar un nuevo puntaje", status_code=201)
def post_puntaje(nuevo: NuevoPuntaje):
    """Recibe jugador, tiempo y puntaje; calcula nivel y fecha, y guarda en puntajes.json."""
    puntajes = leer_puntajes()

    registro = {
        "jugador": nuevo.jugador,
        "tiempo": nuevo.tiempo,
        "puntaje": nuevo.puntaje,
        "nivel": calcular_nivel(nuevo.puntaje),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    puntajes.append(registro)
    guardar_puntajes(puntajes)

    return registro
