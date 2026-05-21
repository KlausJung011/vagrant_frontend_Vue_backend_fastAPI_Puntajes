# 🏆 Leaderboard — Proyecto de Sistemas 2

Sistema de marcador de puntajes con **FastAPI** (backend) + **Vue.js** (frontend), desplegado automáticamente en una VM mediante **Vagrant** + **Ansible**.

---

## Estructura del proyecto

```
P41/
├── .gitignore
├── Proyecto/
│   ├── backend/
│   │   ├── main.py           ← API REST (FastAPI)
│   │   ├── puntajes.json     ← Base de datos JSON
│   │   └── requirements.txt  ← Dependencias Python
│   └── frontend/
│       ├── index.html
│       ├── package.json
│       ├── vite.config.js
│       └── src/
│           ├── main.js
│           └── App.vue       ← Interfaz de usuario
└── Sistema pruebas/
    ├── Vagrantfile           ← Configuración de la VM
    └── ansible/
        └── playbook.yml      ← Script de instalación automática
```

---

## Cómo funciona la arquitectura

```
Tu PC (Windows)
 │
 └─ vagrant up  ──→  VM Ubuntu 24.04 (VirtualBox)
                          │
                          ├─ Nginx (puerto 80 → tu PC: 8080)
                          │   ├─ Sirve: frontend/dist/ (Vue compilado)
                          │   └─ Proxy: /puntajes → FastAPI
                          │
                          └─ FastAPI (puerto 8000 → tu PC: 8001)
                              └─ Lee/escribe: backend/puntajes.json
```

Después de `vagrant up`:
- **Frontend:** http://localhost:8080
- **API (debug):** http://localhost:8001/puntajes
- **Swagger UI:** http://localhost:8001/docs

---

## API REST

| Método | Ruta        | Descripción                        |
|--------|-------------|------------------------------------|
| GET    | /puntajes   | Lista todos los puntajes (ordenados por puntaje desc) |
| POST   | /puntajes   | Registra un nuevo puntaje          |

### Ejemplo POST
```json
{
  "jugador": "Heroe123",
  "tiempo": "1:23",
  "puntaje": 5400
}
```

### Respuesta POST
```json
{
  "jugador": "Heroe123",
  "tiempo": "1:23",
  "puntaje": 5400,
  "nivel": 2,
  "fecha": "2026-05-21 08:15"
}
```

**Niveles calculados automáticamente:**
- Nivel 1: puntaje < 3000
- Nivel 2: puntaje 3000–6999
- Nivel 3: puntaje ≥ 7000

---

## Desarrollo local (sin VM)

### Backend
```bash
cd Proyecto/backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload
# API disponible en http://localhost:8000
```

### Frontend
```bash
cd Proyecto/frontend
npm install
npm run dev
# App disponible en http://localhost:5173
# (el proxy de Vite redirige /puntajes → http://localhost:8000)
```

---

## Despliegue en VM

```bash
# Desde la carpeta "Sistema pruebas/"
vagrant up           # primera vez: crea la VM + provisiona
vagrant provision    # re-ejecutar Ansible (sin recrear la VM)
vagrant ssh          # entrar a la VM
vagrant halt         # apagar la VM
vagrant destroy      # eliminar la VM completamente
```

---

## Conexión VS Code Remote SSH (Punto Extra)

1. Instala la extensión **Remote - SSH** en VS Code.
2. Con la VM encendida (`vagrant up`), ejecuta en PowerShell:
   ```powershell
   # Desde la carpeta "Sistema pruebas/"
   vagrant ssh-config >> $HOME\.ssh\config
   ```
3. En VS Code: `Ctrl+Shift+P` → **Remote-SSH: Connect to Host** → selecciona **default**.
4. ¡Estás dentro de la VM editando con VS Code!

---

## Tecnologías

| Capa            | Tecnología           |
|-----------------|----------------------|
| Frontend        | Vue 3 + Vite         |
| Backend         | FastAPI + Uvicorn    |
| Base de datos   | JSON (puntajes.json) |
| Servidor web    | Nginx                |
| Servicio        | systemd              |
| VM              | Vagrant + VirtualBox |
| Provisión       | Ansible              |
