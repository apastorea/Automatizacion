# Publicación del proyecto en el repositorio existente de GitHub

**Repositorio verificado:** https://github.com/apastorea/Automatizacion

**Estado al 23 de noviembre de 2026:** vacío, rama predeterminada `main`, público y con permisos de escritura para la conexión GitHub actual.

## Paso 0 — Privacidad

El ZIP contiene informes, mediciones, metadatos de instrumentos y archivos académicos. Se recomienda configurar el repositorio como **Private** antes de publicarlos: GitHub > repositorio > Settings > General > Danger Zone > Change repository visibility > Make private.

## Paso 1 — Descargar y preparar

- Instalar Git for Windows (https://git-scm.com/downloads/win), si falta.
- Descargar `Automatizacion_Lab5_Lab7_para_GitHub.zip` desde el chat y guardarlo en Descargas de Windows.
- Abrir PowerShell.

## Paso 2 — Clonar el repositorio vacío y extraer el proyecto

```powershell
git --version
New-Item -ItemType Directory -Force -Path "$HOME\Documents\Proyectos" | Out-Null
Set-Location "$HOME\Documents\Proyectos"
git clone https://github.com/apastorea/Automatizacion.git
Set-Location Automatizacion
Expand-Archive -LiteralPath "$HOME\Downloads\Automatizacion_Lab5_Lab7_para_GitHub.zip" -DestinationPath (Get-Location).Path -Force
Get-ChildItem -Name
```

Se deberían observar `README.md`, `.gitignore`, `Laboratorio_5`, `Laboratorio_7` y `Herramientas_Comunes`. Si el ZIP fue descargado en otra carpeta, cambiar la ruta en el comando `Expand-Archive`.

**Importante:** el ZIP se extrae *dentro* de `Automatizacion`, no dentro de una subcarpeta adicional. El directorio `.git` que crea `git clone` debe permanecer intacto.

## Paso 3 — Primera publicación

```powershell
git status
git add .
git status
git commit -m "Incorporar antecedentes Lab5 y estructura inicial Lab7"
git push -u origin main
```

- Si Git solicita identidad para crear el commit, configurar una sola vez: `git config --global user.name "Tu nombre"` y `git config --global user.email "tu_correo_de_git"`. Usar la dirección asociada a GitHub o la dirección privada noreply si se prefiere.
- Si pide autenticación, iniciar sesión mediante navegador / Git Credential Manager. **Nunca compartir tokens o contraseñas en este chat.**
- Si falla `git push`, copiar aquí **el error sin credenciales** para diagnosticarlo.

## Paso 4 — Comprobación

Abrir https://github.com/apastorea/Automatizacion y recargar. Deben aparecer estas carpetas:

```text
Automatizacion/
├── README.md
├── .gitignore
├── GUIA_GITHUB_WINDOWS.md
├── Herramientas_Comunes/
├── Laboratorio_5/
└── Laboratorio_7/
    ├── 00_Enunciado/
    ├── 01_Modelado_MATLAB/
    ├── 02_Firmware_PSoC_5LP/
    ├── 03_Calibracion/
    ├── 04_Ensayos/
    ├── 05_Resultados/
    ├── 06_Informe_IEEE/
    └── 07_Registro_de_decisiones/
```

## Paso 5 — Actualizaciones posteriores

Trabajando en la carpeta `Automatizacion`:

```powershell
git pull --ff-only
git status
git add .
git commit -m "Describir el cambio realizado"
git push
```

No editar simultáneamente el mismo archivo desde la web y el PC sin hacer `git pull` antes. Examinar siempre `git status` y las calibraciones originales antes de agregar datos nuevos.

## LaTeX y PSoC

- `Laboratorio_7/06_Informe_IEEE/main.tex`: archivo maestro LaTeX para importar como proyecto Overleaf (subir ZIP con esta carpeta, no todos los datos de Lab5).
- `Laboratorio_5/PSoC_5LP/`: proyecto histórico PSoC Creator, referencia, no firmware seguro para aplicar directamente.
- `Laboratorio_7/02_Firmware_PSoC_5LP/`: núcleo C independiente del hardware, **todavía no integrado con PSoC Creator**.
