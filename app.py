from flask import Flask, render_template, url_for
import os
from pathlib import Path
from PIL import Image
import random

app = Flask(__name__)

# Custom country order
COUNTRY_ORDER = [
    "Spain",
    "Iceland",
    "Morocco",
    "Croatia",
    "Greece",
    "Portugal",
    "Hungary",
    "United Kingdom",
    "Germany",
    "Netherlands",
    "Austria",
    "Slovakia",
    "Czech Republic"  # Adding this at the end since it wasn't in the specified order
]

# Your travel data
TRAVEL_DATA = {
    "Spain": {
        "flag": "🇪🇸",
        "cities": ["Barcelona", "Tarragona", "Valencia", "Girona", "Montserrat", "Málaga", "Granada", "Seville"]
    },
    "Austria": {
        "flag": "🇦🇹",
        "cities": ["Vienna"]
    },
    "Slovakia": {
        "flag": "🇸🇰",
        "cities": ["Bratislava"]
    },
    "Hungary": {
        "flag": "🇭🇺",
        "cities": ["Budapest"]
    },
    "Netherlands": {
        "flag": "🇳🇱",
        "cities": ["Amsterdam", "Rotterdam"]
    },
    "Germany": {
        "flag": "🇩🇪",
        "cities": ["Berlin"]
    },
    "United Kingdom": {
        "flag": "🇬🇧",
        "cities": ["London"]
    },
    "Czech Republic": {
        "flag": "🇨🇿",
        "cities": ["Prague"]
    },
    "Iceland": {
        "flag": "🇮🇸",
        "cities": ["Reykjavík"]
    },
    "Morocco": {
        "flag": "🇲🇦",
        "cities": ["Marrakech"]
    },
    "Croatia": {
        "flag": "🇭🇷",
        "cities": ["Split"]
    },
    "Greece": {
        "flag": "🇬🇷",
        "cities": ["Mykonos", "Crete"]
    },
    "Portugal": {
        "flag": "🇵🇹",
        "cities": ["Lagos", "Lisbon"]
    }
}

VISITED_COUNTRIES = [
    "France"
]

def get_images_in_folder(folder_path):
    """Get all image files in a folder."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    try:
        return sorted([
            f.name for f in Path(folder_path).iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ])
    except Exception:
        return []

# Make the function available to templates
app.jinja_env.globals.update(get_images_in_folder=get_images_in_folder)

@app.route('/')
def home():
    # Get the first image from each country folder
    countries_with_images = {}
    for country, data in TRAVEL_DATA.items():
        country_path = os.path.join('static', 'photos', country)
        images = get_images_in_folder(country_path)
        countries_with_images[country] = {
            **data,
            'main_image': images[0] if images else None
        }
    
    # Sort countries according to the custom order
    sorted_countries = {}
    for country in COUNTRY_ORDER:
        if country in countries_with_images:
            sorted_countries[country] = countries_with_images[country]
    
    return render_template('index.html', countries=sorted_countries)

@app.route('/country/<country>')
def country(country):
    if country not in TRAVEL_DATA:
        return "Country not found", 404
    
    # Get the first image from each city folder
    cities_with_images = {}
    for city in TRAVEL_DATA[country]['cities']:
        city_path = os.path.join('static', 'photos', country, city)
        images = get_images_in_folder(city_path)
        cities_with_images[city] = {
            'main_image': images[0] if images else None
        }
    
    return render_template('country.html', 
                         country=country, 
                         data=TRAVEL_DATA[country],
                         cities_with_images=cities_with_images)

@app.route('/city/<country>/<city>')
def city(country, city):
    if country not in TRAVEL_DATA or city not in TRAVEL_DATA[country]['cities']:
        return "City not found", 404
    
    # Get all images from the city folder
    city_path = os.path.join('static', 'photos', country, city)
    images = get_images_in_folder(city_path)
    
    return render_template('city.html', 
                         country=country, 
                         city=city, 
                         flag=TRAVEL_DATA[country]['flag'],
                         images=images)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/map')
def map_page():
    # List of countries you've visited
    visited_countries = [
        # Project countries
        "Spain", "Iceland", "Morocco", "Croatia", "Greece", "Portugal", "Hungary",
        "United Kingdom", "Germany", "Netherlands", "Austria", "Slovakia", "Czech Republic",
        # Additional countries
        "Israel", "Denmark", "Norway", "Poland", "Turks and Caicos", "Canada", "Costa Rica",
        "United States"
    ]
    bucket_list_countries = [
        "Turkey",
        "Japan",
        "Singapore",
        "United Arab Emirates",
        "Switzerland",
        "United Republic of Tanzania",
        "New Zealand",
        "Australia",
        "Madagascar",
    ]
    return render_template('map.html', visited_countries=visited_countries, bucket_list_countries=bucket_list_countries)

if __name__ == '__main__':
    # Run the app on all network interfaces (0.0.0.0) on port 5001
    app.run(host='0.0.0.0', port=5001, debug=True) 