# 📸 QA Evidence Automator

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.13+-brightgreen.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.119.1-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> Automatiza la generación de documentos de evidencia de QA capturando capturas de pantalla con ShareX y enviándolas a un backend FastAPI.

## ✨ Características

- 🚀 **API REST** con FastAPI para recibir capturas de pantalla
- 📄 **Generación automática** de documentos Word con evidencias
- 🖼️ **Integración con ShareX** para captura instantánea
- 📁 **Organización automática** por casos de prueba
- ⏰ **Timestamps** en cada captura
- 🎨 **Plantillas personalizables** para documentos
- 💬 **Descripción de pasos** en cada evidencia

## 📋 Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Solución de Problemas](#solución-de-problemas)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

## 📁 Estructura del Proyecto

```
QA-Evidence-Automator/
│
├── app.py                           # API principal (FastAPI)
├── iniciar_evidencias.bat           # Script para iniciar la API
├── requirements.txt                 # Dependencias del proyecto
├── .gitignore                       # Archivos ignorados por Git
├── LICENSE                          # Licencia MIT
│
├── utils/
│   └── docx_builder.py              # Módulo para insertar imágenes en DOCX
│
├── templates/
│   └── base_template.docx           # Plantilla base para evidencias
│
├── evidences/                       # Carpeta de evidencias generadas
│   └── .gitkeep                     # Mantiene la carpeta en Git
│
└── sharex/
    ├── QA_Evidence_API.sxcu         # Uploader básico para ShareX
    └── QA_Evidence_API_Dinamico.sxcu# Uploader con inputs interactivos
```

## 🔧 Requisitos Previos

- **Python 3.13+** (o superior)
- **ShareX** (para Windows)
- **Git** (opcional, para clonar el repositorio)

## 📦 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/muruapablo/QA-Evidence-Automator.git
cd QA-Evidence-Automator
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
```

### 3. Activar Entorno Virtual

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### Configurar ShareX

1. **Abrir ShareX**
2. **Importar configuración:**
   - Ve a `Destinos` → `Configuración de uploader personalizado...`
   - Haz clic en `Importar` → `Desde archivo...`
   - Navega a `sharex/` y selecciona uno de los archivos `.sxcu`

3. **Seleccionar uploader:**
   - En `Destinos` → `Destino de carga` → `Uploader personalizado`
   - Elige `QA Evidence API` o `QA Evidence API (Dinámico)`

### Tipos de Uploaders

- **QA_Evidence_API.sxcu**: Uploader básico con valores fijos
- **QA_Evidence_API_Dinamico.sxcu**: Uploader con inputs interactivos para `testId` y `step`

## 🚀 Uso

### 1. Iniciar el Servidor

**Opción A - Usando el script .bat (Windows):**
```bash
# Haz doble clic en iniciar_evidencias.bat
```

**Opción B - Manualmente:**
```bash
# Activar entorno virtual primero
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

El servidor estará disponible en: `http://127.0.0.1:8000`

### 2. Capturar Evidencias

1. Realiza una captura de pantalla con ShareX (ej. `Shift + Print Screen`)
2. Si usas el uploader dinámico, ingresa:
   - **testId**: Identificador del caso de prueba (ej. `TC001_Login`)
   - **step**: Descripción del paso (ej. `Ingresar credenciales`)
3. La captura se enviará automáticamente a la API

### 3. Verificar Evidencias

Las evidencias se guardarán en:
```
evidences/
└── TC001_Login/
    ├── 20241024_143052_screenshot.png
    └── TC001_Login_evidence.docx
```

### 4. Descargar Documento

Accede a: `http://127.0.0.1:8000/evidences/TC001_Login/docx`

## 📚 API Endpoints

### POST `/evidences`

Recibe una captura de pantalla y la agrega al documento de evidencias.

**Parámetros (form-data):**
- `testId` (string, requerido): Identificador del caso de prueba
- `step` (string, opcional): Descripción del paso
- `file` (file, requerido): Archivo de imagen

**Respuesta:**
```json
{
  "message": "Evidencia agregada correctamente",
  "file_saved": "evidences/TC001_Login/20241024_143052_screenshot.png",
  "docx_path": "evidences/TC001_Login/TC001_Login_evidence.docx"
}
```

### GET `/evidences/{testId}/docx`

Descarga el documento de evidencias generado para un caso de prueba.

**Parámetros:**
- `testId` (path): Identificador del caso de prueba

**Respuesta:**
- Archivo DOCX descargable

### Documentación Interactiva

FastAPI genera documentación automática:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🧪 Probar con Postman

1. Crear una solicitud `POST` a `http://127.0.0.1:8000/evidences`
2. Configurar `Body` como `form-data`:
   - `testId`: `TC_POSTMAN_001`
   - `step`: `Prueba desde Postman`
   - `file`: Seleccionar una imagen
3. Enviar la solicitud

## ⚠️ Solución de Problemas

### La API no recibe capturas de ShareX

**Posibles causas:**
- Verificar que el servidor esté corriendo
- Confirmar que el uploader correcto está seleccionado en ShareX
- Revisar el historial de ShareX para ver errores
- Verificar firewall (puede bloquear conexiones locales)

### Error al instalar dependencias

**Solución:**
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt
```

### El documento DOCX no se genera

**Verificar:**
- Que existe `templates/base_template.docx`
- Que la carpeta `evidences/` tiene permisos de escritura
- Revisar logs en la consola del servidor

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Contacto

**Pablo Murua**
- Email: muruapablo@gmail.com
- Website: [EvidenceAutomator.net](https://EvidenceAutomator.net)
- GitHub: [@muruapablo](https://github.com/muruapablo)

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno y rápido
- [python-docx](https://python-docx.readthedocs.io/) - Manipulación de archivos Word
- [ShareX](https://getsharex.com/) - Herramienta de captura de pantalla

---

⭐️ Si este proyecto te fue útil, considera darle una estrella en GitHub!
