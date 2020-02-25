from geopy.geocoders import Nominatim
import tweepy
import folium
from config import twitter_api


def get_coordinates(location):
    '''
    str->(float,float)
    Return latitude and longitude by location
    '''
    geolocator = Nominatim(user_agent="program", timeout=2)

    location_coordinates = geolocator.geocode(location)
    lat2, lng2 = location_coordinates.latitude, location_coordinates.longitude
    return lat2, lng2


CONSUMER_KEY = twitter_api['CONSUMER_KEY']
CONSUMER_SECRET = twitter_api['CONSUMER_SECRET']
ACCESS_TOKEN = twitter_api['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = twitter_api['ACCESS_TOKEN_SECRET']


def get_friends(screen_name):
    '''
    str->list
    Return list of friends and their coordinates
    '''
    auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    users = tweepy.Cursor(api.friends, screen_name=screen_name).items()
    friends = []
    for user in users:
        print(user.screen_name, user.location)
        for i in range(3):
            try:
                location = get_coordinates(user.location)
                print('HERE')
                friends.append([user.screen_name, location])
                break
            except:
                pass
    print(friends)
    return friends


def create_map(screen_name):
    '''
    str -> html
    Create and return html file with map and user friends
    '''
    if screen_name[0] != '@':
        screen_name = '@' + screen_name
    try:
        friends = get_friends(screen_name)
    except:
        return 'Invalid user'
    friendstart = 0
    layer2 = folium.FeatureGroup(name="Friends map")
    locations = {}
    for friend in friends:
        if friendstart == 0:
            friendstart = friend

        lt, ln = friend[1][0], friend[1][1]
        locations[(lt,ln)] = locations.get((lt,ln),[])
        locations[(lt, ln)].append(friend[0])
        layer2.add_child(folium.Marker(location=[lt, ln],
                                       popup=','.join(locations[(lt,ln)]),
                                       icon=folium.Icon()))
    m = folium.Map(location=[friendstart[1][0], friendstart[1][1]], zoom_start=10)
    m.add_child(layer2)

    return m._repr_html_()
