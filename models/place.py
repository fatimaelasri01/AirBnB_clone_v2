#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.review import Review
from os import getenv


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60), ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))

class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    city = relationship("City", backref="places")
    user = relationship("User", backref="places")

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review",
                               cascade='all, delete, delete-orphan',
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)
    else:
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
