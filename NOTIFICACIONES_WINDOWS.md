# 🔔 Notificaciones de Escritorio de Windows

## Descripción

El sistema ahora envía **notificaciones toast nativas de Windows 10/11** para informar sobre el estado de las operaciones.

## Características

### ✅ Notificación de Éxito
- Se muestra cuando una imagen se agrega correctamente al documento
- Duración: 3 segundos
- Incluye el nombre del paso y archivo

### ❌ Notificación de Error - Documento Bloqueado
- Se muestra cuando el documento `.docx` está abierto
- Duración: 7 segundos
- Indica que debe cerrar el documento

### ❌ Notificación de Error Inesperado
- Se muestra ante cualquier otro error
- Duración: 7 segundos
- Muestra los primeros 100 caracteres del error

## Instalación

1. Instalar la nueva dependencia:
```bash
cd C:\Proyectos\QA-Evidence-Automator
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

### Usar Icono Personalizado (Opcional)

Puedes agregar un icono personalizado para las notificaciones:

1. Coloca un archivo `.ico` en `C:\Proyectos\QA-Evidence-Automator\static\logo.ico`

2. Modifica la función en `app.py`:
```python
icon_path = str(BASE_DIR / "static" / "logo.ico")
send_windows_notification(
    "Evidencia Agregada ✅",
    f"Paso: {step}\nArchivo: {file.filename}",
    duration=3,
    icon_path=icon_path
)
```

## Funcionamiento

Las notificaciones se envían automáticamente:

- **Al subir una imagen exitosamente** → Notificación verde ✅
- **Si el documento está abierto** → Notificación roja ❌
- **Si ocurre un error inesperado** → Notificación roja ❌

## Solución de Problemas

### Las notificaciones no aparecen

1. **Verificar configuración de Windows:**
   - `Configuración > Sistema > Notificaciones`
   - Asegúrate de que las notificaciones estén habilitadas

2. **Verificar que Python tenga permisos:**
   - Ejecuta la terminal como administrador si es necesario

3. **Verificar los logs:**
   - Las notificaciones aparecen en el monitor de logs con el icono 🔔

### Error al instalar win10toast

Si `pip install win10toast` falla, intenta:

```bash
pip install --upgrade pip
pip install win10toast==0.9
```

## Personalización

### Cambiar duración de notificaciones

En `app.py`, modifica el parámetro `duration`:

```python
send_windows_notification(
    "Título",
    "Mensaje",
    duration=10  # 10 segundos
)
```

### Deshabilitar notificaciones

Comenta las llamadas a `send_windows_notification()` en el endpoint `/evidences`:

```python
# send_windows_notification(
#     "Evidencia Agregada ✅",
#     f"Paso: {step}\nArchivo: {file.filename}",
#     duration=3
# )
```

## Referencia Técnica

La función `send_windows_notification()` utiliza:

- **Librería:** `win10toast`
- **Modo:** `threaded=True` (no bloquea el servidor)
- **Compatibilidad:** Windows 10/11

### Parámetros de la función

```python
def send_windows_notification(
    title: str,           # Título de la notificación
    message: str,         # Mensaje a mostrar
    duration: int = 5,    # Duración en segundos
    icon_path: str = None # Ruta al icono (opcional)
)
```

## Logs

Todas las notificaciones generan un log con formato:

```
🔔 Notificación enviada: [Título] - [Mensaje]
```

En caso de error:

```
❌ Error al enviar notificación de Windows: [detalle del error]
```
