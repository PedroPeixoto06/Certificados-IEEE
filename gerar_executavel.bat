@echo off
echo ========================================================
echo   Empacotando o Gerador de Certificados (PyInstaller)
echo ========================================================
echo.
echo Instalando dependencias...
python -m pip install -r requirements.txt
python -m pip install pyinstaller customtkinter
echo.
echo Compilando o executavel (isso pode levar alguns minutos)...
python -m PyInstaller --noconfirm --onefile --windowed --paths "src" --hidden-import "main" --add-data "src;src" --add-data "assets;assets" --add-data "data;data" --add-data "config.json;." app_gui.py
echo.
if exist "dist\app_gui.exe" (
    echo ========================================================
    echo   CONCLUIDO COM SUCESSO! 
    echo   O seu arquivo executavel "app_gui.exe" foi gerado e 
    echo   esta disponivel dentro da pasta "dist".
    echo ========================================================
) else (
    echo ========================================================
    echo   ERRO! O executavel nao foi encontrado.
    echo   Por favor, leia as mensagens de erro acima.
    echo ========================================================
)
pause
