@echo off
cd /d "%~dp0"
echo Starting Car Price Predictor from:
cd
streamlit run car_price_api\app.py
pause
