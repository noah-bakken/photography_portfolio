import json

# Load the GeoJSON file
with open('worold.svg') as f:
    data = json.load(f)

# Print all country names from ADMIN field
for feature in data['features']:
    print(feature['properties']['ADMIN'])
