import json
import requests
import os

current_path = os.path.dirname(os.path.abspath(__file__))

data = None
print(os.path.join(current_path, 'config.json'))
with open(os.path.join(current_path, 'config.json')) as f:
    data = json.load(f)

session = requests.Session()

session.headers.update({
    "X-MBX-APIKEY": "ezdgFJZaMbC3v7peg73hIjTjBuqIglZWxbQDAcro6mYPFutE0Rei0UjWZzhSFR8H"
})

class Config:

    def __new__(self):
        self.session = session
        for key, value in data.items():
            setattr(self, key, value)
        return self

