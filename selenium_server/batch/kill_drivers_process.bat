@echo off
rem   just kills stray local IE/chrome/firefox drivers instances.

taskkill /im chromedriver.exe /t /f
taskkill /im IEDriverServer.exe /t /f
taskkill /im geckodriver.exe /t /f