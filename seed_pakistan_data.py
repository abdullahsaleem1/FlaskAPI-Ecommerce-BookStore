"""
Seed script for Pakistani cities and provinces reference data
This creates a JSON file that can be used by the frontend for dropdowns
"""

import json
import os

# Pakistani Provinces and their major cities
PAKISTAN_DATA = {
    "Punjab": [
        "Lahore", "Faisalabad", "Rawalpindi", "Multan", "Gujranwala",
        "Sialkot", "Bahawalpur", "Sargodha", "Sheikhupura", "Jhang",
        "Gujrat", "Kasur", "Rahim Yar Khan", "Sahiwal", "Okara",
        "Wah Cantt", "Dera Ghazi Khan", "Chiniot", "Kamoke", "Mandi Bahauddin",
        "Hafizabad", "Jhelum", "Khanpur", "Muzaffargarh", "Attock"
    ],
    "Sindh": [
        "Karachi", "Hyderabad", "Sukkur", "Larkana", "Nawabshah",
        "Mirpur Khas", "Jacobabad", "Shikarpur", "Khairpur", "Dadu",
        "Thatta", "Badin", "Tando Allahyar", "Tando Adam", "Umerkot",
        "Sanghar", "Ghotki", "Naushahro Feroze", "Matiari", "Jamshoro"
    ],
    "Khyber Pakhtunkhwa": [
        "Peshawar", "Mardan", "Abbottabad", "Mingora", "Kohat",
        "Dera Ismail Khan", "Swabi", "Charsadda", "Nowshera", "Mansehra",
        "Bannu", "Swat", "Haripur", "Karak", "Lakki Marwat",
        "Chitral", "Dir", "Hangu", "Battagram", "Buner"
    ],
    "Balochistan": [
        "Quetta", "Turbat", "Khuzdar", "Hub", "Gwadar",
        "Chaman", "Zhob", "Sibi", "Loralai", "Dera Murad Jamali",
        "Mastung", "Kalat", "Pishin", "Dera Bugti", "Kharan"
    ],
    "Gilgit-Baltistan": [
        "Gilgit", "Skardu", "Chilas", "Hunza", "Ghanche",
        "Ghizer", "Astore", "Diamer", "Nagar"
    ],
    "Azad Kashmir": [
        "Muzaffarabad", "Mirpur", "Kotli", "Rawalakot", "Bagh",
        "Bhimber", "Palandri", "Sudhnoti", "Neelum", "Hattian"
    ],
    "Islamabad Capital Territory": [
        "Islamabad"
    ]
}

def seed_pakistan_data():
    """Create JSON file with Pakistani provinces and cities"""
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to JSON file
    output_file = 'data/pakistan_cities.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(PAKISTAN_DATA, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Pakistani cities and provinces data saved to {output_file}")
    print(f"\nTotal Provinces/Territories: {len(PAKISTAN_DATA)}")
    for province, cities in PAKISTAN_DATA.items():
        print(f"  - {province}: {len(cities)} cities")
    
    # Also create a frontend-friendly version
    frontend_file = 'frontend/assets/js/pakistan-data.js'
    with open(frontend_file, 'w', encoding='utf-8') as f:
        f.write('// Pakistani Provinces and Cities Data\n')
        f.write('const PAKISTAN_DATA = ')
        json.dump(PAKISTAN_DATA, f, indent=2, ensure_ascii=False)
        f.write(';\n')
    
    print(f"✅ Frontend data file created at {frontend_file}")

if __name__ == '__main__':
    seed_pakistan_data()
