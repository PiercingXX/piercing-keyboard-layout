# PiercingXX layout — Windows installer helper. Run as Administrator.
# 1) Applies the scancode remaps (Caps->Backspace, Backspace->Delete)
# 2) Installs the AltGr-arrows AutoHotkey script to Startup (if AHK v2 found)
# The layout itself must be built once from piercing.klc with MSKLC 1.4
# (Project -> Build DLL and Setup Package -> run setup.exe) — MSKLC output
# cannot be automated from a script.

#Requires -RunAsAdministrator
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Applying scancode remaps (Caps->Backspace, Backspace->Delete)..."
reg import "$here\scancode-remap.reg"
Write-Host "  done — takes effect after sign-out/reboot."

$ahk = Get-Command "AutoHotkey64.exe","AutoHotkey.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($ahk) {
    $startup = [Environment]::GetFolderPath("Startup")
    $ws = New-Object -ComObject WScript.Shell
    $lnk = $ws.CreateShortcut("$startup\piercing-altgr-arrows.lnk")
    $lnk.TargetPath = $ahk.Source
    $lnk.Arguments  = "`"$here\altgr-arrows.ahk`""
    $lnk.Save()
    Start-Process $ahk.Source -ArgumentList "`"$here\altgr-arrows.ahk`""
    Write-Host "AltGr-arrows script installed to Startup and started."
} else {
    Write-Host "AutoHotkey v2 not found — install it from https://www.autohotkey.com"
    Write-Host "then put a shortcut to altgr-arrows.ahk in shell:startup."
}

Write-Host ""
Write-Host "Remaining manual step: build piercing.klc with MSKLC 1.4 and run"
Write-Host "its setup.exe, then pick 'English (Piercing)' in language settings."
