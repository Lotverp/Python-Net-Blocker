Name "Python Net Blocker"
OutFile "PythonNetBlocker_Installer.exe"

InstallDir "$PROGRAMFILES\Python Net Blocker"

; Richiede i privilegi di amministratore (necessario per modificare le regole del firewall)
RequestExecutionLevel admin

; Sezione principale dell'installer
Section "Install"

    ; Crea la directory di installazione
    SetOutPath "$INSTDIR"

    ; Copia l'eseguibile e l'icona nella directory di installazione
    File ".\Net Blocker.exe"  ; Sostituisci con il percorso corretto del tuo eseguibile
    File ".\myicon.ico"  ; Sostituisci con il percorso corretto della tua icona

    ; Crea un collegamento nel menu Start
    CreateDirectory "$SMPROGRAMS\Python Net Blocker"
    CreateShortcut "$SMPROGRAMS\Python Net Blocker\Python Net Blocker.lnk" "$INSTDIR\Net Blocker.exe" "" "$INSTDIR\myicon.ico"

    ; Crea un collegamento sul desktop (opzionale)
    CreateShortcut "$DESKTOP\Python Net Blocker.lnk" "$INSTDIR\Net Blocker.exe" "" "$INSTDIR\myicon.ico"

    ; Scrivi le informazioni di disinstallazione nel registro di sistema
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PythonNetBlocker" "DisplayName" "Python Net Blocker"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PythonNetBlocker" "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PythonNetBlocker" "DisplayIcon" '"$INSTDIR\myicon.ico"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PythonNetBlocker" "Publisher" "https://github.com/Lotverp/Python-Net-Blocker"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PythonNetBlocker" "DisplayVersion" "1.0.0"

SectionEnd

; Sezione di disinstallazione
Section "Uninstall"

    ; Rimuovi i file installati
    Delete "$INSTDIR\Net Blocker.exe"
    Delete "$INSTDIR\myicon.ico"
    Delete "$INSTDIR\Uninstall.exe"

    ; Rimuovi i collegamenti
    Delete "$SMPROGRAMS\Python Net Blocker\Python Net Blocker.lnk"
    Delete "$DESKTOP\Python Net Blocker.lnk"
    RMDir "$SMPROGRAMS\Python Net Blocker"

    ; Rimuovi la directory di installazione (se vuota)
    RMDir "$INSTDIR"

    ; Rimuovi le informazioni di disinstallazione dal registro di sistema
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PythonNetBlocker"

SectionEnd