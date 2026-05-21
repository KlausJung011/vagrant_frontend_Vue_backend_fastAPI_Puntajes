<template>
  <div class="app">
    <!-- ===== HEADER ===== -->
    <header class="header">
      <div class="header-content">
        <div class="trophy-icon">🏆</div>
        <div>
          <h1 class="title">LEADERBOARD</h1>
          <p class="subtitle">Marcador de Puntajes &bull; Proyecto de Sistemas 2</p>
        </div>
      </div>
    </header>

    <main class="main">
      <!-- ===== FORMULARIO ===== -->
      <section class="card form-card">
        <h2 class="card-title">
          <span class="icon">✏️</span> Registrar Puntaje
        </h2>

        <form @submit.prevent="submitScore" class="form" id="score-form">
          <div class="form-row">
            <div class="form-group">
              <label class="label" for="input-jugador">Jugador</label>
              <input
                id="input-jugador"
                v-model="form.jugador"
                class="input"
                placeholder="Heroe123"
                required
                maxlength="30"
                autocomplete="off"
              />
            </div>

            <div class="form-group">
              <label class="label" for="input-tiempo">Tiempo (mm:ss)</label>
              <input
                id="input-tiempo"
                v-model="form.tiempo"
                class="input"
                placeholder="1:23"
                required
                pattern="[0-9]+:[0-5][0-9]"
                title="Formato: minutos:segundos — ejemplo: 1:23"
                autocomplete="off"
              />
            </div>

            <div class="form-group">
              <label class="label" for="input-puntaje">Puntaje</label>
              <input
                id="input-puntaje"
                v-model.number="form.puntaje"
                class="input"
                type="number"
                min="0"
                max="99999"
                placeholder="5400"
                required
              />
            </div>
          </div>

          <button
            id="btn-registrar"
            type="submit"
            class="btn-submit"
            :disabled="loading"
          >
            <span v-if="loading" class="loading-text">Guardando</span>
            <span v-else>🚀 Registrar Puntaje</span>
          </button>

          <p v-if="successMsg" class="success-msg" role="alert">{{ successMsg }}</p>
          <p v-if="errorMsg"   class="error-msg"   role="alert">{{ errorMsg }}</p>
        </form>
      </section>

      <!-- ===== TABLA ===== -->
      <section class="card table-card">
        <div class="table-header">
          <h2 class="card-title">
            <span class="icon">🎮</span> Mejores Puntajes
          </h2>
          <button id="btn-refresh" class="btn-refresh" @click="fetchPuntajes" title="Actualizar">
            <span :class="{ spinning: loadingData }">↺</span>
          </button>
        </div>

        <!-- Cargando -->
        <div v-if="loadingData" class="state-container">
          <div class="spinner"></div>
          <p>Cargando puntajes...</p>
        </div>

        <!-- Sin datos -->
        <div v-else-if="puntajes.length === 0" class="state-container empty-state">
          <p class="state-icon">🎯</p>
          <p class="state-title">¡No hay puntajes todavía!</p>
          <p class="state-sub">Sé el primero en registrar tu puntaje</p>
        </div>

        <!-- Tabla de puntajes -->
        <div v-else class="table-wrapper">
          <table class="table" id="tabla-puntajes">
            <thead>
              <tr>
                <th>#</th>
                <th>Jugador</th>
                <th>Tiempo</th>
                <th>Puntaje</th>
                <th>Nivel</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(p, i) in puntajes"
                :key="i"
                class="table-row"
                :class="`rank-${Math.min(i + 1, 4)}`"
                :style="{ animationDelay: `${i * 60}ms` }"
              >
                <td class="rank-cell">
                  <span class="rank-badge">{{ rankIcon(i) }}</span>
                </td>
                <td class="player-cell">{{ p.jugador }}</td>
                <td class="time-cell">{{ p.tiempo }}</td>
                <td class="score-cell">{{ p.puntaje.toLocaleString('es') }}</td>
                <td>
                  <span class="level-badge" :class="`level-${p.nivel}`">
                    Lvl {{ p.nivel }}
                  </span>
                </td>
                <td class="date-cell">{{ p.fecha }}</td>
              </tr>
            </tbody>
          </table>

          <p class="table-count">{{ puntajes.length }} registro{{ puntajes.length !== 1 ? 's' : '' }}</p>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>Leaderboard System &bull; Proyecto de Sistemas 2 &bull; FastAPI + Vue.js</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// ── Estado ─────────────────────────────────────────────────────────────────
const puntajes    = ref([])
const loadingData = ref(true)
const loading     = ref(false)
const successMsg  = ref('')
const errorMsg    = ref('')

const form = ref({ jugador: '', tiempo: '', puntaje: '' })

// ── Utilidades ──────────────────────────────────────────────────────────────
const rankIcon = (i) => ['🥇', '🥈', '🥉'][i] ?? `#${i + 1}`

// ── API ─────────────────────────────────────────────────────────────────────
const fetchPuntajes = async () => {
  loadingData.value = true
  try {
    const res = await fetch('/puntajes')
    if (!res.ok) throw new Error('Error al cargar los puntajes')
    puntajes.value = await res.json()
  } catch (e) {
    console.error(e)
  } finally {
    loadingData.value = false
  }
}

const submitScore = async () => {
  loading.value  = true
  successMsg.value = ''
  errorMsg.value   = ''

  try {
    const res = await fetch('/puntajes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jugador: form.value.jugador,
        tiempo:  form.value.tiempo,
        puntaje: Number(form.value.puntaje),
      }),
    })

    if (!res.ok) throw new Error('Error al guardar el puntaje')

    form.value = { jugador: '', tiempo: '', puntaje: '' }
    successMsg.value = '¡Puntaje registrado con éxito! 🎉'
    await fetchPuntajes()
    setTimeout(() => { successMsg.value = '' }, 3500)
  } catch (e) {
    errorMsg.value = 'No se pudo conectar al servidor. Verifica que el backend esté activo.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchPuntajes)
</script>

<!-- ────────────────────────────────────────────────────────────────────────
     ESTILOS GLOBALES
────────────────────────────────────────────────────────────────────────── -->
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --bg:        #0d0d1a;
  --bg2:       #12122a;
  --card:      rgba(255, 255, 255, 0.04);
  --border:    rgba(255, 255, 255, 0.08);
  --cyan:      #00d4ff;
  --purple:    #7b2dff;
  --gold:      #ffd700;
  --silver:    #c0c0c0;
  --bronze:    #cd7f32;
  --text:      #e8e8ff;
  --muted:     rgba(232, 232, 255, 0.45);
  --success:   #00ff88;
  --error:     #ff4d6d;
  --radius:    18px;
}

html { scroll-behavior: smooth; }

body {
  font-family: 'Exo 2', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  background-image:
    radial-gradient(ellipse 60% 50% at 15% 15%, rgba(123, 45, 255, 0.18) 0%, transparent 70%),
    radial-gradient(ellipse 60% 50% at 85% 85%, rgba(0, 212, 255, 0.12) 0%, transparent 70%);
}
</style>

<!-- ────────────────────────────────────────────────────────────────────────
     ESTILOS DEL COMPONENTE
────────────────────────────────────────────────────────────────────────── -->
<style scoped>

/* ── Layout ─────────────────────────────────────────────────────────────── */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Header ─────────────────────────────────────────────────────────────── */
.header {
  padding: 2rem 2.5rem;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(
    135deg,
    rgba(123, 45, 255, 0.22) 0%,
    rgba(0, 212, 255, 0.10) 100%
  );
  backdrop-filter: blur(12px);
}

.header-content {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.trophy-icon {
  font-size: 3.8rem;
  filter: drop-shadow(0 0 22px rgba(255, 215, 0, 0.65));
  animation: float 3.2s ease-in-out infinite;
  user-select: none;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(-3deg); }
  50%       { transform: translateY(-10px) rotate(3deg); }
}

.title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 900;
  letter-spacing: 5px;
  line-height: 1;
  background: linear-gradient(135deg, var(--cyan) 0%, var(--purple) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: var(--muted);
  font-size: 0.85rem;
  font-weight: 400;
  margin-top: 0.35rem;
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* ── Main ────────────────────────────────────────────────────────────────── */
.main {
  flex: 1;
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 2rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ── Cards ───────────────────────────────────────────────────────────────── */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2rem 2.2rem;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
  transition: box-shadow 0.35s ease;
}

.card:hover {
  box-shadow: 0 14px 45px rgba(123, 45, 255, 0.18);
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1.6rem;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.icon { font-size: 1.3rem; }

/* ── Formulario ──────────────────────────────────────────────────────────── */
.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.2rem;
  margin-bottom: 1.6rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.label {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--cyan);
  text-transform: uppercase;
  letter-spacing: 1.2px;
}

.input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.85rem 1rem;
  color: var(--text);
  font-family: 'Exo 2', sans-serif;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.25s ease;
  outline: none;
  width: 100%;
}

.input:focus {
  border-color: var(--cyan);
  box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.18);
  background: rgba(0, 212, 255, 0.05);
}

.input::placeholder { color: var(--muted); }

/* Remove number input arrows */
.input[type="number"]::-webkit-inner-spin-button,
.input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; }

.btn-submit {
  display: block;
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, var(--purple) 0%, var(--cyan) 100%);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-family: 'Exo 2', sans-serif;
  font-size: 1.05rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-submit::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.12);
  opacity: 0;
  transition: opacity 0.25s;
}

.btn-submit:hover:not(:disabled)::before { opacity: 1; }
.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(123, 45, 255, 0.45);
}
.btn-submit:active:not(:disabled) { transform: translateY(0); }
.btn-submit:disabled { opacity: 0.65; cursor: not-allowed; }

.loading-text::after {
  content: '';
  animation: dots 1.5s steps(4, end) infinite;
}
@keyframes dots {
  0%,20%  { content: ''; }
  40%     { content: '.'; }
  60%     { content: '..'; }
  80%,100%{ content: '...'; }
}

.success-msg {
  margin-top: 0.9rem;
  color: var(--success);
  text-align: center;
  font-weight: 600;
  font-size: 0.95rem;
  animation: fadeUp 0.3s ease;
}

.error-msg {
  margin-top: 0.9rem;
  color: var(--error);
  text-align: center;
  font-weight: 500;
  font-size: 0.9rem;
  animation: fadeUp 0.3s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Tabla ─────────────────────────────────────────────────────────────── */
.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0;
}

.btn-refresh {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--muted);
  width: 36px;
  height: 36px;
  font-size: 1.3rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
  margin-bottom: 1.6rem;
}
.btn-refresh:hover { color: var(--cyan); border-color: var(--cyan); }

@keyframes spin { to { transform: rotate(360deg); } }
.spinning { display: inline-block; animation: spin 0.7s linear infinite; }

.table-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid var(--border);
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
  min-width: 540px;
}

.table th {
  background: rgba(123, 45, 255, 0.18);
  color: var(--cyan);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  font-size: 0.72rem;
  padding: 1rem 1.2rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}

.table-row {
  border-bottom: 1px solid var(--border);
  transition: background 0.2s ease;
  animation: slideIn 0.45s ease both;
}
.table-row:last-child { border-bottom: none; }
.table-row:hover { background: rgba(255, 255, 255, 0.04); }

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-12px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Filas especiales por ranking */
.rank-1 { background: rgba(255, 215, 0,   0.06); }
.rank-2 { background: rgba(192, 192, 192, 0.03); }
.rank-3 { background: rgba(205, 127, 50,  0.03); }

.table td { padding: 0.85rem 1.2rem; }

.rank-cell { text-align: center; }
.rank-badge { font-size: 1.35rem; display: inline-block; }

.rank-1 .rank-badge { filter: drop-shadow(0 0 8px rgba(255,215,0,  0.9)); }
.rank-2 .rank-badge { filter: drop-shadow(0 0 8px rgba(192,192,192,0.9)); }
.rank-3 .rank-badge { filter: drop-shadow(0 0 8px rgba(205,127,50, 0.9)); }

.player-cell { font-weight: 700; }

.time-cell {
  font-family: 'Courier New', monospace;
  color: var(--muted);
  font-size: 0.95rem;
}

.score-cell {
  font-weight: 900;
  font-size: 1.1rem;
  color: var(--cyan);
}

.level-badge {
  display: inline-block;
  padding: 0.2rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  white-space: nowrap;
}
.level-1 {
  background: rgba(0, 255, 136, 0.12);
  color: #00ff88;
  border: 1px solid rgba(0, 255, 136, 0.3);
}
.level-2 {
  background: rgba(0, 212, 255, 0.12);
  color: #00d4ff;
  border: 1px solid rgba(0, 212, 255, 0.3);
}
.level-3 {
  background: rgba(123, 45, 255, 0.15);
  color: #b57bff;
  border: 1px solid rgba(123, 45, 255, 0.35);
}

.date-cell {
  color: var(--muted);
  font-size: 0.83rem;
}

.table-count {
  margin-top: 0.8rem;
  text-align: right;
  color: var(--muted);
  font-size: 0.8rem;
}

/* ── Estados vacío / carga ─────────────────────────────────────────────── */
.state-container {
  text-align: center;
  padding: 3rem 2rem;
  color: var(--muted);
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--border);
  border-top-color: var(--cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

.state-icon  { font-size: 3.2rem; margin-bottom: 0.6rem; }
.state-title { font-size: 1.1rem; font-weight: 600; color: var(--text); }
.state-sub   { font-size: 0.85rem; margin-top: 0.35rem; }

/* ── Footer ─────────────────────────────────────────────────────────────── */
.footer {
  text-align: center;
  padding: 1.4rem;
  color: var(--muted);
  font-size: 0.78rem;
  border-top: 1px solid var(--border);
  letter-spacing: 0.5px;
}

/* ── Responsive ─────────────────────────────────────────────────────────── */
@media (max-width: 700px) {
  .header         { padding: 1.5rem; }
  .trophy-icon    { font-size: 2.8rem; }
  .main           { padding: 1.5rem 1rem; }
  .card           { padding: 1.4rem; }
  .form-row       { grid-template-columns: 1fr; }
  .date-cell      { display: none; }
}
</style>
