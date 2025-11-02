@echo off
cd /d C:\Proyectos\QA-Evidence-Automator

echo ================================
echo   Git Status
echo ================================
git status

echo.
echo ================================
echo   Adding changes...
echo ================================
git add .

echo.
echo ================================
echo   Committing changes...
echo ================================
git commit -m "feat: Optimized document generation with proper table merges and content order

- Fixed table, text, and image ordering (Table -> Text -> Image sequence)
- Implemented proper cell merging for tables to maintain template structure
- Added permission error handling with Windows notifications
- Optimized performance by removing debug logs
- Reduced memory usage and CPU overhead
- Improved error handling for locked documents
- Clean code implementation using python-docx methods only"

echo.
echo ================================
echo   Current Git Tags
echo ================================
git tag

echo.
echo ================================
echo   What version do you want? (e.g., v1.1.0)
echo ================================
set /p VERSION="Enter version number: "

echo.
echo ================================
echo   Creating tag %VERSION%...
echo ================================
git tag -a %VERSION% -m "Release %VERSION%: Optimized document generation with proper formatting"

echo.
echo ================================
echo   Pushing to GitHub...
echo ================================
git push origin main
git push origin %VERSION%

echo.
echo ================================
echo   Done! Now go to GitHub to create the release:
echo   https://github.com/muruapablo/QA-Evidence-Automator/releases/new
echo   Select tag: %VERSION%
echo ================================
pause
