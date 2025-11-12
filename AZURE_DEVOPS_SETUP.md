# 🔵 Configuración de Integración con Azure DevOps

Esta guía te ayudará a configurar la integración con Azure DevOps para importar automáticamente Test Plans, Test Suites y Test Cases en el Automatizador de Evidencias QA.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Paso 1: Generar Personal Access Token (PAT)](#paso-1-generar-personal-access-token-pat)
- [Paso 2: Configurar Variables de Entorno](#paso-2-configurar-variables-de-entorno)
- [Paso 3: Instalar Dependencias](#paso-3-instalar-dependencias)
- [Paso 4: Verificar Conexión](#paso-4-verificar-conexión)
- [Uso de la Integración](#uso-de-la-integración)
- [Solución de Problemas](#solución-de-problemas)

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

1. ✅ Una cuenta de Azure DevOps con acceso a un proyecto
2. ✅ Permisos para crear Personal Access Tokens (PAT)
3. ✅ Test Plans, Test Suites y Test Cases creados en Azure DevOps
4. ✅ Python 3.8+ instalado
5. ✅ El proyecto QA-Evidence-Automator clonado localmente

---

## Paso 1: Generar Personal Access Token (PAT)

El Personal Access Token (PAT) es una clave de autenticación que permite a la aplicación acceder a la API de Azure DevOps de forma segura.

### 1.1 Acceder a la configuración de tokens

1. Inicia sesión en Azure DevOps: `https://dev.azure.com/{tu-organizacion}`
2. Haz clic en tu avatar (esquina superior derecha)
3. Selecciona **Personal access tokens**
4. O accede directamente a: `https://dev.azure.com/{tu-organizacion}/_usersSettings/tokens`

### 1.2 Crear un nuevo token

1. Haz clic en **+ New Token**
2. Completa los siguientes campos:

   | Campo | Valor |
   |-------|-------|
   | **Name** | `QA Evidence Automator` |
   | **Organization** | Selecciona tu organización |
   | **Expiration** | Configura la fecha de expiración (recomendado: 90 días) |
   | **Scopes** | Selecciona **Custom defined** |

3. Configura los permisos necesarios:

   | Scope | Permiso | Descripción |
   |-------|---------|-------------|
   | **Work Items** | `Read` | Para leer Test Cases (work items) |
   | **Test Management** | `Read` | Para leer Test Plans y Test Suites |

4. Haz clic en **Create**

### 1.3 Copiar el token

⚠️ **IMPORTANTE**: El token solo se mostrará una vez. Cópialo inmediatamente.

```
Ejemplo de PAT:
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Si pierdes el token, deberás crear uno nuevo.

---

## Paso 2: Configurar Variables de Entorno

### 2.1 Crear archivo .env

En la raíz del proyecto `QA-Evidence-Automator`, crea un archivo llamado `.env`:

```bash
# En Windows (CMD)
copy .env.example .env

# En Windows (PowerShell)
Copy-Item .env.example .env

# En Linux/Mac
cp .env.example .env
```

### 2.2 Editar archivo .env

Abre el archivo `.env` con tu editor de texto favorito y configura las siguientes variables:

```env
# ============================================
# CONFIGURACIÓN DE AZURE DEVOPS
# ============================================

# Habilitar integración con Azure DevOps
AZURE_DEVOPS_ENABLED=true

# Nombre de tu organización (aparece en la URL de Azure DevOps)
# Ejemplo: Si tu URL es https://dev.azure.com/MiEmpresa
# Entonces tu organización es: MiEmpresa
AZURE_DEVOPS_ORG=tu-organizacion

# Nombre del proyecto en Azure DevOps
# Ejemplo: ProyectoQA
AZURE_DEVOPS_PROJECT=tu-proyecto

# Personal Access Token generado en el Paso 1
AZURE_DEVOPS_PAT=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Versión de la API (opcional, por defecto es 7.1)
AZURE_DEVOPS_API_VERSION=7.1
```

### 2.3 Ejemplo de configuración

```env
# Ejemplo real (reemplaza con tus datos)
AZURE_DEVOPS_ENABLED=true
AZURE_DEVOPS_ORG=ContosoCompany
AZURE_DEVOPS_PROJECT=WebAppQA
AZURE_DEVOPS_PAT=abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx
AZURE_DEVOPS_API_VERSION=7.1
```

### 2.4 Verificar que .env está en .gitignore

⚠️ **IMPORTANTE**: Nunca subas el archivo `.env` a Git. Verifica que esté en `.gitignore`:

```bash
# Verificar en Windows (PowerShell)
Select-String -Path .gitignore -Pattern "\.env"

# Verificar en Linux/Mac
grep "\.env" .gitignore
```

Deberías ver:
```
.env
.env.local
```

---

## Paso 3: Instalar Dependencias

Instala las nuevas dependencias necesarias para la integración:

```bash
# Activar entorno virtual (si usas uno)
# En Windows:
.\venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

Las nuevas dependencias instaladas son:
- `python-dotenv==1.0.0` - Para cargar variables de entorno
- `requests==2.31.0` - Para hacer peticiones HTTP a la API de Azure DevOps

---

## Paso 4: Verificar Conexión

### 4.1 Iniciar la aplicación

```bash
# Iniciar servidor
python -m uvicorn app:app --reload

# O en Windows, usar el script:
iniciar_evidencias.bat
```

### 4.2 Probar conexión desde el navegador

1. Abre tu navegador en: `http://localhost:8000`
2. Verifica el botón de Azure DevOps:
   - ✅ Si está habilitado (azul): La conexión está OK
   - ❌ Si está deshabilitado (gris): Hay un error de configuración

### 4.3 Verificar manualmente el endpoint de status

Abre en tu navegador o usa curl:

```bash
# Desde el navegador:
http://localhost:8000/azure/status

# Desde curl (Windows PowerShell):
Invoke-RestMethod -Uri "http://localhost:8000/azure/status"

# Desde curl (Linux/Mac):
curl http://localhost:8000/azure/status
```

**Respuesta esperada (conexión exitosa):**
```json
{
  "enabled": true,
  "configured": true,
  "connected": true,
  "organization": "ContosoCompany",
  "project": "WebAppQA",
  "message": "Conectado correctamente"
}
```

**Posibles errores:**

| Mensaje | Causa | Solución |
|---------|-------|----------|
| `"enabled": false` | `AZURE_DEVOPS_ENABLED=false` en .env | Cambiar a `true` |
| `"configured": false` | Falta alguna variable en .env | Verificar ORG, PROJECT y PAT |
| `"connected": false` | Error de autenticación o red | Verificar PAT, organización y proyecto |

---

## Uso de la Integración

### Flujo de Importación de Test Cases

1. **Abrir la aplicación**: `http://localhost:8000`

2. **Hacer clic en "Cargar desde Azure DevOps"** (botón azul)

3. **Seleccionar Test Plan**:
   - Se cargarán todos los Test Plans del proyecto
   - Selecciona el plan que contiene tus casos de prueba

4. **Seleccionar Test Suite**:
   - Se cargarán todos los suites del plan seleccionado
   - Selecciona la suite correspondiente

5. **Seleccionar Test Case**:
   - Se cargarán todos los test cases de la suite
   - Selecciona el caso de prueba que deseas importar
   - Verás una vista previa con:
     - Título del test case
     - Descripción
     - Pasos de prueba
     - Estado y prioridad

6. **Importar**:
   - Haz clic en "Importar Test Case"
   - El sistema creará automáticamente:
     - ID del caso: `TC{id}_{titulo_sanitizado}`
     - Paso: "Caso_Completo"
     - Descripción: HTML con toda la información del caso
     - Documento Word con la información importada

7. **Capturar evidencias**:
   - Continúa con el flujo normal de captura de evidencias
   - El contexto ya está configurado con la información de Azure DevOps

### Modo Manual (sin Azure DevOps)

Si no quieres usar Azure DevOps, simplemente:
- Deja `AZURE_DEVOPS_ENABLED=false` en .env
- El botón azul estará deshabilitado
- Podrás seguir usando el modo manual normalmente

---

## Solución de Problemas

### Error: "Azure DevOps no configurado"

**Causa**: Faltan variables de entorno en `.env`

**Solución**:
```bash
# Verificar que el archivo .env existe
dir .env        # Windows
ls -la .env     # Linux/Mac

# Verificar que las variables están configuradas
type .env       # Windows
cat .env        # Linux/Mac
```

Asegúrate de que tengas:
- `AZURE_DEVOPS_ENABLED=true`
- `AZURE_DEVOPS_ORG=...`
- `AZURE_DEVOPS_PROJECT=...`
- `AZURE_DEVOPS_PAT=...`

---

### Error: "Error de conexión" o "401 Unauthorized"

**Causa**: Personal Access Token inválido o expirado

**Solución**:
1. Verifica que el PAT esté correctamente copiado en `.env`
2. Verifica que el PAT no haya expirado
3. Crea un nuevo PAT si es necesario
4. Asegúrate de que el PAT tenga los permisos correctos:
   - Work Items (Read)
   - Test Management (Read)

---

### Error: "No hay Test Plans disponibles"

**Causa**: El proyecto no tiene Test Plans o no tienes permisos

**Solución**:
1. Verifica que el nombre del proyecto en `.env` sea correcto
2. Verifica que existan Test Plans en Azure DevOps:
   - Ve a `https://dev.azure.com/{org}/{project}/_testPlans`
3. Verifica que tu cuenta tenga acceso al proyecto
4. Verifica que el PAT tenga permisos de Test Management (Read)

---

### Error: "Test case sin pasos definidos"

**Causa**: El test case en Azure DevOps no tiene pasos configurados

**Solución**:
1. Edita el test case en Azure DevOps
2. Agrega pasos de prueba:
   - Acción: Qué hacer
   - Resultado Esperado: Qué debería pasar
3. Guarda el test case
4. Recarga en la aplicación

---

### El botón de Azure DevOps no aparece

**Causa**: Posible error en la carga de JavaScript

**Solución**:
1. Abre la consola del navegador (F12)
2. Busca errores de JavaScript
3. Refresca la página (Ctrl + F5)
4. Verifica que el archivo `set_context_form.html` esté actualizado

---

### Error: "Cannot read property of undefined"

**Causa**: Respuesta inesperada de la API de Azure DevOps

**Solución**:
1. Verifica los logs del servidor:
   ```bash
   # Verás los logs en la consola donde iniciaste uvicorn
   ```
2. Verifica que la versión de la API sea compatible (7.1)
3. Verifica que los IDs de plan/suite/case existan

---

## Soporte y Documentación Adicional

### Recursos Oficiales de Azure DevOps

- [Azure DevOps REST API Reference](https://learn.microsoft.com/en-us/rest/api/azure/devops/)
- [Personal Access Tokens](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate)
- [Test Plans API](https://learn.microsoft.com/en-us/rest/api/azure/devops/testplan/)
- [Work Items API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/)

### Arquitectura de la Integración

```
QA-Evidence-Automator/
├── app.py                              # Endpoints de API y lógica principal
├── services/
│   └── azure_devops_service.py         # Cliente de Azure DevOps API
├── models/
│   └── test_case.py                    # Modelos de datos (TestCase, TestSuite, TestPlan)
├── templates/
│   └── set_context_form.html           # UI con modal de selección
├── .env                                # Configuración (NO COMMITEAR)
└── .env.example                        # Plantilla de configuración

Flujo de Datos:
1. Usuario abre modal en el navegador
2. JavaScript llama a /azure/test-plans
3. FastAPI (app.py) usa AzureDevOpsService
4. AzureDevOpsService hace request a Azure DevOps API
5. Respuesta se parsea con modelos (TestCase, etc.)
6. JSON se envía al navegador
7. Usuario selecciona test case
8. Se importa y se crea documento Word
```

### Logs y Debugging

Para habilitar logs detallados:

```env
# En .env
DEBUG_MODE=true
```

Los logs aparecerán en:
- Consola del servidor (donde corriste `uvicorn`)
- Consola del navegador (F12 → Console)
- Página de monitoreo: `http://localhost:8000/monitor`

---

## Preguntas Frecuentes (FAQ)

### ¿Puedo usar múltiples organizaciones de Azure DevOps?

No actualmente. La aplicación soporta una organización y un proyecto a la vez. Para cambiar de proyecto, modifica el archivo `.env` y reinicia el servidor.

### ¿Los test cases se sincronizan automáticamente?

No. La importación se hace manualmente cada vez que abres el modal. Si un test case cambia en Azure DevOps, deberás importarlo nuevamente.

### ¿Puedo desactivar Azure DevOps temporalmente?

Sí, simplemente cambia `AZURE_DEVOPS_ENABLED=false` en `.env` y reinicia el servidor. El botón desaparecerá y podrás seguir usando el modo manual.

### ¿Se pueden importar múltiples test cases a la vez?

No en la versión actual. Debes importar un test case a la vez. Esta funcionalidad podría agregarse en futuras versiones.

### ¿Qué pasa si el PAT expira?

El botón de Azure DevOps se deshabilitará automáticamente. Deberás generar un nuevo PAT y actualizarlo en `.env`.

---

## Volver a Versión Estable (Sin Azure DevOps)

Si deseas volver a la versión anterior sin integración de Azure DevOps:

```bash
# Ver tag de versión estable
git tag -l

# Volver a versión estable
git checkout v1.0-stable

# O simplemente deshabilitar Azure DevOps
# En .env:
AZURE_DEVOPS_ENABLED=false
```

---

**¿Necesitas ayuda?** Abre un issue en el repositorio del proyecto.

**Autor:** Pablo Murua
**Email:** muruapablo@gmail.com
**Versión:** 2.0.0 (con integración Azure DevOps)
