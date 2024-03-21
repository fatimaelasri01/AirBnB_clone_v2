#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models.review import Review


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60), ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """Python model representation of a `Place` database """
    __tablename__ = "places"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        reviews = relationship("Review",
                               cascade='all, delete, delete-orphan',
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)
    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """returns a list of Review instances"""
            from models import storage
            review_list = []
            reviews_dict = storage.all(Review)
            for inst in reviews_dict.values():
                if self.id == inst.place_id:
                    review_list.append(inst)
            return review_list

        @property
        def amenities(self):
            """returns a list of amenity instances"""
            from models import storage
            amenity_list = []
            for item in storage.all(Amenity).values():
                if item.id in self.amenity_ids:
                    amenity_list.append(item)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            """setter for amenities"""
            from models.amenity import Amenity
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
