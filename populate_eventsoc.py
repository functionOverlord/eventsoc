import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad_project.settings')

django.setup()
from eventsoc.models import Category, Event, UserProfile


def populate():

    # Dictionary for societies
    societies = {"simmy": {"society_name": "University of Glasgow Twin Peaks Society", 
                "email": "kaka5@gmail.com", 
                "password": "begemotas5", 
                "social_media_website": "https://welcometotwinpeaks.com/"},

                "kenko5": {"society_name": "University of Glasgow Consulting Society", 
                "email": "consultingsoc@gmail.com", 
                "password": "persimonas092",
                "social_media_website": "https://consultinggu.com/"},

                "winesoc5": {"society_name": "University of Glasgow Wine Society", 
                "email": "wineforu@gmail.com", 
                "password": "iberica5664",
                "social_media_website": "https://guwine.com/"},

                "photou7": {"society_name": "University of Glasgow Photography Society", 
                "email": "guphoto5@gmail.com", 
                "password": "kangohj654p",
                "social_media_website": "https://www.facebook.com/guphotosoc/"},

                "sportsgu1": {"society_name": "University of Glasgow Sports Society", 
                "email": "gusport@gmail.com", 
                "password": "menhpolozik54",
                "social_media_website": "https://www.facebook.com/gusapresident/"},

                "densoc": {"society_name": "University of Glasgow Danish Society", 
                "email": "dangu@gmail.com", 
                "password": "kamnpas9871",
                "social_media_website": "https://www.facebook.com/danishsocgu/"},

                "guts": {"society_name": "University of Glasgow Tech Society", 
                "email": "guts43@gmail.com", 
                "password": "hgpotkambaryje6",
                "social_media_website": "https://www.facebook.com/guts/"}
    }

    # Dictionary with details for the admin user
    admin_user = {"username":"admin", 
                "password": "admin", "email":"admin@gmail.com"}


    # The code below goes through the societies dictionary and add's
    # an account for society in the database
    for soc, soc_data in societies.items():
        s = add_society(
                soc, 
                societies[soc]["society_name"], 
                societies[soc]["email"],
                societies[soc]["password"], 
                societies[soc]["social_media_website"])

    a = add_admin(admin_user["username"], admin_user["password"], admin_user["email"])


    # Create lists of dictionaries containing the events we want
    # to add to each category.
    tech_events = [{"title": "Python Workshop",
                    "date": "2019-04-05",
                    "time": "17:00:00",
                    "room": "407",
                    "address": "Boyd Orr",
                    "price": 0,
                    "description": "Learn how to code!",
                    "capacity": 50,
                    "picture": "events/python.jpg",
                    "creator": UserProfile.objects.get(society_name="University of Glasgow Tech Society")}
    ]

    sports_health_events = [{"title": "Volleyball Competition",
                             "date": "2019-05-12 15:00:00",
                             "room": "200",
                             "address": "Sports Centre",
                             "price": 5,
                             "description": "GU vs Strathclyde!",
                             "capacity": 200,
                             "picture": "events/volleyball.jpg",
                             "creator": UserProfile.objects.get(society_name="University of Glasgow Sports Society")},
                            {"title": "Yoga for Beginners",
                             "date": "2019-03-12 18:30:00",
                             "room": "Main hall",
                             "address": "Argyle St. 5",
                             "price": 3,
                             "description": "We're a yoga studio that likes to keep it real and experts at making you feel good.",
                             "capacity": 15,
                             "picture": "events/yoga.jpg",
                             "creator": UserProfile.objects.get(society_name="University of Glasgow Sports Society")}
    ]

    games_events = [{"title": "Monopoly Night",
                     "date": "2019-04-15 19:15:00",
                     "room": "407",
                     "address": "Joseph Black Building",
                     "price": 0,
                     "description": "Come and become the monopolist haha.",
                     "capacity": 16,
                     "picture": "events/monopoly.jpg",
                     "creator": UserProfile.objects.get(society_name="University of Glasgow Consulting Society")}
    ]

    art_events = [{"title": "Twin Peaks Painting Show",
                   "date": "2019-03-25 13:00:00",
                   "room": "Exibition Space 3",
                   "address": "Hunterian Museum",
                   "price": 0,
                   "description": "The Owls are not what they seem.",
                   "capacity": 40,
                   "picture": "events/twin.jpg",
                   "creator": UserProfile.objects.get(society_name="University of Glasgow Twin Peaks Society")},
                  {"title": "Bread in Daily Life. Photo Display.",
                   "date": "2019-03-28 15:00:00",
                   "room": "1st floor",
                   "address": "GU Library",
                   "price": 0,
                   "description": "I like bread and I took some photos of it.",
                   "capacity": 35,
                   "picture": "events/bread.png",
                   "creator": UserProfile.objects.get(society_name="University of Glasgow Photography Society")}
    ]

    media_films_events = [

    ]

    party_events = [{"title": "DJ J WILLY at HIVE",
                   "date": "2019-03-08 22:00:00",
                   "room": "Hive",
                   "address": "Where hive is?",
                   "price": 10,
                   "description": "This is going to be the best party in history. Maybe ever.",
                   "capacity": 150,
                   "picture": "events/hive.jpg",
                   "creator": UserProfile.objects.get(society_name="University of Glasgow Twin Peaks Society")}
    ]

    bussiness_economy_events = [

    ]

    educations_events = [

    ]

    food_drink_events = [{"title": "Wine and Cheese Tasting",
                   "date": "2019-05-05 18:30:00",
                   "room": "Drawing Room",
                   "address": "GUU",
                   "price": 5,
                   "description": "We're going to try some delicious wines from France and Italy acompanied by cheese.",
                   "capacity": 35,
                   "picture": "events/wine.jpg",
                   "creator": UserProfile.objects.get(society_name="University of Glasgow Wine Society")},
                   {"title": "Eat all you can Pancakes.",
                   "date": "2019-03-30 14:30:00",
                   "room": "QMU Hall",
                   "address": "QMU",
                   "price": 7,
                   "description": "The best fluffy american pancakes. Yummmmm.",
                   "capacity": 40,
                   "picture": "events/pancakes.jpg",
                   "creator": UserProfile.objects.get(society_name="University of Glasgow Danish Society")}
    ]

    music_dance_events = [

    ]

    talks_discussions_events = [{"title": "Talks on Geopolitics",
                   "date": "2019-04-20 17:00:00",
                   "room": "Hunter Hall",
                   "address": "Main Building",
                   "price": 0,
                   "description": "Fire, walk with me.",
                   "capacity": 300,
                   "picture": "events/talk.jpeg",
                   "creator": UserProfile.objects.get(society_name="University of Glasgow Consulting Society")}
    ]


    # Dictionary of dictonaries for our categories.
    cats = {"Technology": {"events": tech_events},
            "Sports and Health": {"events": sports_health_events},
            "Media and Films": {"events": media_films_events},
            "Party": {"events": party_events},
            "Art": {"events": art_events},
            "Business and Economy": {"events": bussiness_economy_events},
            "Education": {"events": educations_events},
            "Games": {"events": games_events},
            "Food and Drinks": {"events": food_drink_events},
            "Music and Dance": {"events": music_dance_events},
            "Talks and Discussions": {"events": talks_discussions_events}}


    # The code below goes through the cats dictionary, then adds each
    # category and then adds all the associated events for that category
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data["events"]:
            add_event(
                c,
                p["title"],
                p["date"],
                p["room"],
                p["address"],
                p["price"],
                p["description"],
                p["capacity"],
                p["picture"],
                p["creator"])
                
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Event.objects.filter(category=c):
            print("- {0}  -  {1}".format(str(c), str(p)))


def add_society(username, society_name, email, password, social_media_website):
    s = UserProfile.objects.get_or_create(username = username, password=password, email=email, 
    society_name=society_name, social_media_website=social_media_website, is_society=True)[0]
    s.save()
    return s


def add_admin(username, password, email):
    admin = UserProfile.objects.create_user(username=username, password=password, email=email)
    admin.is_superuser=True
    admin.is_staff=True
    admin.save()
    return admin


def add_event(
        cat,
        title,
        date,
        room,
        address,
        price,
        description,
        capacity,
        picture,
        creator):
    p = Event.objects.get_or_create(category=cat, title=title, creator=creator)[0]
    p.date = date
    p.room = room
    p.address = address
    p.price = price
    p.description = description
    p.capacity = capacity
    p.picture = picture
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
