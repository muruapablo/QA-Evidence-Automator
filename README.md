![EviQA Banner](banner.png)
# 📊 QA Evidence Automator - RESUMEN COMPLETO

## 🎯 ¿Qué incluye ahora?

### ✅ **Funcionalidades Originales**
1. Subir imágenes con ShareX
2. Generar documentos Word automáticamente
3. Organizar evidencias por test
4. Panel web para configurar contexto

### ⭐ **NUEVAS Funcionalidades Implementadas**

#### 1. **Modal de Logs en Tiempo Real Mejorado** 🔥 (v1.1)
- ✨ **Diseño no invasivo**: Aparece en esquina inferior derecha (450px × 600px)
- ✨ **No tapa el formulario**: Puedes seguir trabajando mientras ves los logs
- ✨ **Destacado automático**: Mensajes con emojis importantes resaltados visualmente
  - ✅ **Éxito** → Fondo verde, borde verde brillante
  - ❌ **Error** → Fondo rojo, borde rojo brillante
  - ⚠️ **Advertencia** → Fondo rojo, borde rojo brillante
  - 🎯 🚀 📝 💾 ⏰🔍 → Destacado especial con sombra
- 🎨 **Scrollbar personalizado** con gradiente del tema
- 📱 **Diseño responsive** para móviles y tablets
- ⚡ Actualización automática con Server-Sent Events
- 🌈 Colores por nivel (INFO, WARNING, ERROR, DEBUG)
- 🎯 Botón flotante siempre visible
- ⌨️ Se cierra con `Escape`, `X`, o botón de cerrar

#### 2. **Mensajes de Notificación Mejorados**
- Animaciones suaves al aparecer
- Colores llamativos (verde/rojo)
- Auto-limpieza de URL después de 3 segundos
- Prevención de caché

#### 3. **Monitor Auto-Refresh**
- Página `/monitor` que se actualiza cada 2 segundos
- Ideal para segunda pantalla
- Spinner animado mientras carga

---

## 🚀 Inicio Rápido

### **1. Instalación** (si es primera vez)
```bash
# Clonar repositorio
git clone <URL-del-repo>
cd QA-Evidence-Automator

# Crear entorno virtual
python -m venv venv

# Activar entorno
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt
```

### **2. Ejecutar Servidor**
```bash
uvicorn app:app --reload
```

### **3. Abrir Navegador**
```
http://localhost:8000/set_context_form
```

### **4. Configurar ShareX**
- Importar archivo: `sharex/QA_Evidence_API.sxcu`
- Endpoint: `http://localhost:8000/evidences`

---

## 📱 Interfaces Disponibles

### **1. Formulario Principal** (`/set_context_form`)
**URL:** `http://localhost:8000/set_context_form`

**Funciones:**
- Configurar Test ID y Paso
- Ver imágenes subidas
- Ver notificaciones de éxito/error
- **NUEVO:** Botón flotante para abrir logs

**Características:**
- 🟢 Mensaje verde: Evidencia agregada correctamente
- 🔴 Mensaje rojo: Error (documento abierto, etc.)
- 🖼️ Galería de evidencias del test actual
- 📊 Botón flotante: "Ver Logs en Tiempo Real"

### **2. Modal de Logs** (dentro del formulario)
**Abrir:** Click en botón flotante o desde formulario

**Funciones:**
- Ver logs del servidor en tiempo real
- Filtrado visual por colores
- Auto-scroll al final
- Limpiar logs con un click

**Características:**
- 🔵 INFO - Azul
- 🟠 WARNING - Naranja  
- 🔴 ERROR - Rojo
- ⚫ DEBUG - Gris
- ⚡ Actualización instantánea (SSE)
- 🎯 Máximo 100 logs en pantalla

### **3. Monitor Auto-Refresh** (`/monitor`)
**URL:** `http://localhost:8000/monitor`

**Funciones:**
- Auto-actualización cada 2 segundos
- Ideal para segunda pantalla
- Redirige automáticamente al formulario

---

## 🎨 Capturas de Pantalla

### **Formulario con Notificación de Éxito**
```
┌─────────────────────────────────────────┐
│  [Logo]                                 │
│                                         │
│  ✅ Evidencia agregada correctamente   │ ← Verde, animado
│                                         │
│  ID del Caso: [TC001_Login]            │
│  Descripción: [Login exitoso]          │
│  [Guardar Contexto]                    │
│                                         │
│  Contexto actual:                       │
│  ID de Prueba: TC001_Login             │
│  Paso: Login exitoso                   │
│                                         │
│  📊 Ver Logs ← Botón flotante         │
└─────────────────────────────────────────┘
```

### **Modal de Logs Abierto (Nuevo Diseño v1.1)**
```
┌─────── Formulario Principal ───────────────┐
│  [Logo]                                   │
│                                          │
│  ID del Caso: [TC001_Login]             │
│  Descripción: [Login exitoso]           │
│  [Guardar Contexto]                     │
│                                          │
│  Contexto actual:                        │
│  ID de Prueba: TC001_Login              │
│  Paso: Login exitoso                    │
│                                          │
│                      ┌─────────────────────────┐
│                      │ 📊 Logs del Sistema  [X] │
│                      ├─────────────────────────┤
│                      │ [14:30] INFO 📥 Rec... │
│                      │                         │
│                      │ [14:30] INFO ✅ Evid... │ ← Verde
│                      │                         │
│                      │ [14:30] INFO 📄 Docu... │
│                      │                         │
│                      │ [14:30] ERROR ❌ Doc...  │ ← Rojo
│  📊 Ver Logs ← Botón ├─────────────────────────┤
└────────────────────────── │ ● En vivo  [Limpiar] │
                           └─────────────────────────┘
             ↑
      Modal NO tapa el formulario!
      Puedes seguir trabajando normalmente
```

---

## 📖 Guías de Uso

### **Escenario 1: Trabajo Normal con ShareX**

```
1. Abre formulario: http://localhost:8000/set_context_form
2. Click en "📊 Ver Logs"
3. Configura Test ID y Paso
4. Toma screenshots con ShareX
5. Los logs aparecen automáticamente en el modal:
   - 📥 Recibiendo evidencia...
   - ✅ Evidencia agregada correctamente
   - 📄 Documento actualizado
   - 🖼️  Imagen guardada
6. Continúa trabajando, los logs siguen apareciendo
7. Cierra modal con Escape cuando termines
```

### **Escenario 2: Debugging de Errores**

```
1. Abre el documento Word por error
2. Modal de logs abierto
3. Intentas subir imagen con ShareX
4. Ves inmediatamente en el modal:
   ❌ PermissionError: Documento abierto...
5. Cierras el documento Word
6. Subes la imagen de nuevo
7. Ves en el modal:
   ✅ Evidencia agregada correctamente
8. ¡Problema resuelto en segundos!
```

### **Escenario 3: Múltiples Evidencias Rápidas**

```
1. Modal de logs abierto
2. Tomas 10 screenshots seguidos
3. Los logs aparecen en tiempo real:
   - Evidencia 1... ✅
   - Evidencia 2... ✅
   - Evidencia 3... ✅
   - ...
4. Puedes confirmar que TODAS se subieron correctamente
5. Sin necesidad de revisar carpetas o terminal
```

---

## 🔧 Endpoints API

### **Principales**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Redirect a formulario |
| GET | `/set_context_form` | Formulario principal |
| POST | `/set_context` | Guardar contexto |
| POST | `/evidences` | Subir imagen (ShareX) |
| GET | `/evidences/{testId}/docx` | Descargar documento |

### **Nuevos - Logs**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/logs/stream` | SSE stream de logs |
| GET | `/logs/recent` | Últimos 50 logs (JSON) |

### **Utilidad**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/monitor` | Monitor auto-refresh |
| GET | `/open_browser` | Redirect con mensaje |

---

## 🎯 Tecnologías Utilizadas

### **Backend**
- **FastAPI** - Framework web asíncrono
- **Python-docx** - Generación de documentos Word
- **Uvicorn** - Servidor ASGI
- **Server-Sent Events** - Streaming de logs

### **Frontend**
- **HTML5/CSS3** - Interfaz responsive
- **JavaScript vanilla** - Sin frameworks pesados
- **EventSource API** - Recepción de logs en tiempo real
- **Jinja2** - Templating

### **Integración**
- **ShareX** - Captura y upload de screenshots

---

## 📊 Comparación: Antes vs Ahora

| Característica | Antes | Ahora |
|----------------|-------|-------|
| Ver mensajes | ❌ Panel FastAPI | ✅ Navegador + Modal |
| Logs en tiempo real | ❌ Solo terminal | ✅ Modal interactivo |
| Notificaciones | ❌ Invisibles | ✅ Animadas y claras |
| Debugging | ⚠️ Complicado | ✅ Inmediato |
| Experiencia | ⚠️ Básica | ✅ Profesional |

---

## 🐛 Solución de Problemas Comunes

### **Problema 1: No veo mensajes de notificación**

**Causa:** Estás usando ShareX y no el navegador

**Solución:**
```
OPCIÓN A: Abre el navegador
  http://localhost:8000/set_context_form

OPCIÓN B: Abre el modal de logs
  Click en "📊 Ver Logs"
  
OPCIÓN C: Revisa logs del servidor
  En la terminal donde corre uvicorn
```

### **Problema 2: Modal de logs no se abre**

**Solución:**
```bash
# 1. Refresca el navegador
Ctrl + F5

# 2. Abre DevTools
F12 → Console → Busca errores

# 3. Reinicia el servidor
Ctrl + C
uvicorn app:app --reload

# 4. Limpia caché
Ctrl + Shift + Delete → Limpiar todo
```

### **Problema 3: "Error: Documento abierto"**

**Causa:** El archivo Word está abierto en Microsoft Word

**Solución:**
```
1. Cierra Microsoft Word
2. O cierra solo el documento de evidencias
3. Vuelve a subir la imagen
4. Verás ✅ en verde
```

### **Problema 4: Logs no aparecen en el modal**

**Checklist:**
```
□ ¿El servidor está corriendo?
□ ¿El modal está abierto?
□ ¿Hay actividad? (¿subiste una imagen?)
□ ¿El indicador "En vivo" está pulsando?
□ ¿La consola del navegador muestra errores?
```

**Solución:**
```bash
# Reiniciar todo
1. Cerrar modal
2. Ctrl + C en terminal
3. uvicorn app:app --reload
4. F5 en navegador
5. Abrir modal de nuevo
```

---

## 📚 Documentación Detallada

### **Archivos de Ayuda**

| Archivo | Descripción |
|---------|-------------|
| `COMO_VER_MENSAJES.md` | Guía para ver notificaciones |
| `MODAL_LOGS_GUIA.md` | Documentación completa del modal |
| `README.md` | Este archivo (resumen) |

### **Estructura del Proyecto**

```
QA-Evidence-Automator/
├── app.py                      ← FastAPI + Endpoints + SSE
├── requirements.txt            ← Dependencias
├── evidences/                  ← Carpeta de evidencias
│   └── {testId}/
│       ├── {testId}_evidence.docx
│       └── *.png
├── templates/
│   ├── base_template.docx      ← Plantilla Word
│   ├── set_context_form.html   ← Formulario + Modal
│   └── auto_refresh.html       ← Monitor
├── utils/
│   └── docx_builder.py         ← Lógica de Word
├── static/
│   ├── logo.png
│   └── favicon.ico
├── sharex/
│   └── QA_Evidence_API.sxcu    ← Configuración ShareX
├── COMO_VER_MENSAJES.md        ← Guía de notificaciones
├── MODAL_LOGS_GUIA.md          ← Guía del modal
└── README.md                   ← Este archivo
```

---

## 🚀 Próximas Mejoras

### **Corto Plazo (v1.1)**
- [ ] Filtros en modal de logs (por nivel)
- [ ] Búsqueda en logs
- [ ] Exportar logs a archivo .txt
- [ ] Copiar log al portapapeles
- [ ] Atajo de teclado `Ctrl+L` para abrir modal

### **Mediano Plazo (v1.2)**
- [ ] Resaltar palabras clave automáticamente
- [ ] Estadísticas de logs (total, errores, warnings)
- [ ] Gráfico de actividad por minuto
- [ ] Temas claro/oscuro/personalizado
- [ ] Notificaciones de escritorio de Windows

### **Largo Plazo (v2.0)**
- [ ] Múltiples sesiones simultáneas
- [ ] Base de datos para logs históricos
- [ ] Búsqueda avanzada en logs
- [ ] Integración con Slack/Discord/Teams
- [ ] Dashboard de estadísticas
- [ ] Autenticación y usuarios
- [ ] API REST completa

---

## 💡 Tips Profesionales

### **Tip 1: Usa Dos Monitores**
```
Monitor Principal:
  - Aplicación que estás probando
  - ShareX para screenshots

Monitor Secundario:
  - Navegador con formulario
  - Modal de logs abierto
  = Ver todo en tiempo real sin cambiar ventanas
```

### **Tip 2: Deja el Modal Abierto**
```
- Los logs no consumen muchos recursos
- Máximo 100 logs en memoria
- Se actualiza solo cuando hay actividad
- Puedes minimizar si molesta pero sigue funcionando
```

### **Tip 3: Organiza tus Tests**
```
Buena nomenclatura:
✅ TC001_Login
✅ TC002_CrearUsuario
✅ TC003_EliminarUsuario

Mala nomenclatura:
❌ test1
❌ prueba
❌ 123
```

### **Tip 4: Nombra Pasos Descriptivos**
```
Buenos nombres:
✅ "01 - Login con credenciales válidas"
✅ "02 - Verificar dashboard"
✅ "03 - Cerrar sesión exitoso"

Malos nombres:
❌ "paso1"
❌ "test"
❌ "screenshot"
```

### **Tip 5: Cierra Word Antes de Subir**
```
- El error más común es documento abierto
- Cierra Word o al menos el documento de evidencias
- O usa el modo "Solo lectura" en Word
- El modal te avisará inmediatamente si hay error
```

---

## 📊 Casos de Uso Reales

### **Caso 1: Testing de Aplicación Web**
```
Contexto: Probar flujo completo de login

1. Configura Test ID: "TC001_FlujLogin"
2. Abre modal de logs
3. Configura paso: "01 - Página de login"
4. Screenshot → Sube a ShareX
5. Cambia paso: "02 - Ingresar credenciales"
6. Screenshot → Sube a ShareX
7. Cambia paso: "03 - Dashboard exitoso"
8. Screenshot → Sube a ShareX
9. Descargas el Word con todas las evidencias
10. ¡Listo para reportar!
```

### **Caso 2: Testing de API con Postman**
```
Contexto: Probar endpoints REST

1. Test ID: "TC002_API_Usuarios"
2. Modal de logs abierto
3. Paso: "01 - GET /users"
4. Screenshot de Postman → ShareX
5. Paso: "02 - POST /users"
6. Screenshot de Postman → ShareX
7. Logs confirman que todo se guarda
8. Documento listo con evidencias
```

### **Caso 3: Testing Mobile**
```
Contexto: Probar app Android

1. Test ID: "TC003_AppMovil"
2. Emulador abierto
3. Modal de logs en segundo monitor
4. Paso: "01 - Splash screen"
5. Screenshot → ShareX
6. Paso: "02 - Onboarding"
7. Screenshot → ShareX
8. Ver en logs que todo se procesa
9. Documento generado automáticamente
```

---

## 🎓 Buenas Prácticas

### **Organización de Tests**
```
evidences/
├── TC001_Login/
│   ├── TC001_Login_evidence.docx
│   ├── 01_Pagina_login_20251027_143022_screenshot.png
│   ├── 02_Credenciales_20251027_143045_screenshot.png
│   └── 03_Dashboard_20251027_143102_screenshot.png
├── TC002_CrearUsuario/
│   ├── TC002_CrearUsuario_evidence.docx
│   └── ...
└── TC003_EliminarUsuario/
    ├── TC003_EliminarUsuario_evidence.docx
    └── ...
```

### **Nomenclatura de Pasos**
```
Formato recomendado:
[Número] - [Acción breve]

Ejemplos:
✅ "01 - Login exitoso"
✅ "02 - Crear usuario"
✅ "03 - Validar mensaje"

Evitar:
❌ Pasos muy largos
❌ Sin numeración
❌ Nombres genéricos
```

### **Flujo de Trabajo**
```
1. Planifica el test
2. Configura Test ID
3. Abre modal de logs
4. Para cada paso:
   a. Configura descripción del paso
   b. Ejecuta la acción
   c. Toma screenshot
   d. Verifica en logs que se guardó
5. Descarga documento final
6. Revisa que todas las imágenes están
7. ¡Entrega el documento!
```

---

## ✅ Checklist de Instalación

Antes de empezar, verifica que tienes todo:

### **Software Necesario**
- [x] Python 3.8+ instalado
- [x] Pip funcionando
- [x] Git instalado (opcional)
- [x] ShareX instalado
- [x] Microsoft Word (para ver documentos)

### **Configuración**
- [x] Servidor FastAPI corriendo
- [x] ShareX configurado con endpoint correcto
- [x] Navegador abierto en formulario
- [x] Modal de logs funcional

### **Pruebas**
- [x] Subir una imagen funciona
- [x] Documento Word se genera
- [x] Logs aparecen en modal
- [x] Notificaciones se ven
- [x] No hay errores en consola

---

## 🆘 Soporte y Ayuda

### **¿Necesitas ayuda?**

**Paso 1:** Revisa la documentación
- `README.md` (este archivo)
- `COMO_VER_MENSAJES.md`
- `MODAL_LOGS_GUIA.md`

**Paso 2:** Verifica logs
- Terminal del servidor (uvicorn)
- Modal de logs en navegador
- Console del navegador (F12)

**Paso 3:** Prueba soluciones comunes
- Reiniciar servidor
- Limpiar caché del navegador
- Cerrar documento Word
- Modo incógnito

**Paso 4:** Reporta el problema
```
Incluye:
- Versión de Python
- Sistema operativo
- Navegador y versión
- Logs del servidor (últimas 20 líneas)
- Logs de la consola del navegador
- Pasos para reproducir el error
```

---

## 🎉 ¡Listo para Usar!

### **Resumen de Funcionalidades**

✅ Subida automática de evidencias con ShareX  
✅ Generación automática de documentos Word  
✅ Organización por test y paso  
✅ Notificaciones visuales de éxito/error  
✅ **Modal de logs en tiempo real**  
✅ **Colores por nivel de log**  
✅ **Auto-scroll y actualización automática**  
✅ Monitor auto-refresh para segunda pantalla  
✅ Interfaz web moderna y responsive  

### **Próximos Pasos**

1. **Reinicia el servidor:**
   ```bash
   uvicorn app:app --reload
   ```

2. **Abre el navegador:**
   ```
   http://localhost:8000/set_context_form
   ```

3. **Click en "📊 Ver Logs"**

4. **¡Empieza a documentar tus tests!**

---

## 📝 Changelog

### **v1.1.0** (28 Octubre 2025) - Monitor de Logs Mejorado
- ✨ **Diseño no invasivo**: Modal aparece en esquina inferior derecha (450px × 600px)
- ✨ **Destacado automático**: Mensajes con emojis importantes resaltados visualmente
  - ✅ Éxito → Fondo verde brillante
  - ❌ Error → Fondo rojo brillante
  - ⚠️ Advertencia → Fondo rojo brillante
  - 🎯 🚀 📝 💾 ⏰ 🔍 → Destacado especial con sombra
- 🎨 Scrollbar personalizado con gradiente del tema
- 📱 Diseño responsive para móviles (<768px)
- ✨ Interfaz compacta y profesional
- 📄 Documentación completa en MEJORAS_MONITOR_LOGS.md

### **v1.0.1** (27 Octubre 2025)
- ✨ Agregado modal de logs en tiempo real
- ✨ Server-Sent Events para streaming
- ✨ Notificaciones animadas mejoradas
- ✨ Monitor auto-refresh
- 🐛 Corregido problema de caché
- 📚 Documentación completa agregada

### **v1.0.0** (Original)
- ✨ Subida de imágenes con ShareX
- ✨ Generación automática de Word
- ✨ Panel web de configuración
- ✨ Organización por test

---

## 📄 Licencia

[Tu licencia aquí]

---

## 👤 Autor

Pablo Murua
- Email: muruapablo@gmail.com
- Web: https://EvidenceAutomator.net

---

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- ShareX por la herramienta de captura
- python-docx por la manipulación de Word
- La comunidad de Python por todo el soporte

---

**¿Preguntas? ¿Sugerencias? ¿Problemas?**  
Revisa la documentación o abre un issue en el repositorio.

**¡Feliz Testing! 🚀**
