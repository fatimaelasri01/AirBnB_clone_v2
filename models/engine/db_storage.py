from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage():
    """Class for db storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes storage"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'
            .format(getenv("HBNB_MYSQL_USER"),
                    getenv("HBNB_MYSQL_PWD"),
                    getenv("HBNB_MYSQL_HOST"),
                    getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

    def all(self, cls=None):
        """returns all objs of cls"""
        if cls is None:
            cls_list = [State, City, User, Place, Review, Amenity]
            return {type(obj).__name__ + '.' + obj.id: obj
                    for cls in cls_list
                    for obj in self.__session.query(cls).all()}
        else:
            return {type(obj).__name__ + '.' + obj.id: obj
                    for obj in self.__session.query(cls).all()}

    def new(self, obj):
        """add obj to db"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit changes to db"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from db"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """create all tables in the db"""
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)

        f_se = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(f_se)
        self.__session = Session()

    def close(self):
        """Close session"""
        self.__session.close()
