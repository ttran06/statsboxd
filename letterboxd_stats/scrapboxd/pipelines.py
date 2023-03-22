# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from sqlalchemy.orm import sessionmaker
from .models import (
    db_connect,
    create_table,
    Movie,
    Director,
    Actor,
    Genre,
    ProductionCompany,
)


class MysqlPipeline:
    def __init__(self) -> None:
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        logging.info("*****MysqlPipe: database connected*****")

    def process_item(self, item, spider):
        """
        Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        movie = Movie()
        director = Director()
        actor = Actor()
        genre = Genre()
        production_company = ProductionCompany()

        movie.title = item["title"]
        movie.rating = item["rating"]
        movie.release_year = item["release_year"]
        movie.num_watch = item["num_watch"]
        movie.user_rating = item["mean"]

        for director_name in item["director"]:
            director = Director(name=director_name)
            exist_director = (
                session.query(Director).filter_by(name=director.name).first()
            )
            if exist_director is not None:
                director = exist_director
            movie.director.append(director)

        for actor_name, actor_link in zip(item["actors"], item["actors_link"]):
            actor = Actor(name=actor_name, link=actor_link)
            exist_actor = session.query(Actor).filter_by(link=actor.link).first()
            if exist_actor is not None:
                actor = exist_actor
            movie.actors.append(actor)

        for genre_type in item["genres"]:
            genre = Genre(genre=genre_type)
            exist_genre = session.query(Genre).filter_by(genre=genre.genre).first()
            if exist_genre is not None:
                genre = exist_genre
            movie.genres.append(genre)

        for production_company_name in item["production_company"]:
            production_company = ProductionCompany(
                production_company=production_company_name
            )
            exist_production_company = (
                session.query(ProductionCompany)
                .filter_by(production_company=production_company.production_company)
                .first()
            )
            if exist_production_company is not None:
                production_company = exist_production_company
            movie.production_company.append(production_company)

        try:
            session.add(movie)
            session.commit()
        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
