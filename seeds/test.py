import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

json_data = open(f"{dir_path}/event.json")
parsed_json = json.load(json_data)
json_data.close()

for i in parsed_json:
    name = i["fields"]["name"]
    lower = name.lower().replace("'", "").replace(".", "").strip()
    slug = lower.replace(" ", "-")
    with open(f"{dir_path}/slug.txt", "a") as file:
        file.write(f"{slug}\n")


# data1 = json.load(json_data)  # deserialises it
# data2 = json.dumps(data1)  # json formatted string
# json_data.close()

# with open(f"{dir_path}/event.json") as json_file:
#     data = json.load(json_file)
#     for i in json_data[0]:
#         print(i.fields.name)

