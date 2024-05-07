#!/usr/bin/env python3
"""This module has a class named <BasicCache> that inherit from
    BasicCaching class.
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """This class uses the basic caching algorithm"""
    def put(self, key, item):
        """add the item(value) to the dictionary with the key"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        if self.cache_data.get(key):
            return self.cache_data.get(key)
        return None
