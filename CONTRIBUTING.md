# Contribuir a QA Evidence Automator

¡Gracias por tu interés en contribuir! 🎉

## 🚀 Cómo Contribuir

### Reportar Bugs

Si encuentras un bug, por favor abre un [Issue](https://github.com/muruapablo/QA-Evidence-Automator/issues) con:
- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs. actual
- Screenshots si es aplicable
- Información del entorno (OS, versión de Python, etc.)

### Sugerir Mejoras

Para sugerir nuevas características:
1. Abre un Issue con la etiqueta "enhancement"
2. Describe claramente la funcionalidad propuesta
3. Explica por qué sería útil para el proyecto

### Pull Requests

1. **Fork** el repositorio
2. **Crea una rama** desde `main`:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Realiza tus cambios** siguiendo las guías de estilo
4. **Commit** con mensajes descriptivos:
   ```bash
   git commit -m "Add: nueva funcionalidad X"
   ```
5. **Push** a tu fork:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
6. **Abre un Pull Request** con descripción detallada

## 📝 Guías de Estilo

### Python
- Seguir [PEP 8](https://pep8.org/)
- Usar type hints cuando sea posible
- Documentar funciones con docstrings
- Nombres de variables descriptivos

### Commits
Usar prefijos:
- `Add:` nueva funcionalidad
- `Fix:` corrección de bug
- `Update:` actualización de código existente
- `Docs:` cambios en documentación
- `Refactor:` refactorización sin cambio de funcionalidad

### Código
```python
# Bien ✓
def add_image_to_docx(docx_path: str, image_path: str, template_path: str, step_desc: str = "") -> None:
    """
    Agrega una imagen al documento DOCX.
    
    Args:
        docx_path: Ruta del documento de destino
        image_path: Ruta de la imagen a insertar
        template_path: Ruta de la plantilla base
        step_desc: Descripción del paso (opcional)
    """
    pass

# Evitar ✗
def add_img(d, i, t, s=""):
    pass
```

## 🧪 Testing

Antes de enviar un PR, asegúrate de que:
- El código funciona correctamente
- No hay errores de sintaxis
- Las dependencias están actualizadas en `requirements.txt`

## 📚 Documentación

Al agregar nuevas funcionalidades:
- Actualizar el README.md
- Agregar docstrings a nuevas funciones
- Documentar nuevos endpoints en la API

## ❓ Preguntas

Si tienes dudas, abre un Issue con la etiqueta "question" o contacta a:
- Email: muruapablo@gmail.com

¡Gracias por contribuir! 🙌
