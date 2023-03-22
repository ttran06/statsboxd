import scrapy
from scrapy.loader import ItemLoader
from scrapboxd.items import MovieItem, Movies2


class MoviesSpider(scrapy.Spider):
    name = "movies"

    allowed_domains = ["letterboxd.com"]
    BASE_URL = "https://letterboxd.com"
    custom_settings = {"DEPTH_LIMIT": 1}

    def __init__(self, username="ttran06", *args, **kwargs) -> None:
        super(MoviesSpider, self).__init__(*args, **kwargs)
        self.username = username
        self.start_urls = [f"https://letterboxd.com/{self.username}/films/diary/"]
        # self.start_urls = ["file:///Users/tructran/Documents/statsboxd/test.html"]

    def parse(self, response):
        for movie in response.css("tr.diary-entry-row"):
            movie_loader = ItemLoader(item=MovieItem(), response=response)
            dir_loader = ItemLoader(item=Movies2(), response=response)

            # movie_url = movie.css('h3.headline-3 a::attr("href")').get()
            movie_loader.add_css("url", 'h3.headline-3 a::attr("href")').get()
            movie_url = movie_url.replace(self.username + "/", "")
            title = movie.css("h3.headline-3 a::text").get()
            watched_on = movie.css('td.diary-day a::attr("href")').get()
            # get watched date, then remove / at the end of string
            watched_on = watched_on[-11:][:-1]

            movie_item = movie_loader.load_item()

            yield response.follow(
                movie_url, callback=self.parse_movies, meta={"dir_item": dir_item}
            )
            # yield scrapy.Request(url=url, callback=self.parse_movies)
            # yield {"title": title, "link": movie_url, "watched_on": watched_on}

    def parse_movies(self, response):
        """
        parse the movie page e.g. letterboxd.com/film/<title>

        css selector cheat sheet
        https://www.w3schools.com/cssref/css_selectors.php
        .class
        #id
        div > p     select all <p> elements where <div> is a parent element
        attribute[^=value]  select element whose attribute begin with value

        """
        loader = ItemLoader(item=MovieItem(), response=response)

        movie_title = response.css("h1.headline-1::text").get()
        loader.add_css("title", "h1.headline-1::text")
        loader.add_css("director", 'div#tab-crew a[href^="/director"]::text')
        loader.add_css("actors", "div.cast-list p a::text")
        loader.add_css("actors_link", 'div.cast-list p a::attr("href")')
        loader.add_css("genres", 'div#tab-genres a[href^="/films/genre"]::text')
        loader.add_css("rating", 'head > meta[name="twitter:data2"]::attr(content)')
        loader.add_css("country", 'div#tab-details a[href^="/films/country"]::text')
        loader.add_css("production_company", 'div#tab-details a[href^="/studio"]::text')
        loader.add_css("release_year", 'a[href^="/films/year"]::text')
        loader.add_value(
            "watched_on",
            len(self.diary.loc[self.diary["Name"] == movie_title, "Watched Date"]),
        )
        loader.add_value(
            "user_rating",
            self.diary.loc[self.diary["Name"] == movie_title, "Rating"].tolist(),
        )

        yield loader.load_item()
