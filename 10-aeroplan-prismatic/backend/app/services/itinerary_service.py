"""Curated and Procedural Itinerary Service with Exact Locations"""
from typing import List, Dict, Any

CURATED_HUBS: List[Dict[str, Any]] = [
    {"id": "tokyo", "name": "Tokyo, Japan", "city": "Tokyo", "lat": 35.6762, "lng": 139.6503, "lodging": 240, "exp": 120},
    {"id": "reykjavik", "name": "Reykjavík, Iceland", "city": "Reykjavik", "lat": 64.1466, "lng": -21.9426, "lodging": 290, "exp": 160},
    {"id": "cairo", "name": "Cairo, Egypt", "city": "Cairo", "lat": 30.0444, "lng": 31.2357, "lodging": 140, "exp": 70},
    {"id": "paris", "name": "Paris, France", "city": "Paris", "lat": 48.8566, "lng": 2.3522, "lodging": 320, "exp": 150},
    {"id": "bali", "name": "Bali, Indonesia", "city": "Bali", "lat": -8.4095, "lng": 115.1889, "lodging": 160, "exp": 80},
    {"id": "rio", "name": "Rio de Janeiro, Brazil", "city": "Rio", "lat": -22.9068, "lng": -43.1729, "lodging": 190, "exp": 95},
    {"id": "capetown", "name": "Cape Town, South Africa", "city": "Cape Town", "lat": -33.9249, "lng": 18.4241, "lodging": 210, "exp": 110},
    {"id": "swiss_alps", "name": "Zermatt, Swiss Alps", "city": "Zermatt", "lat": 46.0207, "lng": 7.7491, "lodging": 450, "exp": 220},
    {"id": "santorini", "name": "Santorini, Greece", "city": "Santorini", "lat": 36.3932, "lng": 25.4615, "lodging": 380, "exp": 170},
    {"id": "dubai", "name": "Dubai, UAE", "city": "Dubai", "lat": 25.2048, "lng": 55.2708, "lodging": 350, "exp": 180}
]

DESTINATION_ITINERARIES: Dict[str, List[Dict[str, Any]]] = {
  "tokyo": [
    {
      "day": 1,
      "title": "Ancient Heritage, Sumida Waters & Shibuya Skyline",
      "theme": "Historic Shrines & Neon Panoramas",
      "locations": [
        "Sens\u014d-ji Temple",
        "Kaminarimon Gate",
        "Nakamise-dori",
        "Sumida River Cruise",
        "Shibuya Crossing",
        "Shibuya Sky"
      ],
      "morning": "09:00 - 12:30: Historic Asakusa exploration. Enter through the iconic Kaminarimon (Thunder Gate), stroll Nakamise-dori sampling freshly pressed ningyo-yaki, and offer incense at Sens\u014d-ji Temple, Tokyo's oldest temple.",
      "afternoon": "13:30 - 17:00: Board the futuristic Himiko water bus on the Sumida River toward Hamarikyu Gardens. Transfer to Shibuya to experience the world's busiest pedestrian crossing and ascend to Shibuya Sky for 360-degree glass deck sunset views over Tokyo.",
      "evening": "18:30 - 21:30: Navigate lantern-lit alleys of Omoide Yokocho (Memory Lane) in Shinjuku for charcoal yakitori skewers, wagyu bites, and craft highballs.",
      "culinary": "Omoide Yokocho Yakitori & Shibuya Sky Horizon Cocktails"
    },
    {
      "day": 2,
      "title": "Sacred Forests, Avant-Garde Pop & Roppongi Arts",
      "theme": "Imperial Shrines & Contemporary Culture",
      "locations": [
        "Meiji Jingu Shrine",
        "Yoyogi Forest",
        "Takeshita Street",
        "Omotesando Architecture",
        "Mori Art Museum (Roppongi)"
      ],
      "morning": "08:30 - 12:00: Walk beneath towering cypress torii gates into the serene cedar forest of Meiji Jingu Shrine in Shibuya. Witness traditional Shinto morning purification rituals.",
      "afternoon": "13:00 - 16:30: Explore quirky youth fashion along Harajuku's Takeshita Street, then transition to tree-lined Omotesando Avenue to admire flagship architectural designs by Tadao Ando and SANAA.",
      "evening": "17:30 - 21:00: Ascend Roppongi Hills Mori Tower to tour contemporary exhibitions at the Mori Art Museum and enjoy Tokyo City View observation deck gazing at Tokyo Tower's amber illumination.",
      "culinary": "Artisan Tonkatsu at Maisen Aoyama & Roppongi Hills Wine Bar"
    },
    {
      "day": 3,
      "title": "Culinary Gastronomy, Digital Universe & Imperial Ginza",
      "theme": "Seafood Markets & Sensory Art",
      "locations": [
        "Tsukiji Outer Market",
        "teamLab Planets (Toyosu)",
        "Ginza Six Rooftop",
        "Kabuki-za Theatre"
      ],
      "morning": "07:30 - 11:30: Early morning gourmet safari through Tsukiji Outer Market. Savor flame-torched fatty tuna (otoro) nigiri, tamagoyaki rolled omelet, and fresh Hokkaido uni from heritage vendors.",
      "afternoon": "12:30 - 16:00: Wade through crystal water rooms and interactive digital flower projections at teamLab Planets in Toyosu. Return to Ginza for luxury gallery hopping and tea ceremony atop Ginza Six garden.",
      "evening": "18:00 - 21:30: Classical Kabuki theatre architectural viewing followed by a master omakase sushi experience in historic Ginza.",
      "culinary": "Michelin Omakase Sushi in Ginza & Matcha Parfait at Tsujiri"
    },
    {
      "day": 4,
      "title": "Subculture Neon, National Treasures & Shitamachi Retro",
      "theme": "Cyberpunk Otaku & Classical Preservation",
      "locations": [
        "Akihabara Electric Town",
        "Ueno Onshi Park",
        "Tokyo National Museum",
        "Yanaka Ginza Alleyways"
      ],
      "morning": "09:30 - 12:30: Dive into the multi-floor anime, retro arcade, and electronics emporiums of Akihabara Electric Town, including Radio Kaikan and Mandarake Complex.",
      "afternoon": "13:30 - 16:30: Stroll through cherry tree groves of Ueno Park and inspect samurai armor and National Treasure scrolls inside Tokyo National Museum.",
      "evening": "17:00 - 20:30: Step back into 1950s Tokyo in Yanaka Ginza. Walk the 'Sunset Stairs' (Yuyake Dandan), visit craft potteries, and dine at a wooden Edo-era soba house.",
      "culinary": "Handcrafted Juwari Soba in Yanaka & Craft Beer at Yanaka Beer Hall"
    },
    {
      "day": 5,
      "title": "Imperial Gardens, Observatories & Golden Gai Intimacy",
      "theme": "Botanical Tranquility & Micro-Bars",
      "locations": [
        "Shinjuku Gyoen National Garden",
        "Tokyo Metropolitan Government Building",
        "Kagurazaka Geisha Quarter",
        "Golden Gai"
      ],
      "morning": "09:00 - 12:00: Wander the expansive Japanese landscape and French formal gardens of Shinjuku Gyoen, discovering historic teahouses and bonsai greenhouses.",
      "afternoon": "13:00 - 16:30: Ascend 202 meters to the 45th-floor observatory of the Tokyo Metropolitan Government Building for panoramic Mt. Fuji vistas. Afterward, explore cobblestone geisha alleys in Kagurazaka.",
      "evening": "18:00 - 22:30: Twilight exploration of Shinjuku's famed Golden Gai \u2014 a labyrinth of 200 miniature six-seat bars brimming with jazz, vinyl records, and bespoke cocktails.",
      "culinary": "Kaiseki multi-course dinner in Kagurazaka & bespoke cocktails in Golden Gai"
    },
    {
      "day": 6,
      "title": "Coastal Samurai Citadel: Kamakura & Enoshima Island",
      "theme": "Day Excursion: Zen Temples & Pacific Coast",
      "locations": [
        "Kotoku-in Great Buddha",
        "Hase-dera Temple",
        "Tsurugaoka Hachimangu",
        "Enoshima Sea Candle"
      ],
      "morning": "08:30 - 12:00: Coastal train ride to historic Kamakura. Stand before the majestic 13-meter bronze Kotoku-in Great Buddha, then marvel at coastal hydrangea gardens at Hase-dera.",
      "afternoon": "13:00 - 16:30: Walk Kamakura's Wakamiya Oji boulevard to Tsurugaoka Hachimangu Shrine. Ride the vintage Enoden coastal tram along the Pacific shoreline to Enoshima Island.",
      "evening": "17:00 - 20:30: Ascend Enoshima Sea Candle lighthouse for Mt. Fuji silhouettes at dusk, then feast on fresh shirasu (whitebait) bowls at seaside cliffside taverns.",
      "culinary": "Fresh Pacific Shirasu Don & Candied Sweet Potato Croquettes"
    },
    {
      "day": 7,
      "title": "Odaiba Futuristic Bay & Grand Farewell Celebration",
      "theme": "Bayside Horizon & Ceremonial Farewell",
      "locations": [
        "Odaiba Seaside Park",
        "Unicorn Gundam Statue",
        "Rainbow Bridge",
        "Tokyo Skytree"
      ],
      "morning": "09:30 - 12:30: Ride the driverless Yurikamome monorail across Rainbow Bridge to Odaiba. Witness the life-sized Unicorn Gundam transformation display and explore seaside boardwalks.",
      "afternoon": "13:30 - 17:00: Leisure souvenir shopping for wagashi and ceramics at Solamachi mall at the base of Tokyo Skytree, followed by Skytree 450m Tembo Galleria deck views.",
      "evening": "18:30 - 22:00: Celebration farewell dinner: Premium Japanese A5 Kuroge Wagyu Teppanyaki with panoramic Tokyo skyline views overlooking Rainbow Bridge.",
      "culinary": "A5 Wagyu Teppanyaki Dinner overlooking Tokyo Bay"
    }
  ],
  "reykjavik": [
    {
      "day": 1,
      "title": "Capital Architecture, Thermal Vistas & Old Harbour",
      "theme": "Nordic Design & Coastal Charm",
      "locations": [
        "Hallgr\u00edmskirkja Church",
        "Laugavegur Shopping Promenade",
        "Harpa Concert Hall",
        "Old Harbour"
      ],
      "morning": "09:00 - 12:00: Ascend the 74m basalt-column inspired tower of Hallgr\u00edmskirkja Church for panoramic views across Reykjav\u00edk's colorful corrugated rooftops and Mt. Esja.",
      "afternoon": "13:00 - 16:30: Stroll down lively Laugavegur street discovering Icelandic wool craft and design boutiques. Tour the crystalline glass honeycomb facade of Harpa Concert Hall on the waterfront.",
      "evening": "17:30 - 21:00: Walk the Old Harbour piers, sample steaming Langoustine lobster soup in a converted fishermen's shack, and watch fishing vessels return against arctic twilight.",
      "culinary": "Langoustine Lobster Soup at S\u00e6greifinn & Icelandic Rye Bread Ice Cream"
    },
    {
      "day": 2,
      "title": "The Golden Circle: Tectonic Rifts & Roaring Geysers",
      "theme": "Earth's Raw Forces",
      "locations": [
        "\u00deingvellir National Park",
        "Geysir Geothermal Area",
        "Strokkur Spout",
        "Gullfoss Golden Waterfall"
      ],
      "morning": "08:30 - 12:00: Walk between the North American and Eurasian tectonic plates in the Almannagj\u00e1 canyon at \u00deingvellir, site of the world's oldest parliament.",
      "afternoon": "12:30 - 15:30: Witness the Strokkur geysir shoot boiling water 30 meters into the air every 6-10 minutes, surrounded by steaming turquoise mineral pools and bubbling fumaroles.",
      "evening": "16:00 - 20:00: Stand on the edge of Gullfoss waterfall feeling the glacial spray of the Hv\u00edt\u00e1 River thunder down a two-tiered 32m chasm into rugged canyon depths.",
      "culinary": "Slow-cooked Icelandic Lamb Stew at Gullfoss Caf\u00e9 & Geothermal Rye Bread"
    },
    {
      "day": 3,
      "title": "South Coast Splendor: Glacial Cascades & Basalt Shores",
      "theme": "Waterfalls & Black Sand Beaches",
      "locations": [
        "Seljalandsfoss",
        "Gljufrabui Hidden Cave",
        "Sk\u00f3gafoss",
        "Reynisfjara Black Sand Beach"
      ],
      "morning": "08:00 - 11:30: Journey south along the Ring Road. Walk directly behind the 60m veil of Seljalandsfoss waterfall, then wade into the canyon crevice concealing secret Gljufrabui.",
      "afternoon": "12:30 - 15:30: Climb the 527 steps alongside powerful Sk\u00f3gafoss for endless coastal plains views, and visit the heritage turf houses at Sk\u00f3gar Museum.",
      "evening": "16:00 - 20:30: Marvel at towering hexagonal basalt sea columns and roaring Atlantic breakers at Reynisfjara Black Sand Beach near the picturesque hamlet of V\u00edk.",
      "culinary": "Arctic Char with Dill Butter in V\u00edk & Craft Skyr Cake"
    },
    {
      "day": 4,
      "title": "Reykjanes Peninsula & Blue Lagoon Geothermal Sanctuary",
      "theme": "Volcanic Rejuvenation",
      "locations": [
        "Bridge Between Continents",
        "Gunnuhver Mud Pools",
        "Blue Lagoon Geothermal Spa",
        "Grindav\u00edk Lava Fields"
      ],
      "morning": "09:30 - 12:30: Explore the moonscape craters of Reykjanes UNESCO Geopark, walking the footbridge spanning the Mid-Atlantic Ridge and witnessing Gunnuhver's howling steam vent.",
      "afternoon": "13:30 - 17:30: Immerse yourself in the warm 39\u00b0C milky-blue geothermal waters of the world-renowned Blue Lagoon. Apply silica and algae face masks directly from wooden bar tubs.",
      "evening": "18:30 - 21:30: Dine overlooking the volcanic lava fields at Lava Restaurant, indulging in four-course fresh cod and birch-smoked lamb paired with fine wines.",
      "culinary": "Four-course New Nordic Tasting at Lava Restaurant"
    },
    {
      "day": 5,
      "title": "Glacial Lagoon Jewels: J\u00f6kuls\u00e1rl\u00f3n & Diamond Beach",
      "theme": "Deep Blue Ice & Drifting Icebergs",
      "locations": [
        "Vatnaj\u00f6kull Glacier",
        "J\u00f6kuls\u00e1rl\u00f3n Glacier Lagoon",
        "Diamond Beach",
        "Skaftafell"
      ],
      "morning": "08:00 - 12:30: Scenic drive along Vatnaj\u00f6kull, Europe's largest glacier cap. Board an amphibious zodiac craft to cruise among electric-blue icebergs calved from Brei\u00f0amerkurj\u00f6kull.",
      "afternoon": "13:30 - 16:30: Walk Diamond Beach (Brei\u00f0amerkursandur) where glistening crystal icebergs wash ashore on jet-black volcanic sand like scattered diamonds.",
      "evening": "17:30 - 21:00: Easy hike to Svartifoss waterfall in Skaftafell, framed by dark basalt organ pipe columns, followed by warm glacier lodge dining.",
      "culinary": "Smoked Arctic Trout & Wild Cloudberry Tart"
    },
    {
      "day": 6,
      "title": "Sn\u00e6fellsnes Peninsula: 'Iceland in Miniature'",
      "theme": "Glacial Peaks & Sea Arches",
      "locations": [
        "Kirkjufell Mountain & Falls",
        "Dj\u00fapal\u00f3nssandur Beach",
        "L\u00f3ndrangar Basalt Pinnacles",
        "Arnarstapi Cliffs"
      ],
      "morning": "08:30 - 12:00: Photograph the arrowhead silhouette of Mount Kirkjufell and its twin waterfalls, made famous worldwide in cinematic landscapes.",
      "afternoon": "13:00 - 16:30: Test your strength on the historic lifting stones of Dj\u00fapal\u00f3nssandur black pebble cove, then walk the dramatic coastal cliff archways of Arnarstapi.",
      "evening": "17:30 - 21:00: Sunset coastal drive under the glow of Sn\u00e6fellsj\u00f6kull glacier-capped stratovolcano, legendary inspiration for Jules Verne's Journey to the Center of the Earth.",
      "culinary": "Pan-seared Wolf Fish in Stykkish\u00f3lmur with Organic Barley"
    },
    {
      "day": 7,
      "title": "Perlan Wonders, Whale Safari & Aurora Borealis",
      "theme": "Arctic Wildlife & Farewell Lights",
      "locations": [
        "Faxafl\u00f3i Bay Whale Watching",
        "Perlan Glass Dome",
        "\u00c1rb\u00e6r Open Air Museum",
        "Aurora Night Cruise"
      ],
      "morning": "09:00 - 12:00: Board an eco-friendly catamaran from Reykjav\u00edk harbour into Faxafl\u00f3i Bay to spot humpback whales, minke whales, and white-beaked dolphins leaping in the surf.",
      "afternoon": "13:00 - 16:30: Visit Perlan's revolving glass dome to explore a real 100-meter man-made indoor ice cave and experience the 8K northern lights planetarium show.",
      "evening": "18:00 - 22:30: Farewell gourmet dinner at Michelin-starred Dill, followed by a late-night sea voyage away from city lights hunting the vibrant green ribbons of the Aurora Borealis.",
      "culinary": "Michelin-starred Foraged Icelandic Tasting Menu at Dill"
    }
  ],
  "cairo": [
    {
      "day": 1,
      "title": "Wonders of Antiquity: Giza Plateau & The Great Sphinx",
      "theme": "Pharaonic Immersion",
      "locations": [
        "Great Pyramid of Khufu",
        "Pyramid of Khafre",
        "Pyramid of Menkaure",
        "The Great Sphinx",
        "Panoramic Sunset Camel Trail"
      ],
      "morning": "08:00 - 12:30: Step onto the Giza Plateau to stand before the colossal Great Pyramid of Khufu, the sole surviving Wonder of the Ancient World. Enter the inner burial chamber.",
      "afternoon": "13:30 - 16:30: Visit the Valley Temple of Khafre and gaze face-to-face with the mystical lion-bodied Great Sphinx, carved from a single limestone ridge.",
      "evening": "17:00 - 20:30: Camel trek across the desert dunes for a panoramic triple-pyramid sunset backdrop, followed by open-air Egyptian grilled mezze at historic Mena House.",
      "culinary": "Mena House Royal Kebab & Kofta overlooking Illuminated Pyramids"
    },
    {
      "day": 2,
      "title": "Grand Egyptian Museum & King Tutankhamun Treasures",
      "theme": "Imperial Gold & Monumental Artifacts",
      "locations": [
        "Grand Egyptian Museum (GEM)",
        "Statue of Ramesses II",
        "Tutankhamun Galleries",
        "Solar Boat Museum"
      ],
      "morning": "09:00 - 13:00: Enter the breathtaking atrium of the Grand Egyptian Museum (GEM) dominated by the 3,200-year-old colossal statue of Ramesses II and the grand stepped staircase.",
      "afternoon": "14:00 - 17:00: Marvel at the complete 5,000-piece royal collection of King Tutankhamun displayed together for the first time, including his solid gold funerary death mask and golden thrones.",
      "evening": "18:00 - 21:00: Leisure stroll along the landscaped gardens overlooking the desert plateau with traditional fresh pomegranate juice and mint tea.",
      "culinary": "Molokhia with roasted duck and golden Egyptian bread"
    },
    {
      "day": 3,
      "title": "Medieval Citadel, Islamic Minarets & Khan el-Khalili",
      "theme": "Sultans, Spices & Souks",
      "locations": [
        "Citadel of Saladin",
        "Mosque of Muhammad Ali",
        "Al-Mu'izz Street",
        "Khan el-Khalili Bazaar"
      ],
      "morning": "09:00 - 12:00: Ascend the medieval Citadel of Saladin to marvel at the alabaster domes and soaring minarets of the Mosque of Muhammad Ali with panoramic views of Cairo.",
      "afternoon": "13:00 - 16:30: Walk down Al-Mu'izz li-Din Allah al-Fatimi Street, the greatest concentration of medieval Islamic architecture in the Arab world, visiting historic madrasas and complexes.",
      "evening": "17:00 - 21:30: Dive into the sensory labyrinth of Khan el-Khalili bazaar. Savor spiced coffee at historic El Fishawy Caf\u00e9 (operating since 1773) while artisans hammer copper lanterns.",
      "culinary": "Crispy Koshary at Abou Tarek & Spiced Arabic Mint Tea at El Fishawy"
    },
    {
      "day": 4,
      "title": "The Dawn of Pyramids: Saqqara, Memphis & Dahshur",
      "theme": "Architectural Evolution of the Pharaohs",
      "locations": [
        "Step Pyramid of Djoser (Saqqara)",
        "Tomb of Mereruka",
        "Memphis Open-Air Museum",
        "Dahshur Red & Bent Pyramids"
      ],
      "morning": "08:30 - 12:00: Explore Saqqara necropolis and the Step Pyramid of Djoser, engineered by Imhotep in the 27th century BC as humanity's first monumental stone building.",
      "afternoon": "13:00 - 16:00: Visit Memphis, ancient Egypt's first capital, to inspect the fallen limestone colossus of Ramesses II. Continue to Dahshur to examine the fascinating Bent Pyramid and smooth Red Pyramid.",
      "evening": "17:30 - 20:30: Countryside sunset drive past date palm groves and quiet rural canals, enjoying farm-fresh fiteer meshaltet pastry dipped in wild clover honey.",
      "culinary": "Authentic Fiteer Meshaltet with local white cheese and black molasses"
    },
    {
      "day": 5,
      "title": "Historic Coptic Cairo & Sunset Nile Felucca",
      "theme": "Sacred Enclaves & River Rhythms",
      "locations": [
        "The Hanging Church",
        "Church of St. Sergius and Bacchus",
        "Ben Ezra Synagogue",
        "Coptic Museum",
        "Nile Felucca Sail"
      ],
      "morning": "09:00 - 12:30: Enter the fortress walls of Roman Babylon to explore Coptic Cairo. Walk through the nave of the Hanging Church (Al-Muallaqa) suspended over Roman gatehouses.",
      "afternoon": "13:30 - 16:00: Descend into the crypt of the Church of St. Sergius where the Holy Family took refuge during their flight into Egypt, and tour the historic Ben Ezra Synagogue.",
      "evening": "16:30 - 20:00: Board a traditional wooden Egyptian Felucca sailboat with white canvas sails to glide along the Nile at golden hour as evening city lights mirror across the water.",
      "culinary": "Grilled Sea Bass and Tahini on a Private Nile Waterfront Terrace"
    },
    {
      "day": 6,
      "title": "Mediterranean Coastal Excursion: Alexandria by the Sea",
      "theme": "Greco-Roman Elegance",
      "locations": [
        "Catacombs of Kom El Shoqafa",
        "Pompey's Pillar",
        "Citadel of Qaitbay",
        "Bibliotheca Alexandrina"
      ],
      "morning": "07:30 - 12:00: Morning train or private express to Alexandria on the Mediterranean coast. Descend three levels into the subterranean rock-cut Catacombs of Kom El Shoqafa.",
      "afternoon": "13:00 - 16:30: Visit the 15th-century defensive Citadel of Qaitbay built on the exact foundations of the ancient Pharos Lighthouse. Tour the stunning modern Bibliotheca Alexandrina.",
      "evening": "17:00 - 20:30: Seaside corniche walk feeling the Mediterranean sea breeze, dining on grilled calamari and jumbo red sea prawns before returning to Cairo.",
      "culinary": "Alexandrian Seafood Feast at Fish Market Restaurant on the Corniche"
    },
    {
      "day": 7,
      "title": "Zamalek Bohemian Island & Royal Farewell Banquet",
      "theme": "Modern Culture & Pharaonic Celebration",
      "locations": [
        "Cairo Tower",
        "Zamalek Art Galleries",
        "Museum of Egyptian Civilization (NMEC)",
        "Royal Mummies Hall"
      ],
      "morning": "10:00 - 12:30: Ascend the lotus-shaped Cairo Tower on Gezira Island for a 360-degree cityscape view, then explore leafy Zamalek's independent art galleries and antique shops.",
      "afternoon": "13:30 - 17:00: Visit the National Museum of Egyptian Civilization (NMEC) to witness the Royal Mummies Hall, where 22 ancient kings and queens are enshrined in climate-controlled state.",
      "evening": "18:30 - 22:00: Royal farewell banquet aboard an upscale vintage Nile river yacht with live Oud music and traditional Sufi Tanoura whirling dervish performances.",
      "culinary": "Slow-braised Lamb Shank with Saffron Spiced Rice & Pistachio Baklava"
    }
  ],
  "paris": [
    {
      "day": 1,
      "title": "Iron Lady Majesty, River Seine & Saint-Germain",
      "theme": "Iconic Paris Landmarks",
      "locations": [
        "Eiffel Tower Summit",
        "Champ de Mars",
        "Pont Alexandre III",
        "Seine River Cruise",
        "Saint-Germain-des-Pr\u00e9s"
      ],
      "morning": "09:00 - 12:30: Ascend the Eiffel Tower summit via panoramic glass lifts to gaze over the Haussmannian boulevard grid, followed by a leisurely stroll across Champ de Mars lawns.",
      "afternoon": "13:30 - 16:30: Cross the gilded Pont Alexandre III bridge. Board an open-air river cruise on the Seine gliding beneath historic stone archways past the Grand Palais and Mus\u00e9e d'Orsay.",
      "evening": "17:30 - 21:30: Immerse yourself in the literary caf\u00e9 culture of Saint-Germain-des-Pr\u00e9s, settling into Caf\u00e9 de Flore or Les Deux Magots before a candlelit bistro dinner.",
      "culinary": "Steak Frites at Le Relais de l'Entrec\u00f4te & Hot Chocolate at Caf\u00e9 de Flore"
    },
    {
      "day": 2,
      "title": "Louvre Treasures, Tuileries & Belle \u00c9poque Opulence",
      "theme": "Masterpieces & Imperial Gardens",
      "locations": [
        "Mus\u00e9e du Louvre",
        "Jardin des Tuileries",
        "Place Vend\u00f4me",
        "Palais Garnier Opera House"
      ],
      "morning": "09:00 - 12:30: Enter through I.M. Pei's glass pyramid into the Mus\u00e9e du Louvre. View the Mona Lisa, Winged Victory of Samothrace, Venus de Milo, and Napoleon III's state apartments.",
      "afternoon": "13:30 - 16:30: Stroll past fountains and marble sculptures in Jardin des Tuileries. Window shop high jewelry salons on Place Vend\u00f4me and tour the velvet-and-gold Palais Garnier Opera.",
      "evening": "18:00 - 21:30: Walk covered 19th-century glass-roof passages (Galerie Vivienne) discovering rare bookshops, wine cellars, and artisan tea rooms.",
      "culinary": "Duck Confit in Galerie Vivienne & Signature Mont-Blanc pastry at Angelina"
    },
    {
      "day": 3,
      "title": "Bohemian Montmartre, Sacr\u00e9-C\u0153ur & Vineyard Alleys",
      "theme": "Artists, Windmills & Skyline Vistas",
      "locations": [
        "Sacr\u00e9-C\u0153ur Basilica",
        "Place du Tertre",
        "Clos Montmartre Vineyard",
        "Moulin de la Galette",
        "Pigalle"
      ],
      "morning": "09:30 - 12:30: Ascend the cobblestone stairways of the Montmartre butte to Sacr\u00e9-C\u0153ur Basilica. Admire the panoramic views over Paris from the parvis, then watch painters at Place du Tertre.",
      "afternoon": "13:30 - 16:30: Discover the hidden Clos Montmartre hillside vineyard, Le Passe-Muraille sculpture, and the historic windmills of Moulin de la Galette frequented by Renoir.",
      "evening": "17:30 - 21:00: Descend to South Pigalle (SoPi) for natural wine bars and modern bistro cooking in Paris's most vibrant culinary quarter.",
      "culinary": "Artisan French Cheeses, Charcuterie & Natural Wines in Montmartre"
    },
    {
      "day": 4,
      "title": "Gothic Heart: Notre-Dame, Sainte-Chapelle & Latin Quarter",
      "theme": "Stained Glass & Medieval Paris",
      "locations": [
        "\u00cele de la Cit\u00e9",
        "Notre-Dame Cathedral",
        "Sainte-Chapelle",
        "Latin Quarter",
        "Shakespeare and Company"
      ],
      "morning": "09:00 - 12:30: Marvel at the newly restored Gothic majesty of Notre-Dame Cathedral on \u00cele de la Cit\u00e9, then step inside Sainte-Chapelle to stand surrounded by 1,113 glowing 13th-century stained-glass panels.",
      "afternoon": "13:30 - 16:30: Cross Pont Saint-Michel into the Latin Quarter. Browse vintage books inside legendary Shakespeare and Company and explore the grand dome of the Panth\u00e9on.",
      "evening": "17:30 - 21:30: Relax beside the Medici Fountain in Jardin du Luxembourg before savoring fondue or savory galettes along Rue Mouffetard.",
      "culinary": "Buckwheat Galettes with Emmental and Cider on Rue Mouffetard"
    },
    {
      "day": 5,
      "title": "Royal Splendor: Palace of Versailles & Trianon Estate",
      "theme": "Sun King Legacy & Fountains",
      "locations": [
        "Palace of Versailles",
        "Hall of Mirrors",
        "King's Grand Apartments",
        "Gardens of Versailles",
        "Queen's Hamlet"
      ],
      "morning": "08:30 - 12:30: Royal excursion to the Palace of Versailles. Walk the 73-meter Hall of Mirrors reflecting morning sunlight across 357 mirrors, and tour the King's state bedchambers.",
      "afternoon": "13:30 - 16:30: Explore Andr\u00e9 Le N\u00f4tre's geometric formal gardens with musical fountain displays. Rent a bicycle to reach the rustic Queen's Hamlet (Hameau de la Reine).",
      "evening": "17:30 - 20:30: Return to Paris for a relaxed evening in the Marais district, sipping aperitifs around the symmetrical arcades of Place des Vosges.",
      "culinary": "Beef Bourguignon and Bordeaux Wine at a Marais Heritage Auberge"
    },
    {
      "day": 6,
      "title": "Impressionist Masterpieces, Rodin Sculptures & Le Marais",
      "theme": "Monet, Sculptures & Fashion",
      "locations": [
        "Mus\u00e9e d'Orsay",
        "Mus\u00e9e Rodin",
        "Rue des Rosiers",
        "Place des Vosges"
      ],
      "morning": "09:30 - 12:30: Tour the converted Beaux-Arts railway station of Mus\u00e9e d'Orsay, admiring world-famous masterpieces by Monet, Van Gogh, Renoir, Degas, and C\u00e9zanne.",
      "afternoon": "13:30 - 16:30: Walk through the tranquil rose gardens of Mus\u00e9e Rodin to contemplate 'The Thinker' and 'The Gates of Hell'. Stroll through chic design boutiques of the Marais.",
      "evening": "17:30 - 21:30: Savor world-famous warm falafel on Rue des Rosiers followed by delicate French macarons and pastry tastings.",
      "culinary": "L'As du Fallafel on Rue des Rosiers & Pierre Herm\u00e9 Ispahan Macarons"
    },
    {
      "day": 7,
      "title": "Champs-\u00c9lys\u00e9es, Arc de Triomphe & Michelin Farewell",
      "theme": "Grand Avenues & Gastronomic Summit",
      "locations": [
        "Arc de Triomphe",
        "Avenue des Champs-\u00c9lys\u00e9es",
        "Grand Palais",
        "Fondation Louis Vuitton"
      ],
      "morning": "10:00 - 12:30: Ascend to the terrace atop the Arc de Triomphe for unmatched radial views down the twelve avenues, then walk the world-famous Champs-\u00c9lys\u00e9es.",
      "afternoon": "13:30 - 16:30: Tour the contemporary sail-glass architecture of Frank Gehry's Fondation Louis Vuitton in the Bois de Boulogne.",
      "evening": "18:30 - 22:30: Grand farewell gastronomic dinner: Michelin-starred haute cuisine with Seine river panorama and a midnight sparkling toast as the Eiffel Tower flashes.",
      "culinary": "Michelin Haute Cuisine Tasting Menu with Vintage Champagne"
    }
  ],
  "bali": [
    {
      "day": 1,
      "title": "Cultural Soul: Ubud Royal Palaces & Sacred Monkey Forest",
      "theme": "Artisan Villages & Jungle Temples",
      "locations": [
        "Sacred Monkey Forest Sanctuary",
        "Ubud Royal Palace",
        "Campuhan Ridge Walk",
        "Ubud Art Market"
      ],
      "morning": "08:30 - 12:00: Wander beneath giant banyan trees and moss-draped river bridges inside the Sacred Monkey Forest Sanctuary, home to hundreds of Balinese long-tailed macaques.",
      "afternoon": "13:00 - 16:30: Visit the Puri Saren Royal Palace with intricate stone carvings, browse hand-woven ikat textiles in Ubud Art Market, and hike the green Campuhan Ridge Walk.",
      "evening": "17:30 - 21:00: Candlelit organic farm-to-table dining overlooking illuminated jungle ravines, accompanied by the gentle chime of traditional rindik bamboo gamelan.",
      "culinary": "Balinese Crispy Duck (Bebek Betutu) & Fresh Lemongrass Infusions"
    },
    {
      "day": 2,
      "title": "Cascading Terraces, Holy Springs & Kintamani Volcanics",
      "theme": "Emerald Terraces & Water Purification",
      "locations": [
        "Tegalalang Rice Terraces",
        "Tirta Empul Holy Water Temple",
        "Goa Gajah (Elephant Cave)",
        "Kintamani Highlands"
      ],
      "morning": "06:30 - 10:30: Catch sunrise rays piercing morning mist over the stepped green amphitheater of Tegalalang Rice Terraces. Walk irrigation paths and ride the canyon swings.",
      "afternoon": "11:30 - 15:30: Partake in sacred Melukat purification blessings beneath stone fountain spouts at Tirta Empul Temple. Continue up to Kintamani for views of Mount Batur and Lake Batur.",
      "evening": "16:30 - 20:00: Explore the 9th-century demonic carved entrance of Goa Gajah (Elephant Cave) before enjoying an artisanal civet coffee and spice tasting.",
      "culinary": "Highland Indonesian Nasi Campur with fresh sambal matah"
    },
    {
      "day": 3,
      "title": "Coastal Sunsets & Sacred Sea Temples: Tanah Lot",
      "theme": "Ocean Clifftops & Crashing Waves",
      "locations": [
        "Tanah Lot Sea Temple",
        "Batu Bolong Temple",
        "Canggu Echo Beach",
        "Seminyak Beach Clubs"
      ],
      "morning": "09:30 - 12:30: Coastal relaxation and surf-watching at Canggu's Echo Beach. Browse surf boutiques, organic a\u00e7ai bowls, and beachfront wooden shacks.",
      "afternoon": "13:30 - 16:00: Relax at an upscale Seminyak beach club with daybeds, infinity pools, and coconut water overlooking the Indian Ocean.",
      "evening": "16:45 - 20:30: Arrive at Tanah Lot temple perched upon a black volcanic rock outcrop. Watch roaring ocean breakers crash against the sanctuary as golden sunset envelops the silhouette.",
      "culinary": "Grilled Jimbaran-style Snapper with Jimbaran spice paste & young coconuts"
    },
    {
      "day": 4,
      "title": "Mount Batur Volcanic Sunrise & Thermal Springs",
      "theme": "Pre-Dawn Summit & Natural Healing",
      "locations": [
        "Mount Batur Caldera (1,717m)",
        "Batur Natural Hot Springs",
        "Lake Batur",
        "Besakih Mother Temple"
      ],
      "morning": "03:30 - 09:30: Pre-dawn guided hike up Mount Batur to watch the sun rise over sea clouds and Mount Agung. Enjoy eggs boiled directly in natural volcanic steam vents.",
      "afternoon": "10:30 - 14:00: Soak tired muscles in natural lakeside thermal pools at Toya Devasya on the shores of Lake Batur with volcanic mountain backdrops.",
      "evening": "15:30 - 19:30: Visit Pura Besakih, Bali's revered 'Mother Temple' perched high on the volcanic slopes of sacred Mount Agung, featuring 23 separate sanctuary complexes.",
      "culinary": "Lake Batur Tilapia with sweet soy glaze & steamed Balinese rice"
    },
    {
      "day": 5,
      "title": "Dramatic Clifftops, Kecak Fire Dance & Jimbaran Seafood",
      "theme": "Southern Peninsula Majesty",
      "locations": [
        "Pura Luhur Uluwatu",
        "Uluwatu Sea Cliffs",
        "Kecak Fire Amphitheatre",
        "Jimbaran Bay Beach"
      ],
      "morning": "10:00 - 13:00: Tour the dramatic Bukit Peninsula, visiting hidden coves like Padang Padang Beach with turquoise lagoons enclosed by limestone cliffs.",
      "afternoon": "14:00 - 17:00: Walk the winding paved clifftop path of Pura Luhur Uluwatu, suspended 70 meters above churning ocean swells.",
      "evening": "17:30 - 21:30: Witness the spellbinding open-air Sunset Kecak Fire Dance chanting against the blazing orange horizon. Head to Jimbaran Bay for candlelit seafood dinners right on the beach.",
      "culinary": "Candlelit Jimbaran Bay Grilled Seafood Platter with Tiger Prawns and Squid"
    },
    {
      "day": 6,
      "title": "Nusa Penida Island Adventure: Kelingking & Crystal Bay",
      "theme": "Island Speedboat Expedition",
      "locations": [
        "Sanur Port",
        "Kelingking T-Rex Beach",
        "Broken Beach",
        "Angel's Billabong",
        "Crystal Bay"
      ],
      "morning": "07:30 - 12:00: Speedboat crossing from Sanur to Nusa Penida. Gaze down from the dizzying viewpoint over Kelingking Beach's iconic T-Rex shaped limestone peninsula.",
      "afternoon": "13:00 - 16:30: Walk around the natural circular arch of Broken Beach and swim in the emerald tidal infinity pool at Angel's Billabong. Snorkel with tropical reef fish at Crystal Bay.",
      "evening": "17:30 - 20:30: Return speedboat to the main island as twilight settles over Bali's coastline, followed by traditional spa herbal foot baths.",
      "culinary": "Indonesian Sate Ayam with crushed peanut sauce & fresh papaya"
    },
    {
      "day": 7,
      "title": "Northern Jungle Waterfalls, Floating Temple & Spa Ritual",
      "theme": "Misty Lakes & Ultimate Relaxation",
      "locations": [
        "Sekumpul Waterfalls",
        "Ulun Danu Beratan Floating Temple",
        "Lake Bratan",
        "Luxury Ayurvedic Spa"
      ],
      "morning": "08:00 - 12:00: Hike through lush spice and cocoa plantations into the ravine of Sekumpul, Bali's most magnificent 80m twin waterfalls surrounded by sheer jungle walls.",
      "afternoon": "13:00 - 16:00: Visit the postcard-famous Ulun Danu Beratan Temple, seemingly floating effortlessly on the misty surface of alpine Lake Bratan.",
      "evening": "17:00 - 21:00: Indulge in a 2-hour Balinese Royal Lulur flower bath massage ritual, followed by a farewell candlelit celebration dinner under palm trees.",
      "culinary": "Royal Balinese Megibung Feast with whole roasted suckling pig (Babi Guling)"
    }
  ],
  "rio": [
    {
      "day": 1,
      "title": "Christ the Redeemer, Tijuca Jungle & Santa Teresa",
      "theme": "Iconic Wonders & Bohemian Heights",
      "locations": [
        "Corcovado Mountain Summit",
        "Christ the Redeemer Statue",
        "Tijuca Rainforest",
        "Santa Teresa",
        "Selar\u00f3n Steps"
      ],
      "morning": "08:00 - 12:00: Board the vintage cogwheel train climbing through the lush Atlantic rainforest of Tijuca National Park to the summit of Corcovado (710m) to stand beneath Christ the Redeemer.",
      "afternoon": "13:00 - 16:30: Explore the cobblestone hillside mansions and art studios of Santa Teresa. Walk down the 215 vibrant ceramic-tiled steps of the Escadaria Selar\u00f3n created by Jorge Selar\u00f3n.",
      "evening": "17:30 - 21:00: Enjoy craft cacha\u00e7a caipirinhas and petisco bar snacks at Bar do Mineiro in Santa Teresa, overlooking the illuminated city below.",
      "culinary": "Feijoada Completa at Bar do Mineiro & Passion Fruit Caipirinhas"
    },
    {
      "day": 2,
      "title": "Sugarloaf Cable Cars, Urca Sunset & Traditional Churrasco",
      "theme": "Guanabara Panoramas & Gaucho Barbecue",
      "locations": [
        "Morro da Urca",
        "Sugarloaf Mountain (P\u00e3o de A\u00e7\u00facar)",
        "Praia Vermelha",
        "Fogo de Ch\u00e3o Botafogo"
      ],
      "morning": "09:30 - 12:30: Relax on the tranquil pink-tinged sands of Praia Vermelha beneath Sugarloaf Mountain, exploring the shaded clifftop Claudio Coutinho coastal walking trail.",
      "afternoon": "14:00 - 17:30: Board the glass bubble cable cars (bondinho) first to Morro da Urca, then onward to Sugarloaf Mountain summit for 360-degree panoramas of Guanabara Bay and Copacabana.",
      "evening": "18:00 - 22:00: Sunset drinks at the historic Urca seawall (Mureta da Urca), followed by a world-class all-you-can-eat Brazilian Rod\u00edzio churrascaria dinner overlooking Botafogo Bay.",
      "culinary": "Prime Picanha Steak Carved Tableside at Fogo de Ch\u00e3o"
    },
    {
      "day": 3,
      "title": "Copacabana, Ipanema Beaches & Bossa Nova Sunset",
      "theme": "Carioca Beach Culture & Bossa Nova",
      "locations": [
        "Copacabana Promenade",
        "Copacabana Fort",
        "Ipanema Beach (Posto 9)",
        "Arpoador Rock"
      ],
      "morning": "09:00 - 12:30: Stroll along the famous black-and-white wave-patterned mosaic sidewalk of Copacabana Beach, sipping fresh chilled agua de coco from beach kiosks.",
      "afternoon": "13:30 - 16:30: Walk to the historic Copacabana Fort and caf\u00e9, then experience the sun-soaked vibrancy of Ipanema Beach with beach volleyball and local beachwear designers.",
      "evening": "17:00 - 21:00: Gather atop Arpoador Rock alongside hundreds of Cariocas to applaud the sun setting behind the Two Brothers (Dois Irm\u00e3os) peaks, followed by live Bossa Nova in Vinicius Bar.",
      "culinary": "Fresh A\u00e7a\u00ed Bowls with Guaran\u00e1 & Seafood Moqueca at Garota de Ipanema"
    },
    {
      "day": 4,
      "title": "Imperial Rio & Futuristic Waterfront: Downtown & Museum of Tomorrow",
      "theme": "Colonial Heritage & Futuristic Design",
      "locations": [
        "Royal Portuguese Reading Room",
        "Theatro Municipal",
        "Metropolitan Cathedral",
        "Museum of Tomorrow (Santiago Calatrava)"
      ],
      "morning": "09:00 - 12:30: Step into the awe-inspiring neo-Manueline Royal Portuguese Cabinet of Reading, containing over 350,000 historic volumes. Tour the gilded Belle \u00c9poque Theatro Municipal.",
      "afternoon": "13:30 - 16:30: Marvel at the modern cone architecture of the Metropolitan Cathedral, then ride the VLT tram along Porto Maravilha to Santiago Calatrava's futuristic cantilevered Museum of Tomorrow.",
      "evening": "17:30 - 21:00: Walk past the 3,000-square-meter colorful Olympic mural 'Etnias' by Eduardo Kobra, followed by craft beer in the historic revitalization quarter.",
      "culinary": "Past\u00e9is de Camar\u00e3o & Draft Chopp Beer in Cinel\u00e2ndia"
    },
    {
      "day": 5,
      "title": "Tropical Botanic Splendor & Contemporary Art in Niter\u00f3i",
      "theme": "Exotic Flora & Niemeyer Architecture",
      "locations": [
        "Jardim Bot\u00e2nico",
        "Avenue of Royal Palms",
        "Parque Lage",
        "Niter\u00f3i Contemporary Art Museum (MAC)"
      ],
      "morning": "09:00 - 12:30: Walk beneath 134 towering imperial palms at the Rio Botanical Garden (Jardim Bot\u00e2nico), discovering Amazonian water lilies and 600 orchid species.",
      "afternoon": "13:00 - 15:30: Photograph the iconic courtyard pool of the Italianate mansion Parque Lage, framed directly beneath Christ the Redeemer.",
      "evening": "16:00 - 20:30: Ferry across Guanabara Bay to Oscar Niemeyer's UFO-shaped Niter\u00f3i Contemporary Art Museum perched dramatic over the sea cliff.",
      "culinary": "Grilled Grouper with banana farofa & lime caipirinha"
    },
    {
      "day": 6,
      "title": "Pedra Bonita Hang Gliding & Afro-Brazilian Samba Soul",
      "theme": "Skyline Thrills & Rhythmic Nights",
      "locations": [
        "Pedra Bonita Ramp",
        "S\u00e3o Conrado Beach",
        "Pedra do Sal",
        "Lapa Arches (Arcos da Lapa)"
      ],
      "morning": "08:30 - 12:30: Ascend to Pedra Bonita for an optional tandem hang-gliding flight soaring over the ocean to land smoothly on S\u00e3o Conrado Beach, or hike to the scenic overlook.",
      "afternoon": "13:30 - 16:30: Rest along the tranquil shores of Leblon beach, discovering high-end designer stores and artisan ice cream shops.",
      "evening": "18:00 - 23:00: Experience authentic live Samba at Pedra do Sal in Little Africa (Pequena \u00c1frica), where musicians sit around a wooden table surrounded by cheering dancers, followed by Lapa nightlife.",
      "culinary": "Crispy Bolinhos de Bacalhau & Street Samba Cacha\u00e7a Cocktails"
    },
    {
      "day": 7,
      "title": "Sunset Catamaran Cruise & Grand Rooftop Farewell",
      "theme": "Maritime Elegance & Golden Farewell",
      "locations": [
        "Marina da Gl\u00f3ria",
        "Guanabara Bay Cruise",
        "Fortaleza de Santa Cruz",
        "Leblon Panoramic Rooftop"
      ],
      "morning": "10:00 - 12:30: Stroll through Flamengo Park designed by Burle Marx, admiring coastal gardens and public modernist sculptures.",
      "afternoon": "13:30 - 17:00: Embark on a private sunset catamaran cruise from Marina da Gl\u00f3ria, gliding beneath the Rio-Niter\u00f3i Bridge with cinematic viewpoints of all Rio's iconic peaks.",
      "evening": "18:30 - 22:30: Farewell celebration atop an exclusive Leblon or Ipanema rooftop lounge, toasting with sparkling Brazilian wine overlooking the Atlantic lights.",
      "culinary": "Bahian Seafood Moqueca with Dend\u00ea Oil and Coconut Rice"
    }
  ],
  "capetown": [
    {
      "day": 1,
      "title": "Table Mountain Aerial Summit & V&A Waterfront",
      "theme": "Vertical Panoramas & Harbour Life",
      "locations": [
        "Table Mountain Aerial Cableway",
        "Table Mountain Plateau",
        "Bo-Kaap Colorful Quarter",
        "V&A Waterfront"
      ],
      "morning": "08:30 - 12:00: Ascend via the 360-degree rotating Table Mountain Cableway to the 1,086m flat summit plateau. Walk hiking paths looking out over City Bowl and Camps Bay.",
      "afternoon": "13:00 - 16:00: Walk through the rainbow-hued Georgian houses and cobblestone streets of Bo-Kaap, discovering Cape Malay cultural history and fragrant spice shops.",
      "evening": "17:00 - 21:00: Stroll the bustling Victoria & Alfred Waterfront with street musicians, harbor seals, and an oceanfront seafood dinner under the evening lights.",
      "culinary": "Cape Malay Chicken Curry with Samosas & V&A Fresh Ocean Oysters"
    },
    {
      "day": 2,
      "title": "Cape Peninsula Safari: Chapman's Peak & African Penguins",
      "theme": "Coastal Cliffs & Wildlife Encounters",
      "locations": [
        "Chapman's Peak Drive",
        "Boulders Beach Penguin Colony",
        "Cape Point Nature Reserve",
        "Cape of Good Hope"
      ],
      "morning": "08:30 - 12:00: Drive the exhilarating 114 curves of Chapman's Peak Drive carved into vertical cliffs. Arrive at Boulders Beach in Simon's Town to walk boardwalks alongside thousands of wild African penguins.",
      "afternoon": "13:00 - 16:30: Explore Cape of Good Hope, the southwesternmost point of the African continent. Ride the Flying Dutchman Funicular up to the historic Cape Point Lighthouse.",
      "evening": "17:30 - 20:30: Return via the seaside surf village of Kalk Bay, stopping for golden fish and chips at the fishing harbor while watching playful Cape fur seals.",
      "culinary": "Fresh Snoek Fish & Chips in Kalk Bay with local craft cider"
    },
    {
      "day": 3,
      "title": "Cape Winelands: Stellenbosch & Franschhoek Gourmet Valley",
      "theme": "Vineyard Estates & French Huguenot Heritage",
      "locations": [
        "Stellenbosch Oak Avenues",
        "Delaire Graff Estate",
        "Franschhoek Wine Tram",
        "Haute Cabri\u00e8re Cellars"
      ],
      "morning": "09:00 - 12:30: Journey into the Cape Winelands. Walk the historic Cape Dutch and Victorian oak-lined streets of Stellenbosch before a private Pinotage tasting at Delaire Graff Estate.",
      "afternoon": "13:30 - 16:30: Board the open-sided Franschhoek Wine Tram touring between world-renowned estates nestled beneath the Franschhoek mountain amphitheater.",
      "evening": "17:30 - 21:00: Multi-course culinary tasting menu at a world-class Franschhoek vineyard restaurant paired with award-winning M\u00e9thode Cap Classique sparkling wines.",
      "culinary": "Karoo Lamb Rack paired with Stellenbosch Cabernet Sauvignon"
    },
    {
      "day": 4,
      "title": "Kirstenbosch Botanical Canopy Walk & Constantia Valley",
      "theme": "Endemic Fynbos & Historic Vineyards",
      "locations": [
        "Kirstenbosch National Botanical Garden",
        "Boomslang Tree Canopy Walkway",
        "Groot Constantia",
        "Camps Bay"
      ],
      "morning": "09:00 - 12:30: Explore the lush eastern slopes of Table Mountain inside Kirstenbosch Gardens. Walk the curved 'Boomslang' canopy bridge suspended above ancient forest treetops.",
      "afternoon": "13:30 - 16:30: Tour Groot Constantia, South Africa's oldest wine estate founded in 1685, sampling the famous Grand Constance dessert wine beloved by Napoleon Bonaparte.",
      "evening": "17:30 - 21:00: Sunset cocktails along the glamorous palm-fringed beachfront promenade of Camps Bay facing the imposing Twelve Apostles mountain peaks.",
      "culinary": "South African Braai Barbecue with Boerewors and Chakalaka"
    },
    {
      "day": 5,
      "title": "Historic Nelson Mandela Journey: Robben Island & Zeitz MOCAA",
      "theme": "Human Triumph & Contemporary African Art",
      "locations": [
        "Robben Island Ferry",
        "Maximum Security Prison (Cell 5)",
        "Zeitz MOCAA Grain Silo",
        "The Silo Rooftop"
      ],
      "morning": "08:30 - 12:30: Ferry across Table Bay to UNESCO World Heritage Robben Island. Tour the prison guided by a former political prisoner, viewing Nelson Mandela's 8x7-foot cell where he was held for 18 years.",
      "afternoon": "13:30 - 16:30: Explore Zeitz MOCAA, the world's largest museum of contemporary African art, carved out of historic 1920s concrete grain silos by architect Thomas Heatherwick.",
      "evening": "17:30 - 21:00: Sip sundowners atop the Silo Hotel rooftop with 360-degree vistas across Table Mountain, Lions Head, and the working harbor.",
      "culinary": "Pan-seared Kingklip with Cape lemon butter & Rooibos tea mousse"
    },
    {
      "day": 6,
      "title": "Atlantic Ocean Safari & Hermanus Coastal Whales",
      "theme": "Marine Big Five & Coastal Trails",
      "locations": [
        "Hermanus Cliff Path",
        "Walker Bay",
        "Hemel-en-Aarde Wine Valley",
        "Gansbaai Eco-Reserve"
      ],
      "morning": "08:00 - 12:00: Scenic drive along Clarence Drive to Hermanus. Walk the coastal cliff path spotting Southern Right Whales breaching just meters from the rocky shoreline.",
      "afternoon": "13:00 - 16:00: Tour the Hemel-en-Aarde (Heaven and Earth) Valley for cool-climate Chardonnay and Pinot Noir wine tastings surrounded by rolling green hills.",
      "evening": "17:00 - 20:30: Return along False Bay watching the glow of sunset illuminate the mountain peaks, followed by fireside coastal dining.",
      "culinary": "Local Abalone Tasting & Hemel-en-Aarde Valley Pinot Noir"
    },
    {
      "day": 7,
      "title": "Lion's Head Sunrise Summit & Grand Farewell Feast",
      "theme": "Dawn Ridges & African Celebration",
      "locations": [
        "Lion's Head Peak",
        "Clifton 4th Beach",
        "Bree Street Artisan District",
        "GOLD Restaurant"
      ],
      "morning": "06:00 - 09:30: Sunrise hike wrapping around the spiral trail of Lion's Head for first morning light breaking over Table Mountain and the Atlantic horizon.",
      "afternoon": "11:00 - 15:30: Relax on the white granite sands of secluded Clifton 4th Beach, followed by exploring the designer boutiques and art galleries along Bree Street.",
      "evening": "18:30 - 22:30: Grand celebratory farewell at GOLD Restaurant: 14-course interactive pan-African feast featuring live djembe drumming, Mali puppetry, and singer performances.",
      "culinary": "14-course Pan-African Tasting Banquet at GOLD Restaurant"
    }
  ],
  "swiss_alps": [
    {
      "day": 1,
      "title": "The Icon of Switzerland: Gornergrat Cogwheel Railway",
      "theme": "High Alpine Panoramas & Matterhorn Reflections",
      "locations": [
        "Gornergrat Bahn (3,089m)",
        "Riffelsee Alpine Lake",
        "Gorner Glacier Viewpoint",
        "Historic Zermatt Village"
      ],
      "morning": "09:00 - 12:30: Board Europe's highest open-air cogwheel railway from Zermatt village up to the 3,089m Gornergrat summit, gazing at 29 mountain peaks above 4,000 meters.",
      "afternoon": "13:30 - 16:30: Walk down to alpine Lake Riffelsee to capture the mirror reflection of the Matterhorn on crystal mountain water, then hike the alpine flower trail down to Riffelberg.",
      "evening": "17:30 - 21:00: Stroll past 500-year-old sun-blackened larchwood barns in the 'Hinterdorf' old quarter of car-free Zermatt village.",
      "culinary": "Authentic Swiss Valais Cheese Fondue & Dried B\u00fcndnerfleisch Beef"
    },
    {
      "day": 2,
      "title": "Matterhorn Glacier Paradise & The Highest Ice Palace",
      "theme": "Glacial Altitudes & Permafrost Sculptures",
      "locations": [
        "Matterhorn Glacier Paradise (3,883m)",
        "Glacier Palace Ice Grotto",
        "Theodul Glacier",
        "Cinema Lounge 3883"
      ],
      "morning": "08:30 - 12:00: Ride the 3S cableway with Swarovski crystal cabins up to the Klein Matterhorn summit (3,883m), Europe's highest cable car station.",
      "afternoon": "12:30 - 15:30: Descend 15 meters inside the living glacier into the magical Glacier Palace, walking through glistening natural ice tunnels and intricate ice sculptures.",
      "evening": "16:30 - 20:30: Warm up in an alpine panoramic spa with heated outdoor pools facing the illuminated pyramid of the Matterhorn.",
      "culinary": "Traditional Valais Raclette scraped hot over potatoes and cornichons"
    },
    {
      "day": 3,
      "title": "The Famous Five Lakes Alpine Trail (5-Seenweg)",
      "theme": "Pristine Mountain Waters & Marmots",
      "locations": [
        "Sunnegga Funicular",
        "Stellisee Lake",
        "Grindjisee Lake",
        "Gr\u00fcnsee Lake",
        "Moosjisee & Leisee"
      ],
      "morning": "08:30 - 12:30: Funicular up to Sunnegga. Embark on the 9km Five Lakes Trail beginning at pristine Stellisee, where the Matterhorn's jagged tip reflects in calm alpine water.",
      "afternoon": "13:00 - 16:30: Continue past the larch reflections of Grindjisee and turquoise glacial waters of Gr\u00fcnsee, spotting wild alpine marmots playing along rocky boulders.",
      "evening": "17:00 - 20:30: Relax on the terrace of a traditional mountain refuge in Findeln, enjoying hearty Swiss r\u00f6sti with sunny eggs and melted Gruy\u00e8re.",
      "culinary": "Crispy Swiss Potato R\u00f6sti with Valais Ham & Swiss Alpine Herbal Tea"
    },
    {
      "day": 4,
      "title": "Rothorn Summit & Glacial Gorges: Gornerschlucht",
      "theme": "Rugged Chasms & High Ridges",
      "locations": [
        "Rothorn Summit (3,103m)",
        "Fluhalp Mountain Hut",
        "Gorner Gorge (Gornerschlucht)",
        "Zermatt Museum"
      ],
      "morning": "09:00 - 12:30: Cable car ride to the Rothorn summit for an entirely different perspective of the Matterhorn's razor-sharp northeast H\u00f6rnli ridge.",
      "afternoon": "13:30 - 16:30: Walk along wooden galleries and suspension stairways clinging to sheer rock walls through the dramatic turquoise rapids of Gorner Gorge.",
      "evening": "17:30 - 20:30: Visit the subterranean Zermatlantis Matterhorn Museum to see the historic frayed rope from Edward Whymper's fateful first 1865 ascent.",
      "culinary": "Slow-cooked Swiss Veal Z\u00fcrcher Geschnetzeltes with crispy butter r\u00f6sti"
    },
    {
      "day": 5,
      "title": "Glacier Express Panoramic Segment & Alpine Thermal Baths",
      "theme": "Scenic Train Vistas & Geothermal Healing",
      "locations": [
        "Glacier Express Route",
        "Brig Historic Old Town",
        "Stockalper Palace",
        "Leukerbad Thermal Springs"
      ],
      "morning": "08:45 - 12:00: Board the glass-domed Glacier Express panoramic coach through the rugged Matter valley down to Brig, viewing dramatic alpine viaducts and gorges.",
      "afternoon": "12:30 - 16:00: Tour the baroque 17th-century Stockalper Palace courtyard in Brig, then ascend to Leukerbad to soak in 43\u00b0C mineral-rich natural hot springs.",
      "evening": "17:00 - 20:30: Return to Zermatt as mountain dusk paints the snowfields in rose-gold alpenglow, accompanied by hot gl\u00fchwein spiced wine.",
      "culinary": "Warm Swiss Spiced Gl\u00fchwein & Fresh Baked Apple Strudel"
    },
    {
      "day": 6,
      "title": "Schwarzsee Matterhorn Trail & Forest Alpine Adventures",
      "theme": "Approaching the Giant & Artisan Chocolate",
      "locations": [
        "Schwarzsee Gondola (2,583m)",
        "Maria zum Schnee Chapel",
        "Matterhorn Trail Walk",
        "Zermatt Artisan Chocolatier"
      ],
      "morning": "09:00 - 12:30: Gondola to Schwarzsee at the immediate base of the Matterhorn. Visit the tiny 'Mary of the Snow' chapel and hike directly along the base of the mighty north face.",
      "afternoon": "13:30 - 16:30: Walk down through aromatic pine forests, stopping at an artisanal Swiss chocolate boutique in Zermatt to hand-craft personalized Matterhorn chocolates.",
      "evening": "17:30 - 21:00: Enjoy a cozy fireside dinner inside a century-old chalet featuring local game meats and Valais wines like Fendant and Petite Arvine.",
      "culinary": "Handmade Swiss Matterhorn Truffles & Glass of Petite Arvine Wine"
    },
    {
      "day": 7,
      "title": "Scenic Alpine Helicopter Flight & Michelin Mountain Farewell",
      "theme": "Skyline Wonder & Michelin Gastronomy",
      "locations": [
        "Air Zermatt Heliport",
        "Matterhorn Aerial Circle",
        "Findeln Gourmet Hamlet",
        "After 7 Michelin Dining"
      ],
      "morning": "09:30 - 12:30: Scenic 20-minute helicopter flight with Air Zermatt circling the summit of the Matterhorn, Monte Rosa, and the vast Gorner Glacier crevasse fields.",
      "afternoon": "13:30 - 16:30: Relax in the car-free village or indulge in a signature Swiss pine sauna and cold mountain water plunge.",
      "evening": "18:30 - 22:00: Grand celebratory farewell dinner at Michelin-starred After 7 by Heinz Julen, savoring alpine haute cuisine framed by illuminated mountain silhouettes.",
      "culinary": "Michelin Alpine Tasting Menu at After 7 by Heinz Julen"
    }
  ],
  "santorini": [
    {
      "day": 1,
      "title": "Caldera Cliff Walk: Fira to Imerovigli & Skaros Rock",
      "theme": "Cliffside Vistas & Volcanic Panoramas",
      "locations": [
        "Fira Caldera Promenade",
        "Firostefani Blue Dome",
        "Imerovigli Clifftop",
        "Skaros Rock Promontory"
      ],
      "morning": "09:00 - 12:30: Begin the breathtaking caldera rim walk in Fira, passing whitewashed cube houses and vibrant bougainvillea to photograph the Three Bells of Fira in Firostefani.",
      "afternoon": "13:30 - 16:30: Continue along the edge of the submerged volcanic caldera to Imerovigli ('The Balcony to the Aegean') and hike the rugged promontory trail to medieval Skaros Rock.",
      "evening": "17:30 - 21:00: Check into a cliffside cave suite. Sip crisp local Assyrtiko white wine as the Aegean sunset casts pink and gold over the volcanic islands.",
      "culinary": "Santorini Fava Bean Puree with caramelized onions & local Assyrtiko wine"
    },
    {
      "day": 2,
      "title": "Postcard Perfection: Oia Village, Blue Domes & Ammoudi Bay",
      "theme": "Cycladic Whitewash & Sunsets",
      "locations": [
        "Oia Blue Domes (Agios Spyridon)",
        "Oia Castle Ruins (Agios Nikolaos)",
        "Ammoudi Bay",
        "Maritime Museum"
      ],
      "morning": "08:30 - 12:00: Morning stroll through the marble-paved lanes of Oia before the crowds. Photograph the iconic twin blue domes of Agios Spyridon and Anastasi overlooking the sapphire sea.",
      "afternoon": "12:30 - 16:00: Descend 278 steps down the red cliffside to Ammoudi Bay. Watch cliff jumpers leaping into crystal waters while fishermen tenderize fresh octopus on stone docks.",
      "evening": "17:00 - 21:30: Climb up to the ruins of Oia Byzantine Castle for the world's most famous sunset gathering, followed by waterfront seafood dining at Ammoudi.",
      "culinary": "Sun-dried Charred Octopus at Sunset Taverna in Ammoudi Bay"
    },
    {
      "day": 3,
      "title": "Private Caldera Catamaran: Volcano, Hot Springs & Red Beach",
      "theme": "Sailing the Submerged Caldera",
      "locations": [
        "Vlychada Marina",
        "Nea Kameni Volcano",
        "Palea Kameni Sulfuric Hot Springs",
        "Red Beach & White Beach"
      ],
      "morning": "09:30 - 13:00: Board a luxury catamaran cruise from Vlychada. Sail to the center of the caldera to hike the active volcanic crater of Nea Kameni.",
      "afternoon": "13:30 - 16:30: Swim in the warm sulfuric geothermal mud springs of Palea Kameni, then sail past the towering rust-red volcanic cliffs of Red Beach for snorkeling.",
      "evening": "17:00 - 20:30: Enjoy a freshly prepared Greek BBQ feast on board with grilled shrimp and Greek salad as the catamaran sails into the golden sunset.",
      "culinary": "On-board Catamaran Greek Souvlaki BBQ with Tzatziki and Greek Salad"
    },
    {
      "day": 4,
      "title": "The Minoan Pompeii: Akrotiri Prehistoric Ruins & Red Beach",
      "theme": "Bronze Age Civilizations",
      "locations": [
        "Akrotiri Archaeological Site",
        "Akrotiri Venetian Castle",
        "Red Beach Overlook",
        "Akrotiri Lighthouse"
      ],
      "morning": "09:00 - 12:30: Tour the covered archaeological excavation of Akrotiri, a sophisticated Minoan Bronze Age settlement preserved beneath volcanic ash from 1627 BC.",
      "afternoon": "13:30 - 16:30: Examine the monumental red cinder cliffs and maroon sand at Red Beach, then visit quiet Akrotiri village castle ruins.",
      "evening": "17:30 - 20:30: Drive to the southernmost tip of Santorini to watch the sunset from the solitary 1892 Akrotiri Lighthouse away from tourist crowds.",
      "culinary": "Tomato Gefthedes (Santorini Tomato Fritters) with fresh goat cheese"
    },
    {
      "day": 5,
      "title": "Medieval Pyrgos & Volcanic Wine Terroir Tastings",
      "theme": "Fortified Villages & Basket Vines",
      "locations": [
        "Pyrgos Kallistis Village",
        "Kasteli Fortress",
        "Profitis Ilias Monastery (567m)",
        "Santo Wines Winery"
      ],
      "morning": "09:30 - 12:30: Explore Pyrgos, Santorini's highest and best-preserved medieval village. Wander maze-like fortified alleys up to the Venetian Kasteli fortress.",
      "afternoon": "13:00 - 15:30: Ascend to the highest summit of the island at Profitis Ilias Monastery for 360-degree views of the entire crescent archipelago.",
      "evening": "16:30 - 21:00: Cliffside wine tasting at Santo Wines. Learn how grapes are cultivated in circular 'kouloura' baskets to shield them from relentless Aegean winds.",
      "culinary": "Six-Flight Volcanic Wine Tasting with Vinsanto and Greek Cheeses"
    },
    {
      "day": 6,
      "title": "Black Sand Shores: Perissa, Kamari & Ancient Thera",
      "theme": "Volcanic Beaches & Mountain Ruins",
      "locations": [
        "Perissa Black Sand Beach",
        "Mesa Vouno Mountain",
        "Ancient Thera Ruins",
        "Kamari Beachfront Promenade"
      ],
      "morning": "09:00 - 12:00: Relax on straw thatched sunbeds along the striking black volcanic pebbles of Perissa Beach beneath the towering sheer wall of Mesa Vouno.",
      "afternoon": "13:00 - 16:30: Drive or hike up the hairpin zig-zag road to Ancient Thera, a 9th-century BC hilltop Greek, Roman, and Byzantine city with agora colonnades overlooking the sea.",
      "evening": "17:30 - 21:00: Stroll the vibrant seaside promenade of Kamari lined with seafood tavernas, open-air cinema, and artisan jewelry stalls.",
      "culinary": "Grilled Calamari and Moussaka at a beachfront Kamari taverna"
    },
    {
      "day": 7,
      "title": "Megalochori Cave Cellars, Thirasia Island & Farewell Gala",
      "theme": "Authentic Santorini & Farewell Candlelight",
      "locations": [
        "Megalochori Village",
        "Bell Tower Arch",
        "Thirasia Island Escape",
        "Fine Dining in Oia"
      ],
      "morning": "09:30 - 12:30: Wander the tranquil whitewashed alleyways of Megalochori, admiring ornate pirate-era stone bell tower arches and visiting underground cave wine cellars.",
      "afternoon": "13:00 - 16:30: Take a quick wooden boat to Thirasia, the quiet island opposite Santorini that preserves the traditional Cycladic life untouched by modern tourism.",
      "evening": "18:30 - 22:30: Grand celebratory farewell dinner on a private cliffside terrace in Oia, savoring Michelin-inspired Aegean gastronomy under starlit skies.",
      "culinary": "Aegean Sea Bass with wild fennel and honey-drizzled Baklava"
    }
  ],
  "dubai": [
    {
      "day": 1,
      "title": "Record-Breaking Downtown: Burj Khalifa & Dubai Mall",
      "theme": "Sky-High Wonders & Choreographed Water",
      "locations": [
        "Burj Khalifa (At The Top Level 148)",
        "Dubai Mall",
        "Dubai Aquarium & Underwater Zoo",
        "Dubai Fountain Show"
      ],
      "morning": "09:30 - 12:30: Ascend the world's tallest building, Burj Khalifa, to the SKY deck on Level 148 (555m) for panoramic views across the Arabian Gulf, Sheikh Zayed Road, and the desert horizon.",
      "afternoon": "13:30 - 16:30: Tour the massive Dubai Mall. Walk through the 270-degree acrylic viewing tunnel of the Dubai Aquarium surrounded by sand tiger sharks and giant stingrays.",
      "evening": "17:30 - 21:30: Watch the illuminated Dubai Fountain show dance to Andrea Bocelli, followed by alfresco Lebanese dining on the terrace of Souk Al Bahar overlooking the lake.",
      "culinary": "Lebanese Grilled Mixed Grill & Mezze at Souk Al Bahar"
    },
    {
      "day": 2,
      "title": "Historic Old Dubai: Creek Abras, Gold Souk & Al Fahidi",
      "theme": "Heritage Alleys & Traditional Bazaars",
      "locations": [
        "Al Fahidi Historical Neighborhood",
        "Coffee Museum",
        "Dubai Creek Traditional Abra",
        "Spice & Gold Souks",
        "Al Seef"
      ],
      "morning": "09:00 - 12:30: Walk among traditional coral-stone wind-tower architecture in Al Fahidi Historical Quarter. Sample cardamom-infused Arabic coffee at the Coffee Museum.",
      "afternoon": "13:00 - 16:30: Board a traditional motorized wooden Abra boat across Dubai Creek for 1 AED. Explore sensory pyramids of saffron and frankincense in the Spice Souk and dazzling window displays in the Gold Souk.",
      "evening": "17:30 - 21:00: Dine along the revitalized waterfront boardwalk of Al Seef, watching traditional wooden dhows glide past against twilight.",
      "culinary": "Emirati Machboos spiced chicken rice & Luqaimat sweet date dumplings"
    },
    {
      "day": 3,
      "title": "Red Dune Desert Safari, Falconry & Bedouin Starlight",
      "theme": "Arabian Sands & Campfire Feasts",
      "locations": [
        "Lahbab Desert Red Dunes",
        "Sandboarding Slope",
        "Falconry Demonstration",
        "Bedouin Desert Camp"
      ],
      "morning": "10:00 - 13:00: Relax with morning spa treatments or poolside cabana leisure at your resort hotel.",
      "afternoon": "14:30 - 17:30: 4x4 Land Cruiser pickup for thrilling dune bashing over the towering crimson sands of the Lahbab Desert. Glide down high dunes on sandboards and photograph falcons.",
      "evening": "18:00 - 22:00: Arrive at a traditional desert fortress camp. Enjoy camel riding, henna artistry, charcoal-grilled barbecue banquet, and mesmerizing fire and Tanoura dance performances under starlight.",
      "culinary": "Charcoal-grilled Shish Tawook & Lamb Chops with freshly baked flatbreads"
    },
    {
      "day": 4,
      "title": "Palm Jumeirah Wonders & Luxury Marina Yacht Cruise",
      "theme": "Engineering Marvels & Bayside Luxury",
      "locations": [
        "The View at The Palm (Level 52)",
        "Atlantis The Palm",
        "The Pointe Boardwalk",
        "Dubai Marina Yacht Cruise"
      ],
      "morning": "09:30 - 12:30: Ride the Palm Monorail to The View at The Palm on Level 52 for a 360-degree vantage showing the entire palm-tree shaped archipelago, sea fronds, and outer crescent.",
      "afternoon": "13:30 - 16:30: Visit Atlantis The Palm, exploring the mysterious ruins of The Lost Chambers Aquarium housing 65,000 marine animals.",
      "evening": "17:00 - 20:30: Board a private luxury yacht from Dubai Marina, cruising past Jumeirah Beach Residence and Ain Dubai wheel as towering glass skyscrapers illuminate the night.",
      "culinary": "Mediterranean Seafood at Pier 7 Dubai Marina with skyline views"
    },
    {
      "day": 5,
      "title": "Museum of the Future, Dubai Frame & Neon Glow",
      "theme": "Futuristic Visions & Dual Perspectives",
      "locations": [
        "Museum of the Future (Killa Design)",
        "Dubai Frame (Zabeel Park)",
        "Dubai Garden Glow",
        "DIFC Fine Dining"
      ],
      "morning": "09:30 - 12:30: Marvel at the torus-shaped architectural masterpiece of the Museum of the Future adorned with Arabic calligraphy poetry. Tour immersive exhibits depicting the year 2071.",
      "afternoon": "13:30 - 16:30: Visit the 150-meter-tall golden Dubai Frame in Zabeel Park. Walk the luminous glass floor bridging historic Old Dubai on one side and gleaming New Dubai on the other.",
      "evening": "17:30 - 21:30: Walk through illuminated art installations at Dubai Garden Glow, followed by fine dining in Dubai International Financial Centre (DIFC).",
      "culinary": "Contemporary Japanese robata grill dining at Zuma DIFC"
    },
    {
      "day": 6,
      "title": "Grand Capital Excursion: Abu Dhabi & Sheikh Zayed Mosque",
      "theme": "Royal Marble & Cultural Domes",
      "locations": [
        "Sheikh Zayed Grand Mosque",
        "Louvre Abu Dhabi (Jean Nouvel)",
        "Emirates Palace",
        "Corniche"
      ],
      "morning": "08:30 - 12:30: Scenic 90-minute drive to Abu Dhabi to tour the majestic Sheikh Zayed Grand Mosque, with 82 white marble domes, reflective pools, and the world's largest hand-knotted carpet.",
      "afternoon": "13:30 - 16:30: Visit the Louvre Abu Dhabi on Saadiyat Island, marveling at Jean Nouvel's floating silvery dome creating a magical 'rain of light' over sea-filled galleries.",
      "evening": "17:30 - 21:00: Stop at the opulent Emirates Palace for gold-flaked Palace Cappuccino before returning to Dubai under the desert night sky.",
      "culinary": "Signature 24-Karat Gold Leaf Cappuccino at Emirates Palace"
    },
    {
      "day": 7,
      "title": "Burj Al Arab Glamour, Madinat Canals & Gala Farewell",
      "theme": "Sail-Shaped Luxury & Venetian Venice of the East",
      "locations": [
        "Jumeirah Public Beach",
        "Inside Burj Al Arab Tour",
        "Souk Madinat Jumeirah",
        "Skyview Bar"
      ],
      "morning": "09:30 - 12:30: Photograph the sail-shaped Burj Al Arab from Jumeirah Beach, then take the prestigious Inside Burj Al Arab guided tour through the 180m gold-leaf atrium and Royal Suite.",
      "afternoon": "13:30 - 16:30: Ride traditional wooden abra water taxis along the 3km tranquil turquoise canals of Souk Madinat Jumeirah, shopping for Arabian perfumes and silk pashminas.",
      "evening": "18:30 - 22:30: Gala farewell toast 200 meters above the sea at the Skyview Bar, enjoying multi-course gastronomic luxury overlooking the Arabian Gulf coastline.",
      "culinary": "Fine Dining Gala Dinner at Burj Al Arab with Gulf Seafood"
    }
  ]
}

def generate_custom_plan(city_name: str, days: int) -> List[Dict[str, Any]]:
    """Procedural generator for custom destinations with distinct landmarks per day."""
    custom_themes = [
        {
            "title": "Historic Heart, Ancient Towers & Old Town Square",
            "theme": "Old Town Heritage",
            "locations": [f"{city_name} Historic Core", f"{city_name} Cathedral / Citadel", f"{city_name} Old Town Square", f"{city_name} Clocktower & Panorama"],
            "morning": f"09:00 - 12:30: Explore {city_name} Old Town starting at the ancient Citadel and Grand Cathedral. Tour medieval bell towers and cobblestone artisan squares.",
            "afternoon": f"13:30 - 16:30: Guided walk through {city_name} historic trade guild halls and covered market passages, admiring classical architecture.",
            "evening": f"17:30 - 21:30: Sunset panoramic views from the central observation tower, followed by authentic regional dinner in a heritage tavern.",
            "culinary": f"Heritage Tasting Menu at historic {city_name} Old Town Inn"
        },
        {
            "title": "Imperial Arts, Royal Palaces & Riverfront Gardens",
            "theme": "Fine Arts & Architecture",
            "locations": [f"{city_name} National Art Museum", f"{city_name} Royal Palace & Formal Gardens", f"{city_name} Riverfront Promenade"],
            "morning": f"09:30 - 12:30: Guided discovery of master paintings and classical sculptures inside the prestigious {city_name} National Art Museum.",
            "afternoon": f"13:30 - 16:30: Stroll through the sculpted fountains and rose gardens of the Royal Palace estate, discovering historic staterooms.",
            "evening": f"17:30 - 21:00: Scenic evening promenade along the central riverfront, stopping at a historic café for artisanal pastries and aperitifs.",
            "culinary": f"Artisan Bistro Dining overlooking {city_name} River Promenade"
        },
        {
            "title": "Vibrant Quarters, Local Gastronomy & Sunset Heights",
            "theme": "Food Hall & Culture",
            "locations": [f"{city_name} Central Gourmet Market", f"{city_name} Artisan Crafts District", f"{city_name} Skyline Overlook"],
            "morning": f"08:30 - 12:00: Early morning gourmet safari through {city_name} Central Market. Sample farm-fresh artisanal cheeses, cured delicacies, and local breads.",
            "afternoon": f"13:00 - 16:30: Explore vibrant bohemian quarters filled with independent design ateliers, contemporary art galleries, and vintage bookstores.",
            "evening": f"17:30 - 21:30: Ascend to the highest natural lookout for golden hour vistas across {city_name}, followed by an authentic chef's wine-paired dinner.",
            "culinary": f"Market-fresh Seasonal Gastronomy & Regional Wine Tasting"
        },
        {
            "title": "Panoramic Nature Escapes & Valley Vistas",
            "theme": "Scenic Excursions",
            "locations": [f"{city_name} Scenic Funicular / Ridge", f"{city_name} Botanical Reserve", f"{city_name} Nature Sanctuary"],
            "morning": f"08:45 - 12:30: Cableway or scenic drive to the highest surrounding mountain ridge or coastline overlooking the greater {city_name} basin.",
            "afternoon": f"13:30 - 16:30: Easy hike through lush pine nature trails and protected botanical reserves, discovering hidden waterfalls and native wildlife.",
            "evening": f"17:30 - 20:30: Fireside dinner in a rustic mountainside or seaside lodge savoring slow-roasted specialties.",
            "culinary": f"Rustic Local Delicacies at {city_name} Scenic Mountain Lodge"
        },
        {
            "title": "Modern Horizons, Metropolis Skylines & Grand Farewell",
            "theme": "Modern Metropolis & Farewell Gala",
            "locations": [f"{city_name} Modern Financial District", f"{city_name} Contemporary Center", f"{city_name} Panoramic Rooftop"],
            "morning": f"10:00 - 12:30: Explore cutting-edge modern architecture, avant-garde design centers, and futuristic light-filled atriums.",
            "afternoon": f"13:30 - 17:00: Leisure luxury boutique shopping and museum exhibits in the cultural arts quarter.",
            "evening": f"18:30 - 22:30: Grand celebratory farewell banquet on an exclusive high-rise rooftop overlooking the shimmering city lights of {city_name}.",
            "culinary": f"Celebratory Farewell Gala Dinner with Skyline City Vistas"
        }
    ]

    plan = []
    for d in range(1, days + 1):
        tmpl = custom_themes[(d - 1) % len(custom_themes)]
        plan.append({
            "day": d,
            "title": tmpl["title"],
            "theme": tmpl["theme"],
            "locations": tmpl["locations"],
            "schedule": {
                "morning": tmpl["morning"],
                "afternoon": tmpl["afternoon"],
                "evening": tmpl["evening"]
            },
            "culinary": tmpl["culinary"]
        })
    return plan

def get_itinerary(dest_id: str, city_name: str, days: int) -> List[Dict[str, Any]]:
    """Retrieve distinct days for known curated hub or procedurally generate."""
    key = dest_id.lower().strip()
    raw = DESTINATION_ITINERARIES.get(key)
    
    if not raw:
        return generate_custom_plan(city_name, days)
        
    result = []
    for i in range(days):
        if i < len(raw):
            item = dict(raw[i])
            result.append({
                "day": i + 1,
                "title": item["title"],
                "theme": item["theme"],
                "locations": item["locations"],
                "schedule": {
                    "morning": item["morning"],
                    "afternoon": item["afternoon"],
                    "evening": item["evening"]
                },
                "culinary": item.get("culinary")
            })
        else:
            base = raw[i % len(raw)]
            result.append({
                "day": i + 1,
                "title": f"{base['title']} (Extended Discovery)",
                "theme": base["theme"],
                "locations": base["locations"],
                "schedule": {
                    "morning": base["morning"],
                    "afternoon": base["afternoon"],
                    "evening": base["evening"]
                },
                "culinary": base.get("culinary")
            })
    return result
