from flask import Flask, render_template, url_for
import os
import shutil
from app import app, TRAVEL_DATA, COUNTRY_ORDER

def generate_static():
    # Create static directory if it doesn't exist
    if not os.path.exists('static_site'):
        os.makedirs('static_site')
    
    # Copy static files
    if os.path.exists('static'):
        shutil.copytree('static', 'static_site/static', dirs_exist_ok=True)
    
    # Generate index.html
    with app.test_request_context():
        # Generate home page
        html = render_template('index.html', countries=TRAVEL_DATA)
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
                city_dir = f'{country_dir}/{city}'
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
            html = render_template(f'{page}.html')
            with open(f'static_site/{page}/index.html', 'w', encoding='utf-8') as f:
                f.write(html)

if __name__ == '__main__':
    generate_static() 