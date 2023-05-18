import googlemaps
import pandas as pd
import time


def search_nearby_places(keyword, location, radius):
    places_result = []
    next_page_token = None

    while True:
        search_results = gmaps.places_nearby(
            location=location, radius=radius, keyword=keyword, language='zh-TW', page_token=next_page_token)
        places_result.extend(search_results['results'])

        next_page_token = search_results.get('next_page_token', None)
        if next_page_token is None:
            break

        time.sleep(2)

    return places_result


def get_place_details(place_id):
    try:
        details_result = gmaps.place(place_id, language='zh-TW', fields=['name', 'rating', 'user_ratings_total', 'type','formatted_address', 'formatted_phone_number', 'geometry', 'photos', 'opening_hours'])

        result = {
            'place_id': place_id,
            'name': details_result['result'].get('name', None),
            'rating': details_result['result'].get('rating', None),
            'user_ratings_total': details_result['result'].get('user_ratings_total', None),
            'type': details_result['result'].get('type', None),
            'formatted_address': details_result['result'].get('formatted_address', None),
            'formatted_phone_number': details_result['result'].get('formatted_phone_number', None),
            'geometry.location': details_result['result'].get('geometry.location', None),
            'photos': details_result['result'].get('photos', None),
            'opening_hours': details_result['result'].get('opening_hours', None),
        }

        return result
    except Exception as e:
        print(f"Error fetching details for place_id: {place_id}. Error: {str(e)}")
        return None

gmaps = googlemaps.Client(key='AIzaSyCwGI7BGNrDL_AtaZNvS9jHWweUj1IJsT0')

cities = ["臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市", "基隆市", "新竹市", "嘉義市", "新竹縣","苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "金門縣", "澎湖縣", "連江縣"]

all_places = []

for city in cities:
    print(f"正在擷取 {city} 的資訊...")
    geocode_result = gmaps.geocode(city, language='zh-TW')
    loc = geocode_result[0]['geometry']['location']

    city_places = []
    radii = [5000, 10000, 15000, 20000, 25000]
    for radius in radii:
        places = search_nearby_places(
            keyword="寵物友善", location=loc, radius=radius)
        city_places.extend(places)

    all_places.extend(city_places)

unique_place_ids = {place['place_id'] for place in all_places}
unique_places = [place for place in all_places if place['place_id'] in unique_place_ids]

places_details = []
for place in unique_places:
    place_details = get_place_details(place['place_id'])
    places_details.append(place_details)

places_df = pd.DataFrame(places_details)

places_df.to_csv('pet_friendly_places.csv', index=False, encoding='utf_8_sig')
print("資料已成功儲存至 pet_friendly_places.csv")
