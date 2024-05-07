#!/usr/bin/env python3
"""This module has a class named <FIFOCache> that inherit from
    BasicCaching class.
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """This class uses the FIFO caching algorithm"""
    def __init__(self):
        """initializing"""
        super().__init__()

    def put(self, key, item):
        """add the item(value) to the dictionary with the key"""
        if key and item:
            if (
                len(self.cache_data) == self.MAX_ITEMS
                and not self.cache_data.get(key)
            ):
                first_key = list(self.cache_data.keys())[0]
                del self.cache_data[first_key]
                print(f"DISCARD: {first_key}")
            if self.cache_data.get(key):
                del self.cache_data[key]
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if self.cache_data.get(key):
            return self.cache_data.get(key)
        return None
