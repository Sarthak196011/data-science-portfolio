"""
AeroPlan Prismatic Destinations & Departure Hubs Data
"""

DEPARTURE_AIRPORTS = [
    {
        "id": "JFK",
        "code": "JFK",
        "name": "New York (JFK) — USA",
        "city": "New York",
        "country": "USA",
        "lat": 40.6413,
        "lng": -73.7781,
        "timezone": "America/New_York"
    },
    {
        "id": "LHR",
        "code": "LHR",
        "name": "London Heathrow (LHR) — UK",
        "city": "London",
        "country": "UK",
        "lat": 51.4700,
        "lng": -0.4543,
        "timezone": "Europe/London"
    },
    {
        "id": "HND",
        "code": "HND",
        "name": "Tokyo Haneda (HND) — Japan",
        "city": "Tokyo",
        "country": "Japan",
        "lat": 35.5494,
        "lng": 139.7798,
        "timezone": "Asia/Tokyo"
    },
    {
        "id": "DXB",
        "code": "DXB",
        "name": "Dubai International (DXB) — UAE",
        "city": "Dubai",
        "country": "UAE",
        "lat": 25.2532,
        "lng": 55.3657,
        "timezone": "Asia/Dubai"
    },
    {
        "id": "CDG",
        "code": "CDG",
        "name": "Paris Charles de Gaulle (CDG) — France",
        "city": "Paris",
        "country": "France",
        "lat": 49.0097,
        "lng": 2.5479,
        "timezone": "Europe/Paris"
    },
    {
        "id": "DEL",
        "code": "DEL",
        "name": "Delhi Indira Gandhi (DEL) — India",
        "city": "Delhi",
        "country": "India",
        "lat": 28.5562,
        "lng": 77.1000,
        "timezone": "Asia/Kolkata"
    },
    {
        "id": "SIN",
        "code": "SIN",
        "name": "Singapore Changi (SIN) — Singapore",
        "city": "Singapore",
        "country": "Singapore",
        "lat": 1.3644,
        "lng": 103.9915,
        "timezone": "Asia/Singapore"
    },
    {
        "id": "SYD",
        "code": "SYD",
        "name": "Sydney Kingsford Smith (SYD) — Australia",
        "city": "Sydney",
        "country": "Australia",
        "lat": -33.9399,
        "lng": 151.1753,
        "timezone": "Australia/Sydney"
    },
    {
        "id": "SFO",
        "code": "SFO",
        "name": "San Francisco (SFO) — USA",
        "city": "San Francisco",
        "country": "USA",
        "lat": 37.6213,
        "lng": -122.3790,
        "timezone": "America/Los_Angeles"
    },
    {
        "id": "FRA",
        "code": "FRA",
        "name": "Frankfurt Airport (FRA) — Germany",
        "city": "Frankfurt",
        "country": "Germany",
        "lat": 50.0379,
        "lng": 8.5622,
        "timezone": "Europe/Berlin"
    }
]

CURATED_DESTINATIONS = [
    {
        "id": "tokyo",
        "name": "Tokyo, Japan",
        "city": "Tokyo",
        "country": "Japan",
        "lat": 35.6762,
        "lng": 139.6503,
        "region": "East Asia",
        "tags": ["Cyberpunk", "Culinary", "Temples", "Nightlife"],
        "base_daily_lodging": 240,
        "base_daily_expenses": 120,
        "hero_desc": "Neon metropolis where ancient Shinto shrines coexist with cutting-edge robotics and three-star Michelin dining.",
        "highlights": ["Shibuya Crossing & Sky", "Shinjuku Omoide Yokocho", "teamLab Planets", "Tsukiji Outer Market", "Meiji Shrine Gardens"]
    },
    {
        "id": "reykjavik",
        "name": "Reykjavík, Iceland",
        "city": "Reykjavik",
        "country": "Iceland",
        "lat": 64.1466,
        "lng": -21.9426,
        "region": "Nordic",
        "tags": ["Northern Lights", "Hot Springs", "Glaciers", "Volcanoes"],
        "base_daily_lodging": 290,
        "base_daily_expenses": 160,
        "hero_desc": "Gateway to geothermal lagoons, volcanic lava fields, cascading waterfalls, and glowing aurora borealis.",
        "highlights": ["Blue Lagoon Geothermal Spa", "Golden Circle Route", "Gullfoss Waterfall", "Harpa Concert Hall", "Black Sand Beach Vik"]
    },
    {
        "id": "cairo",
        "name": "Cairo, Egypt",
        "city": "Cairo",
        "country": "Egypt",
        "lat": 30.0444,
        "lng": 31.2357,
        "region": "North Africa",
        "tags": ["Pyramids", "Nile River", "Ancient History", "Bazaars"],
        "base_daily_lodging": 140,
        "base_daily_expenses": 70,
        "hero_desc": "Timeless civilization on the banks of the Nile, guarding 5,000 years of pharaonic wonders and gilded treasures.",
        "highlights": ["Great Pyramids of Giza & Sphinx", "Grand Egyptian Museum", "Khan el-Khalili Bazaar", "Felucca Sunset Cruise on Nile", "Old Coptic Cairo"]
    },
    {
        "id": "paris",
        "name": "Paris, France",
        "city": "Paris",
        "country": "France",
        "lat": 48.8566,
        "lng": 2.3522,
        "region": "Western Europe",
        "tags": ["Art & Fashion", "Bistros", "Architecture", "Haute Couture"],
        "base_daily_lodging": 320,
        "base_daily_expenses": 150,
        "hero_desc": "City of Light draped in Haussmannian facades, world-defining art museums, and candlelit Seine riverbanks.",
        "highlights": ["Eiffel Tower Twilight Summit", "Louvre Masterpieces Tour", "Montmartre & Sacré-Cœur", "Seine River Bateaux Mouches", "Le Marais Artisan Boutiques"]
    },
    {
        "id": "bali",
        "name": "Bali, Indonesia",
        "city": "Bali",
        "country": "Indonesia",
        "lat": -8.4095,
        "lng": 115.1889,
        "region": "Southeast Asia",
        "tags": ["Tropical Villas", "Surf", "Rice Terraces", "Wellness"],
        "base_daily_lodging": 160,
        "base_daily_expenses": 80,
        "hero_desc": "The Island of the Gods: emerald rainforests, tiered rice terraces, cliffside ocean temples, and restorative wellness sanctuaries.",
        "highlights": ["Uluwatu Temple Cliff Sunset", "Tegallalang Rice Terraces", "Seminyak Beachfront Lounges", "Mount Batur Sunrise Trek", "Nusa Penida Coral Lagoon"]
    },
    {
        "id": "rio",
        "name": "Rio de Janeiro, Brazil",
        "city": "Rio de Janeiro",
        "country": "Brazil",
        "lat": -22.9068,
        "lng": -43.1729,
        "region": "South America",
        "tags": ["Copacabana", "Samba", "Sugarloaf", "Carnival"],
        "base_daily_lodging": 190,
        "base_daily_expenses": 95,
        "hero_desc": "Sensory coastal metropolis nestled between emerald granite peaks, Atlantic surf, and pulsating bossa nova rhythms.",
        "highlights": ["Christ the Redeemer Summit", "Sugarloaf Mountain Cable Car", "Ipanema Sunset Session", "Santa Teresa Bohemian Quarter", "Tijuca National Forest"]
    },
    {
        "id": "capetown",
        "name": "Cape Town, South Africa",
        "city": "Cape Town",
        "country": "South Africa",
        "lat": -33.9249,
        "lng": 18.4241,
        "region": "Southern Africa",
        "tags": ["Table Mountain", "Winelands", "Penguins", "Ocean Drive"],
        "base_daily_lodging": 210,
        "base_daily_expenses": 110,
        "hero_desc": "Dramatic convergence of two oceans against the flat-topped grandeur of Table Mountain and world-class wine estates.",
        "highlights": ["Table Mountain Aerial Cableway", "Cape Point Nature Reserve", "Boulders Beach African Penguins", "Stellenbosch Vineyard Tasting", "Kirstenbosch Botanical Canopy"]
    },
    {
        "id": "swiss_alps",
        "name": "Zermatt, Swiss Alps",
        "city": "Zermatt",
        "country": "Switzerland",
        "lat": 46.0207,
        "lng": 7.7491,
        "region": "Central Europe",
        "tags": ["Matterhorn", "Luxury Skiing", "Alpine Chalets", "Fondue"],
        "base_daily_lodging": 450,
        "base_daily_expenses": 220,
        "hero_desc": "Car-free alpine sanctuary crowned by the iconic jagged pyramid of the Matterhorn, offering pure glacial luxury.",
        "highlights": ["Gornergrat Panoramic Railway", "Matterhorn Glacier Paradise", "Hinterdorf Heritage Walk", "Alpine Thermal Spa", "Gourmet Chalet Fondue Experience"]
    },
    {
        "id": "santorini",
        "name": "Santorini, Greece",
        "city": "Santorini",
        "country": "Greece",
        "lat": 36.3932,
        "lng": 25.4615,
        "region": "Mediterranean",
        "tags": ["Caldera", "Whitewashed Oia", "Aegean Sunsets", "Wine"],
        "base_daily_lodging": 380,
        "base_daily_expenses": 170,
        "hero_desc": "Volcanic cliffside wonder with cobalt-domed churches, cliff-hanging infinity pools, and legendary Aegean sunsets.",
        "highlights": ["Oia Sunset Walk", "Private Catamaran Caldera Cruise", "Akrotiri Prehistoric City", "Assyrtiko Volcanic Wine Tasting", "Red Beach Scenic Cove"]
    },
    {
        "id": "dubai",
        "name": "Dubai, UAE",
        "city": "Dubai",
        "country": "UAE",
        "lat": 25.2048,
        "lng": 55.2708,
        "region": "Middle East",
        "tags": ["Burj Khalifa", "Desert Safari", "Supercars", "Skyline"],
        "base_daily_lodging": 350,
        "base_daily_expenses": 180,
        "hero_desc": "Hyper-futuristic desert oasis of architectural superlatives, opulent luxury resorts, and high-adrenaline desert experiences.",
        "highlights": ["Burj Khalifa At The Top Sky", "Premium Red Dune Desert Safari", "Museum of the Future", "Palm Jumeirah Helicopter Tour", "Dubai Marina Yacht Cruise"]
    }
]
