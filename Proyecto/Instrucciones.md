Necesito programar un sistema que sea simple y fácil de entender sobre un Marcador de Puntajes (Leaderboard). Cada registro tendrá jugador (como Heroe123), tiempo (como 1:23 en minutos y segundos), puntaje (como 5400), nivel (1, 2, 3) y fecha (registrará la fecha actual). Este sistema tendrá:
Frontend: Una sola página web con vue.js o vite.js que muestra una tabla con los mejores puntajes y tiene un formulario simple con los campos: Nombre del Jugador, tiempo y puntaje.
Backend: Una API en FastAPI con dos rutas:
•	GET /puntajes: Lee el archivo puntajes.json y devuelve la lista.
•	POST /puntajes: Recibe un nuevo nombre, tiempo y puntaje, y lo guarda en puntajes.json.
Base de Datos: Un archivo llamado puntajes.json.
