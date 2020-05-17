rm dawaiApp/migrations/*
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations dawaiApp
python3 manage.py migrate dawaiApp
python3 manage.py createsuperuser --username faisal --email test@test.com #--noinput
