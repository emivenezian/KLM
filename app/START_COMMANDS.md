# 🚀 COMANDOS PARA INICIAR LA APLICACIÓN WEB

## Terminal 1 - Backend (FastAPI)

```bash
cd "/Users/emivenezian/Desktop/universidad/ingeniera/años/cuarto/Segundo Semestre/AviationOptimization/KLM_Projects/KLM_Modified/app/backend"
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**O simplemente:**
```bash
cd app/backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

---

## Terminal 2 - Frontend (React)

```bash
cd "/Users/emivenezian/Desktop/universidad/ingeniera/años/cuarto/Segundo Semestre/AviationOptimization/KLM_Projects/KLM_Modified/app/frontend"
npm start
```

**O simplemente:**
```bash
cd app/frontend
npm start
```

---

## URLs una vez iniciados:

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## Para terminar los procesos:

```bash
# Matar backend (puerto 8000)
lsof -ti:8000 | xargs kill -9

# Matar frontend (puerto 3000)
lsof -ti:3000 | xargs kill -9

# O matar ambos a la vez:
lsof -ti:8000 | xargs kill -9; lsof -ti:3000 | xargs kill -9
```

---

## Notas:

- El backend necesita tener el venv activado
- El frontend automáticamente abre el navegador (o puedes ir manualmente a localhost:3000)
- Si los puertos están ocupados, los comandos anteriores los liberarán primero

