#!/usr/bin/env python3
"""This module has a class named <LFUCache> that inherit from
    BasicCaching class.
"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """This class uses the LFU caching algorithm"""
    counter = 0

    def __init__(self):
        """initializing"""
        super().__init__()
        self.frequent = {}

    def put(self, key, item):
        """add the item(value) to the dictionary with the key"""
        if key and item:
            # LFU -> Least Recently Used
            if (
                len(self.cache_data) == self.MAX_ITEMS
                and not self.cache_data.get(key)
            ):
                sorted_recent = sorted(self.frequent, key=self.frequent.get)
                least_frequent_key = sorted_recent[0]
                del self.frequent[least_frequent_key]
                del self.cache_data[least_frequent_key]
                print(f"DISCARD: {least_frequent_key}")
            if not self.frequent.get(key):
                self.frequent[key] = 0
            self.frequent[key] += 1
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if self.cache_data.get(key):
            self.frequent[key] += 1
            return self.cache_data.get(key)
        return None
