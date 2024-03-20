#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.city import City


class State(BaseModel, Base):
    """ model representation of a `State` table
    Attributes:
        name: name of state
        if `db` is selected;
            cities: constraint to delete a City instance if its
                corresponding State instance is deleted.
        else:
            cities: a list of cities
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City",
                              cascade='all, delete, delete-orphan',
                              backref="state")
    else:
        @property
        def cities(self):
            """return a list of city instances"""
            from models import storage
            city_list = []
            cities_dict = storage.all(City)
            for inst in cities_dict.values():
                if self.id == inst.state_id:
                    city_list.append(inst)
            return city_list
