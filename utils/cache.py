import os
import time
import hashlib
import functools

import pickle
import pandas as pd

def local_cache(function):
    def hash_url(url: str) -> str:
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    @functools.wraps(function)
    def wrapper(url: str, *args, **kwargs):
        cache_dir = 'cache_data'
        hash_value = hash_url(url)
        cache_file = f'{cache_dir}/{hash_value}.parquet'

        # create cache folder
        os.makedirs(cache_dir, exist_ok=True)

        if os.path.exists(cache_file):
            # if file exists, read from local
            with open(cache_file, "rb") as f:
                result = pickle.load(f)
        else:
            # if not exist, fetch result and save to local
            result = function(url, *args, **kwargs)
            with open(cache_file, "wb") as f:
                pickle.dump(result, f)

        return result

    return wrapper