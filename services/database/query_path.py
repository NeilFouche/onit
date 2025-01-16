"""
QueryPath class
"""

from libs.strings import camel_to_snake


class QueryPath:
    """Class to represent a path of queries between tables"""

    def __init__(self, path_data):
        self._path_data = path_data
        self._size = len(self._path_data)
        self._first_item = None
        self._index = 0
        self._names = []
        self._nodes = []

    @staticmethod
    def flatten_data(data):
        """Flattens the data structure"""
        nodes = [data]

        if data and "child" in data.keys():
            nodes.extend(QueryPath.flatten_data(data["child"]))

        return nodes

    def get_current(self):
        """
        Returns the current item in the loop
        """
        return self._path_data[self._index] if self._path_data else None

    def next(self):
        """
        Focuses the next item if it exists
        """
        self._index += 1

    def at_end(self):
        """
        Checks if the iteration has reached the end
        """
        return self._index == self._size or not self._path_data

    def is_last(self):
        """
        Checks if the current iteration is the last
        """
        return self._index == self._size - 1

    @property
    def data(self):
        """
        Serializes the path data
        """
        return self._path_data

    @property
    def first(self):
        """
        Returns the first item in the path
        """
        if not self._first_item:
            self._first_item = self._path_data[0] if self._path_data else None

        return self._first_item

    @property
    def size(self):
        """
        Returns the size of the path
        """
        return self._size

    @property
    def names(self):
        """
        Returns the names of the nodes on the path
        """
        if not self._names:
            self._names = [
                camel_to_snake(node['table_name'])
                for node in self._path_data
            ]

        return self._names

    @property
    def nodes(self):
        """
        Returns the nodes on the path
        """

        return self._path_data

    ###########################################################################
    #                             SPECIAL METHODS                             #
    ###########################################################################

    def __iter__(self):
        return self

    def __next__(self):
        if self.at_end():
            raise StopIteration

        current = self.get_current()
        self.next()
        return current

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return self._path_data[index]

    def __setitem__(self, index, value):
        if index >= self.size:
            raise IndexError("Index out of range")
        self._path_data[index] = value
