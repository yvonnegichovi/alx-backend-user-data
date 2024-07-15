#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        This method adds a user
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by arbitrary keyword arguments
        Args:
            - **kwargs: Arbitrary keyword arguments for filtering the query
        Returns:
            - User: The first user found
        Raises:
            - NoResultFound: If no user is found
            - InvalidRequestError: If the query arguments are invalid
        """
        try:
            query = self._session.query(User).filter_by(**kwargs)
            user = query.one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the provided arguments.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user
        Args:
            - user_id: user id to be updated
            - **kwargs: arbitrary keyword arguments
        Returns:
            - None
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError("Invalid argument: {}".format(key))
        self._session.commit()
