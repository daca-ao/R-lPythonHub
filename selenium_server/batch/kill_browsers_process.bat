@echo off
rem   just kills stray local IE/chrome/firefox browser processes.

taskkill /im chrome.exe /t /f
taskkill /im firefox.exe /t /f