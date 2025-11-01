# 🔔 SOLUCIÓN: Ver Mensajes de Notificación

## 📋 EL PROBLEMA

Los mensajes **SÍ se están generando** en el backend, pero **NO los ves** porque:
- **ShareX** envía la imagen via POST pero **NO abre el navegador**
- Los mensajes solo se ven cuando accedes a `/set_context_form` en el navegador
- La respuesta del API (JSON) solo la ve ShareX, no tú

## ✅ SOLUCIONES (Elige una)

### **Opción 1: Abrir navegador manualmente** ⭐ (MÁS FÁCIL)

1. **Abre tu navegador** y ve a:
   ```
   http://localhost:8000/monitor
   ```

2. **Deja esta pestaña abierta**
   - Se actualizará automáticamente cada 2 segundos
   - Verás los mensajes cada vez que subas una imagen
   - ✅ Verde: "Evidencia agregada correctamente"
   - ❌ Rojo: "Error: Documento abierto..."

---

### **Opción 2: Ver mensajes en el panel de FastAPI** 📊

Los mensajes ya aparecen en la terminal donde corre FastAPI:

```bash
INFO:     ========================================
INFO:     📥 Recibiendo evidencia
INFO:     ✅ Evidencia agregada correctamente: imagen.png
INFO:     📄 Documento: C:\Proyectos\...\evidence.docx
INFO:     🖼️  Imagen: C:\Proyectos\...\imagen.png
INFO:     ========================================
```

---

### **Opción 3: Ver respuesta de ShareX** 📷

ShareX recibe la respuesta en JSON:

```json
{
  "status": "success",
  "message": "✅ Evidencia agregada correctamente",
  "file_path": "...",
  "docx_path": "...",
  "web_url": "http://localhost:8000/set_context_form?notification_message=..."
}
```

**Para ver esto en ShareX:**
1. Abre ShareX → Historial
2. Busca tu última subida
3. Click derecho → "Show response"

---

### **Opción 4: Configurar ShareX para abrir navegador automáticamente** 🤖

**Crear un script .bat:**

```batch
@echo off
start http://localhost:8000/monitor
timeout /t 1
REM Aquí ShareX subirá la imagen
```

**Configurar en ShareX:**
1. Hotkey settings
2. Task → "After upload" → "Run program"
3. Program path: Ruta a tu script .bat

---

## 🎯 RECOMENDACIÓN

**Usa la Opción 1** (abrir `/monitor` en el navegador):
- ✅ Más visual
- ✅ Actualización automática
- ✅ No requiere configuración adicional
- ✅ Puedes dejarlo en segundo plano

---

## 🧪 CÓMO PROBAR

1. **Reinicia FastAPI:**
   ```bash
   uvicorn app:app --reload
   ```

2. **Abre el monitor:**
   ```
   http://localhost:8000/monitor
   ```

3. **Sube una imagen con ShareX**

4. **Observa:**
   - El monitor se actualizará automáticamente
   - Verás el mensaje en verde/rojo
   - Las imágenes aparecerán abajo

---

## 🐛 SI AÚN NO FUNCIONA

1. **Limpia caché del navegador:**
   - Chrome: `Ctrl + Shift + Delete`
   - Marca "Imágenes y archivos en caché"

2. **Verifica la consola del navegador:**
   - `F12` → Console
   - Busca errores en rojo

3. **Verifica logs del servidor:**
   - Busca en la terminal donde corre FastAPI
   - Los mensajes con 📥 ✅ ❌ 📄 🖼️

---

## 📝 NOTAS ADICIONALES

- Los mensajes **siempre** han estado funcionando en el backend
- El problema era que ShareX no muestra la respuesta HTML
- Ahora tienes múltiples formas de ver los mensajes
- El endpoint `/monitor` es la forma más visual y automática

---

## 🆘 SOPORTE

Si ninguna opción funciona:
1. Comparte los logs de la consola del navegador (F12)
2. Comparte los logs de la terminal de FastAPI
3. Indica qué opción probaste
