#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship



class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs.get('password') is not None:
            passwd = kwargs['password']
            del kwargs['password']
            self.__secure_password(passwd)
        super().__init__(*args, **kwargs)

    def __set_password(self, passwd):
        """sets a password with md5 encryption"""
        secure = hashlib.md5()
        secure.update(passwd.encode("utf-8"))
        self.password = secure.hexdigest()
