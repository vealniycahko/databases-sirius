import psycopg2

from typing import List
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(database='', user='', password='', host='localhost', port=5432,
                        cursor_factory=RealDictCursor)


class Tour:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        self.cities: List[City] = []
        self.reviews: List[Review] = []

class City:
    def __init__(self, name: str, founded: str):
        self.name = name
        self.founded = founded
        self.tours: List[Tour] = []

class Review:
    def __init__(self, id: int, comment: str, ratio: int):
        self.id = id
        self.comment = comment
        self.ratio = ratio
        self.tour: None


cur = conn.cursor()

query = """
select tour_name, price, city_name, founded, id, comment, ratio
from tour
   join city_to_tour on tour.name = city_to_tour.tour_name
   join city on city.name = city_to_tour.city_name
   left join review on tour.name = review.tourname;
"""

cur.execute(query)
rows = cur.fetchall()

tours_dict = {}
cities_dict = {}
reviews_dict = {}

for row in rows:
    tour_name = row['tour_name']
    tour_price = row['price']

    tour = None
    if tour_name in tours_dict:
        tour = tours_dict[tour_name]
    else: # проверка tour_name на null не нужна, tour_name всегда != null
        tour = Tour(tour_name, tour_price)
        tours_dict[tour_name] = tour

    city_name = row['city_name']
    city_founded = row['founded']

    city = None
    if city_name in cities_dict:
        city = cities_dict[city_name]
    elif city_name is not None:
        city = City(city_name, city_founded)
        cities_dict[city_name] = city

    review_id = row['id']
    review_comment = row['comment']
    review_ratio = row['ratio']

    review = None
    if review_id in reviews_dict:
        review = reviews_dict[review_id]
    elif review_id is not None:
        review = Review(review_id, review_comment, review_ratio)
        reviews_dict[review_id] = review

    # отношения tour - city
    if city_name is not None:
        if city not in tour.cities: tour.cities.append(city)
        if tour not in city.tours: city.tours.append(tour)

    # отношения tour - review
    if review is not None:
        if review not in tour.reviews: tour.reviews.append(review)
        review.tour = tour


tours = list(tours_dict.values())
cities = list(cities_dict.values())
reviews = list(reviews_dict.values())

conn.close()
