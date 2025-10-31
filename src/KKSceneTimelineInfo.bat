@echo off
set EXE_PATH="%~dp0bin\KKSceneTimelineInfo.exe"

if exist %EXE_PATH% (
    if "%~1"=="" (
        %EXE_PATH%
    ) else (
        %EXE_PATH% "%~1"
    )
) else (
    echo Error: KKSceneTimelineInfo.exe not found in /bin.
    pause
)