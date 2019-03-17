import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_project.settings')

import django 
django.setup()
from eventsoc.models import Category, Event

def populate():
    # Create lists of dictionaries containing the events we want
    # to add to each category.
    tech_events = [
        {"title": "Python Workshop", "date": "2019-04-05", "time": "17:00:00",
        "room": "407", "address": "Boyd Orr", "price": 0, "description": "Learn how to code!", "capacity": 50}
    ]

    sports_health_events = [
        {"title": "Volleyball Competition", "date": "2019-05-12 15:00:00", "room": "200", 
        "address": "Sports Centre", "price": 5, "description": "GU vs Strathclyde!", "capacity": 200},
        {"title": "Yoga for Beginners", "date": "2019-03-12 18:30:00", "room": "Main hall", 
        "address": "Argyle St. 5", "price": 3, "description": "We're a yoga studio that likes to keep it real and experts at making you feel good.",
        "capacity": 15}
    ]

    games_events = [
         {"title": "Monopoly Night", "date": "2019-04-15 19:15:00", "room": "407", 
         "address": "Joseph Black Building", "price": 0, "description": "Come and become the monopolist haha.",
         "capacity": 16}
    ]

    art_events = [
        {"title": "Twin Peaks Painting Show", "date": "2019-03-25 13:00:00", "room": "Exibition Space 3", 
        "address": "Hunterian Museum", "price": 0, "description": "The Owls are not what they seem.",
        "capacity": 40},
        {"title": "Bread in Daily Life. Photo Display.", "date": "2019-03-28 15:00:00", "room": "1st floor", 
        "address": "GU Library", "price": 0, "description": "I like bread and I took some photos of it.",
        "capacity": 35}
    ]

    media_films_events = [

    ]

    party_events = [

    ]

    bussiness_economy_events = [

    ]

    educations_events = [

    ]

    food_drink_events = [

    ]

    music_dance_events = [

    ]

    talks_discussions_events = [

    ]

    # Dictionary of dictonaries for our categories.
    cats = {"Technology": {"events": tech_events},
            "Sports and Health": {"events": sports_health_events},
            "Media and Films": {"events": media_films_events},
            "Party": {"events": party_events},
            "Art": {"events": art_events},
            "Bussines and Economy": {"events": bussiness_economy_events},
            "Education": {"events": educations_events},
            "Games": {"events": games_events},
            "Food and Drinks": {"events": food_drink_events},
            "Music and Dance": {"events": music_dance_events},
            "Talks and Discussions": {"events": talks_discussions_events}}

    # The code below goes through the cats dictionary, then adds each
    # category and then adds all the associated events for that category.

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data["events"]:
            add_event(c, p["title"], p["date"], p["room"],
            p["address"], p["price"], p["description"], p["capacity"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Event.objects.filter(category=c):
            print("- {0}  -  {1}".format(str(c), str(p)))

def add_event(cat, title, date, room, address, price, description, capacity):
    p = Event.objects.get_or_create(category=cat, title=title)[0]
    p.date=date
    p.room=room
    p.address=address
    p.price=price
    p.description=description
    p.capacity=capacity
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# Start execution here.
if __name__ == '__main__':
    print('Starting EventSoc population script...')
    populate()