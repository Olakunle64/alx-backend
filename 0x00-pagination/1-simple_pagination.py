#!/usr/bin/env python3
"""This module has a class named <Server>"""


import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """return a tuple of size two containing a start
        index and an end index corresponding to the
        range of indexes to return in a list for those
        particular pagination parameters
    """
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """return the appropriate page of the dataset"""
        # check if the page and page_size are valid
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        pagination = index_range(page, page_size)
        dataset = self.dataset()
        # check if the pagination is out of range
        if (
            pagination[0] > len(dataset) - 1
            or
            len(dataset[pagination[0]:]) < page_size
        ):
            return []
        return dataset[pagination[0]:pagination[1]]
