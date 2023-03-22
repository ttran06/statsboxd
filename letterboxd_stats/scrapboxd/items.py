# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def get_rating(text) -> None:
    # have to divide by 2 because scale is 10
    rating = float(text.split()[0])

    return rating


def filter_casts(text) -> None:
    # "Show All…"
    return None if "Show All" in text else text


def make_float(x) -> float:
    return float(x)


def clean_url(url):
    return url.replace(self.username, "")


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=TakeFirst())
    director = scrapy.Field()
    actors = scrapy.Field(input_processor=MapCompose(filter_casts))
    actors_link = scrapy.Field()
    crew = scrapy.Field()
    genres = scrapy.Field()
    rating = scrapy.Field(
        input_processor=MapCompose(get_rating, make_float), output_processor=TakeFirst()
    )
    country = scrapy.Field()
    production_company = scrapy.Field()
    release_year = scrapy.Field(
        input_process=MapCompose(int), output_processor=TakeFirst()
    )
    watched_on = scrapy.Field()
    user_rating = scrapy.Field()
    url = scrapy.Field()


class Movies2(scrapy.Item):
    director = scrapy.Field()
