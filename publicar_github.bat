@echo off
echo ========================================
echo  Publicar Mejoras en GitHub
echo ========================================
echo.

cd /d "%~dp0"

echo [1/6] Verificando estado del repositorio...
git status
echo.

echo [2/6] Agregando archivos modificados...
git add templates/set_context_form.html
git add MEJORAS_MONITOR_LOGS.md
git add README.md
echo - templates/set_context_form.html
echo - MEJORAS_MONITOR_LOGS.md
echo - README.md
echo.

echo [3/6] Creando commit...
git commit -m "✨ Mejora el monitor de logs: diseño no invasivo y destacado de mensajes importantes" -m "" -m "Cambios principales:" -m "- Monitor aparece en esquina inferior derecha (450px × 600px max)" -m "- No tapa el formulario set_context_form" -m "- Mensajes con emojis importantes se destacan automáticamente:" -m "  • ✅ Éxito (fondo verde)" -m "  • ❌ Error (fondo rojo)" -m "  • ⚠️ Advertencia (fondo rojo)" -m "  • 🎯 🚀 📝 💾 ⏰ 🔍 (destacado especial)" -m "- Diseño compacto tipo chat flotante" -m "- Scrollbar personalizado con gradiente del tema" -m "- Responsive para móviles (<768px)" -m "- Animación slideInRight mejorada" -m "- Documentación completa agregada" -m "" -m "Archivos modificados:" -m "- templates/set_context_form.html" -m "- MEJORAS_MONITOR_LOGS.md (nuevo)" -m "- README.md (actualizado changelog)"
echo.

echo [4/6] Verificando commit...
git log -1 --oneline
echo.

echo [5/6] Subiendo cambios a GitHub...
git push origin main
echo.

echo [6/6] ¡Listo!
echo.
echo ========================================
echo  Cambios publicados exitosamente!
echo ========================================
echo.
echo Verifica en: https://github.com/muruapablo/QA-Evidence-Automator
echo.
pause
