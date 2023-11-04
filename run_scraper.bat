@echo off
rem Ative seu ambiente virtual (por exemplo, "venv") se ainda não estiver ativado
call venv\Scripts\activate
rem Execute o web scraper
python web_scraper.py
rem Desative o ambiente virtual (opcional)
deactivate
