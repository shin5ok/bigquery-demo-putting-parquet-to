import faker
from datetime import datetime as dt

def get(n=10, json_path: str = ""):

    f = faker.Faker()
    record = '{'

    i = 1
    while n > 0:

        t = dt.now().strftime("%Y%m%dT%H:%M:%S")
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

    if json_path:
        with open(json_path, "w") as f:
            f.write(record)

    return record
