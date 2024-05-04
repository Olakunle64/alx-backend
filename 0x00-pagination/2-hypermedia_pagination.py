#!/usr/bin/env python3
"""This module has a class named <Server>"""


import csv
import math
from typing import List, Tuple, Dict, Any


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
            pagination[1] >= len(dataset[pagination[0]:])
        ):
            return []
        return dataset[pagination[0]:pagination[1]]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """return a dictionary with the following key-value pairs:

            page_size: the length of the returned dataset page
            page: the current page number
            data: the dataset page (equivalent to return from previous task)
            next_page: number of the next page, None if no next page
            prev_page: number of the previous page, None if no previous page
            total_pages: the total number of pages in the dataset as an integer
        """
        data = self.get_page(page, page_size)
        next_page = None
        prev_page = None
        try:
            if self.get_page(page + 1, page_size):
                next_page = page + 1
        except AssertionError:
            pass
        try:
            if self.get_page(page - 1, page_size):
                prev_page = page - 1
        except AssertionError:
            pass
        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": len(self.dataset())
        }
