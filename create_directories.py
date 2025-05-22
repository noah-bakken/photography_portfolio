import os
from app import TRAVEL_DATA

def create_directory_structure():
    base_path = 'static/photos'
    
    # Create directories for each country and city
    for country in TRAVEL_DATA:
        country_path = os.path.join(base_path, country)
        os.makedirs(country_path, exist_ok=True)
        
        # Create directories for each city in the country
        for city in TRAVEL_DATA[country]['cities']:
            city_path = os.path.join(country_path, city)
            os.makedirs(city_path, exist_ok=True)
            
            # Create placeholder images for each city
            for i in range(1, 7):  # 6 photos per city
                photo_path = os.path.join(city_path, f'photo{i}.jpg')
                if not os.path.exists(photo_path):
                    os.symlink(
                        os.path.join('..', '..', 'placeholder', 'placeholder.jpg'),
                        photo_path
                    )
        
        # Create main country image placeholder
        main_path = os.path.join(country_path, 'main.jpg')
        if not os.path.exists(main_path):
            os.symlink(
                os.path.join('..', 'placeholder', 'placeholder.jpg'),
                main_path
            )

if __name__ == '__main__':
    create_directory_structure() 