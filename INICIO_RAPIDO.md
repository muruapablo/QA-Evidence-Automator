# 🚀 INICIO RÁPIDO - 5 MINUTOS

## ⚡ Instalación Express

```bash
# 1. Clonar (o ya lo tienes)
cd C:\Proyectos\QA-Evidence-Automator

# 2. Activar entorno virtual
venv\Scripts\activate

# 3. Iniciar servidor
uvicorn app:app --reload
```

## 🌐 Abrir Aplicación

```
http://localhost:8000/set_context_form
```

## 📊 Usar Modal de Logs

1. Click en botón flotante **"📊 Ver Logs en Tiempo Real"** (abajo a la derecha)
2. Deja el modal abierto
3. Sube imágenes con ShareX
4. **¡Los logs aparecen automáticamente!**

---

## ✅ Verificación Rápida

### ¿Todo funciona?

```bash
✅ Servidor corriendo en http://localhost:8000
✅ Página carga correctamente
✅ Botón flotante visible
✅ Modal se abre con click
✅ Indicador "En vivo" pulsando
```

### ¿Hay problemas?

```bash
# Reiniciar todo
Ctrl + C
uvicorn app:app --reload
# Navegar a: http://localhost:8000/set_context_form
# F5 para refrescar
# Click en "Ver Logs"
```

---

## 🎯 Primer Test

```
1. Configura:
   Test ID: TC001_Prueba
   Paso: 01 - Screenshot inicial

2. Abre modal de logs

3. Toma un screenshot con ShareX

4. Verás en el modal:
   📥 Recibiendo evidencia...
   ✅ Evidencia agregada correctamente
   📄 Documento: ...
   🖼️  Imagen: ...

5. ¡Listo! Tu primer test documentado
```

---

## 📚 Más Información

- **Guía completa:** `README.md`
- **Modal de logs:** `MODAL_LOGS_GUIA.md`
- **Notificaciones:** `COMO_VER_MENSAJES.md`

---

## 🆘 Ayuda Rápida

**Modal no se abre:**
```bash
F12 → Console → Buscar errores
Ctrl + F5 → Refrescar sin caché
```

**Logs no aparecen:**
```bash
Verifica que el servidor esté corriendo
Sube una imagen para generar actividad
El indicador "En vivo" debe pulsar
```

**Error "Documento abierto":**
```bash
Cierra Microsoft Word
O cierra el documento específico
Vuelve a subir la imagen
```

---

## 🎉 ¡Eso es todo!

Ahora tienes:
- ✅ Logs en tiempo real
- ✅ Notificaciones visuales
- ✅ Documentación automática
- ✅ Todo en un solo lugar

**¡Feliz Testing!** 🚀
