from flask import Flask, render_template, url_for
import os
import shutil
from app import app, TRAVEL_DATA, COUNTRY_ORDER, get_images_in_folder

def generate_static():
    # Create static directory if it doesn't exist
    if not os.path.exists('static_site'):
        os.makedirs('static_site')
    
    # Copy static files
    if os.path.exists('static'):
        shutil.copytree('static', 'static_site/static', dirs_exist_ok=True)
    
    # Generate index.html
    with app.test_request_context():
        # Prepare countries with main image and custom ordering
        countries_with_images = {}
        for country, data in TRAVEL_DATA.items():
            country_path = os.path.join('static', 'photos', country)
            images = get_images_in_folder(country_path)
            countries_with_images[country] = {
                **data,
                'main_image': images[0] if images else None
            }

        sorted_countries = {}
        for country in COUNTRY_ORDER:
            if country in countries_with_images:
                sorted_countries[country] = countries_with_images[country]

        # Generate home page
        html = render_template('index.html', countries=sorted_countries)
        with open('static_site/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Generate country pages
        for country in TRAVEL_DATA:
            country_dir = f'static_site/country/{country}'
            os.makedirs(country_dir, exist_ok=True)
            
            html = render_template('country.html', 
                                 country=country, 
                                 data=TRAVEL_DATA[country])
            with open(f'{country_dir}/index.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            # Generate city pages
            for city in TRAVEL_DATA[country]['cities']:
                # Match dynamic route structure: /city/<country>/<city>
                city_dir = f'static_site/city/{country}/{city}'
                os.makedirs(city_dir, exist_ok=True)
                
                # Get images for this city
                city_path = f'static/photos/{country}/{city}'
                images = []
                if os.path.exists(city_path):
                    images = [f for f in os.listdir(city_path) 
                            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
                
                html = render_template('city.html',
                                     country=country,
                                     city=city,
                                     flag=TRAVEL_DATA[country]['flag'],
                                     images=images)
                with open(f'{city_dir}/index.html', 'w', encoding='utf-8') as f:
                    f.write(html)
        
        # Generate about and contact pages
        for page in ['about', 'contact']:
            page_dir = f'static_site/{page}'
            os.makedirs(page_dir, exist_ok=True)
            html = render_template(f'{page}.html')
            with open(f'{page_dir}/index.html', 'w', encoding='utf-8') as f:
                f.write(html)

        # Generate map page
        map_dir = 'static_site/map'
        os.makedirs(map_dir, exist_ok=True)
        visited_countries = [
            "Spain", "Iceland", "Morocco", "Croatia", "Greece", "Portugal", "Hungary",
            "United Kingdom", "Germany", "Netherlands", "Austria", "Slovakia", "Czech Republic",
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
        html = render_template('map.html', visited_countries=visited_countries, bucket_list_countries=bucket_list_countries)
        with open(f'{map_dir}/index.html', 'w', encoding='utf-8') as f:
            f.write(html)

if __name__ == '__main__':
    generate_static() 