from abc import ABC, abstractmethod


class Database(ABC):

    def __init__(self) -> None:
        self.__schema = None

    @abstractmethod
    def get(self):
        """Getting a database table object on this instance"""

    ###########################################################################
    #                               PROPERTIES                                #
    ###########################################################################

    @property
    def schema(self):
        return self.__schema