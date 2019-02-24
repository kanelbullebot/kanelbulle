import json
from cachetools import cached, TTLCache

string_cache = TTLCache(maxsize=100, ttl=300)

@cached(string_cache)
def translate(lang: str, string: str, **kwargs):
    with open(f"lang/master/lang/{lang}/translate.json") as dataf:
        returntranslatedstring = json.load(dataf)
    return returntranslatedstring[string].format(**kwargs)
