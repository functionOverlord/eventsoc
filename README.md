# Web Application Development - Team B

EventSoc is an online listing of events held at the University of Glasgow. 
It's a place where students can easily navigate upcoming events.

Our application also accommodates the needs of societies that wish to advertise 
their events and gauge interest of students.

## Running the project
Create a virtual environment, for example:
```
python -m venv . 
source bin/activate
```

Followed by:
```
git clone https://github.com/functionOverlord/eventsoc.git
cd eventsoc

pip install -r requirements.txt
```

##### Start server
On Linux
```
./clean_database.sh
```

On Windows:
```
python manage.py makemigrations eventsoc
python manage.py migrate

python populate_eventsoc.py

python manage.py runserver
```

## External resources
- JQuery
- Bootstrap

