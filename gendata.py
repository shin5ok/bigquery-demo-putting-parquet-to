import faker
from datetime import datetime as dt
import pytz

jst = pytz.timezone('Asia/Tokyo')

def get(n=10):

    f = faker.Faker()
    record = '{'

    i = 1
    while n > 0:

        t = dt.now(jst).strftime("%Y%m%dT%H:%M:%S")
        record += f'''
            "{i}":{{
                  "id": "{f.uuid4()}",
                  "name": "{f.name()}",
                  "attr": {{
                      "user_name":"{f.user_name()}",
                      "email":"{f.email()}",
                      "address":"{f.address()}"
                  }},
                  "update_at": "{t}"
              }}'''

        i += 1
        n -= 1
        if n > 0:
            record += ","

    record += '\n   }'

    return record
