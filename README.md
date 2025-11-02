# QA Evidence Automator 🚀

Automatizador de evidencias para pruebas de QA que genera documentos Word profesionales con tablas, descripciones y capturas de pantalla organizadas.

## ✨ Características

- ✅ **Generación automática de documentos**: Crea documentos Word (.docx) con formato profesional
- 📊 **Tablas con formato**: Mantiene el formato exacto del template incluyendo celdas combinadas
- 🖼️ **Gestión de imágenes**: Agrega capturas de pantalla automáticamente en el orden correcto
- 📝 **Texto descriptivo**: Incluye descripciones personalizables para cada paso
- 🔔 **Notificaciones Windows**: Alertas visuales para cada acción
- ⚡ **Alto rendimiento**: Optimizado para uso mínimo de recursos
- 🔒 **Manejo de errores**: Detecta documentos abiertos y muestra notificaciones apropiadas

## 📋 Requisitos

- Python 3.8+
- Windows 10/11 (para notificaciones)

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/muruapablo/QA-Evidence-Automator.git
cd QA-Evidence-Automator
```

2. Crea y activa el entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🎯 Uso

1. Inicia el servidor:
```bash
uvicorn app:app --reload
```

2. Abre tu navegador en: `http://127.0.0.1:8000`

3. **Workflow básico**:
   - Define el ID del caso de prueba
   - Escribe la descripción del paso
   - Haz clic en "Guardar Contexto" (crea la tabla + texto descriptivo)
   - Toma una captura de pantalla
   - Repite para cada paso adicional

## 📁 Estructura del Proyecto

```
QA-Evidence-Automator/
├── app.py                 # Aplicación FastAPI principal
├── utils/
│   └── docx_builder.py   # Lógica de generación de documentos
├── templates/
│   ├── base_template.docx # Template base para documentos
│   └── *.html            # Templates HTML
├── static/               # Archivos estáticos (CSS, JS, iconos)
├── evidences/           # Documentos generados (auto-creado)
└── requirements.txt     # Dependencias Python
```

## 🔧 Configuración del Template

El archivo `templates/base_template.docx` define el formato de los documentos generados. Usa estos placeholders:

- `{{TEST_ID}}`: ID del caso de prueba
- `{{STEP_DESC}}`: Descripción del paso

## 📸 Captura de Pantalla

Las imágenes se agregan automáticamente con:
- Ancho: 5.5 pulgadas
- Alineación: Centrada
- Formato: PNG

## 🛠️ API Endpoints

### `POST /set_context`
Crea una nueva sección (tabla + texto descriptivo)
- **Params**: `testId`, `step`

### `POST /evidences`
Agrega una imagen al documento actual
- **Body**: `file` (multipart/form-data)

### `GET /evidences/{testId}/docx`
Descarga el documento generado

## ⚡ Optimizaciones

- Sin logs de debug innecesarios
- Uso eficiente de memoria
- Manipulación directa del DOM de Word
- Caché de regex precompilados
- Manejo óptimo de celdas combinadas

## 🐛 Manejo de Errores

El sistema detecta y notifica:
- ✅ Documentos bloqueados/abiertos
- ✅ Permisos insuficientes
- ✅ Archivos faltantes
- ✅ Errores de formato

## 📝 Formato del Documento Generado

```
Tabla 1 (con celdas combinadas)
  → Texto descriptivo 1
  → Imagen 1

Tabla 2 (con celdas combinadas)
  → Texto descriptivo 2
  → Imagen 2

...
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Pablo Murua**
- Email: muruapablo@gmail.com
- Website: [EvidenceAutomator.net](https://EvidenceAutomator.net)
- GitHub: [@muruapablo](https://github.com/muruapablo)

## 🙏 Agradecimientos

- [python-docx](https://python-docx.readthedocs.io/) - Manipulación de documentos Word
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [winotify](https://github.com/versa-syahptr/winotify) - Notificaciones Windows

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
