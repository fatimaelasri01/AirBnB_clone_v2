#!/usr/bin/python3
"""This modules defines a class to manage
database storage for HBNBclone"""

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Class representation of database storage
    """
    __engine = None
    __session = None
    check_class = {"Amenity": Amenity,
                   "City": City, "Place": Place, "Review": Review,
                   "State": State, "User": User}

    def __init__(self):
        """constructor for DB class
        """
        env = getenv("HBNB_ENV")
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        hostname = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(username, password,
                                             hostname, database),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns dictionary representation of a model
        currently in storage"""

        new_dict = {}

        if cls is None:
            for k, v in self.check_class.items():
                query_obj = self.__session.query(v).all()
                for _obj in query_obj:
                    key = "{}.{}".format(_obj.__class__.__name__, _obj.id)
                    new_dict[key] = _obj
        else:
            # for k, v in self.check_class.items():
            # if cls == type(v):
            query_obj = self.__session.query(cls).all()
            for _obj in query_obj:
                key = "{}.{}".format(_obj.__class__.__name__, _obj.id)
                new_dict[key] = _obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database
        session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all databases and create current session
        if not already created
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute
        (self.__session) tips or close() on the class Session tips
        """
        self.__session.close()
