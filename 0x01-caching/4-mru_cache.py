#!/usr/bin/env python3
"""This module has a class named <MRUCache> that inherit from
    BasicCaching class.
"""
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """This class uses the MRU caching algorithm"""
    counter = 0

    def __init__(self):
        """initializing"""
        super().__init__()
        self.recent = {}

    def put(self, key, item):
        """add the item(value) to the dictionary with the key"""
        if key and item:
            self.counter += 1
            if (
                len(self.cache_data) == self.MAX_ITEMS
                and not self.cache_data.get(key)
            ):
                sorted_recent = sorted(
                    self.recent, key=self.recent.get, reverse=True
                    )
                # print(sorted_recent)
                most_recent_key = sorted_recent[0]
                del self.recent[most_recent_key]
                del self.cache_data[most_recent_key]
                print(f"DISCARD: {most_recent_key}")
            self.recent[key] = self.counter
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if self.cache_data.get(key):
            self.counter += 1
            self.recent[key] = self.counter
            return self.cache_data.get(key)
        return None
