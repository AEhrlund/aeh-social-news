python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt

python twitter_update.py
@REM python twitter_secrets.py

deactivate
