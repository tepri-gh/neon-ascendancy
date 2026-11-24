#!/usr/bin/env python3
"""Generate curated, deterministic Neon Ascendancy world seed JSON files in data/.

Layout (96 control centers across 9 districts):
  - Watson (20): Little China (5), Kabuki (5), Northside (5), Arasaka Waterfront (5)
  - Westbrook (15): Japantown (5), Charter Hill (5), North Oak (5)
  - Heywood (15): Vista Del Rey (5), The Glen (5), Wellsprings (5)
  - Santo Domingo (10): Arroyo (5), Rancho Coronado (5)
  - Pacifica (10): Coastview (5), West Wind Estate (5)
  - City Center (10): Downtown (5), Corpo Plaza (5)
  - Badlands (10): 10 major named strongholds/landmarks across North & South Badlands
  - Dogtown (5): 5 iconic combat hubs (outside Stadium safe-market interior)
  - Morro Rock (1): Orbital Air NCX Spaceport

Every coordinate is grounded in extracted Cyberpunk 2077 2.5 streaming sector data
(dist/extract/areas.jsonl & dist/extract/markers.jsonl). Nearby extracted combat
communities from dist/extract/areas.jsonl are linked into data/spawn_points.json.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
AREAS_PATH = ROOT / "dist" / "extract" / "areas.jsonl"

DISTRICTS: list[dict[str, Any]] = [
    {
        "district_id": 1, "code": "watson", "display_name": "Watson", "kind": "city",
        "gamedata_district": "Watson", "crime_multiplier": 0.85,
        "bbox_min_x": -2450.0, "bbox_min_y": 900.0, "bbox_max_x": -305.0, "bbox_max_y": 3525.0,
        "vanilla_gangs": ["Maelstrom", "TygerClaws"],
    },
    {
        "district_id": 2, "code": "westbrook", "display_name": "Westbrook", "kind": "city",
        "gamedata_district": "Westbrook", "crime_multiplier": 0.85,
        "bbox_min_x": -1050.0, "bbox_min_y": -750.0, "bbox_max_x": 1095.0, "bbox_max_y": 2150.0,
        "vanilla_gangs": ["TheMox", "TygerClaws"],
    },
    {
        "district_id": 3, "code": "heywood", "display_name": "Heywood", "kind": "city",
        "gamedata_district": "Heywood", "crime_multiplier": 0.8,
        "bbox_min_x": -2795.0, "bbox_min_y": -1750.0, "bbox_max_x": -400.0, "bbox_max_y": -50.0,
        "vanilla_gangs": ["Valentinos"],
    },
    {
        "district_id": 4, "code": "santo_domingo", "display_name": "Santo Domingo", "kind": "city",
        "gamedata_district": "SantoDomingo", "crime_multiplier": 0.8,
        "bbox_min_x": -1060.0, "bbox_min_y": -2585.0, "bbox_max_x": 1585.0, "bbox_max_y": -565.0,
        "vanilla_gangs": ["SixthStreet"],
    },
    {
        "district_id": 5, "code": "pacifica", "display_name": "Pacifica", "kind": "city",
        "gamedata_district": "Pacifica", "crime_multiplier": 0.7,
        "bbox_min_x": -3225.0, "bbox_min_y": -3385.0, "bbox_max_x": -1120.0, "bbox_max_y": -1350.0,
        "vanilla_gangs": ["VoodooBoys", "Animals"],
    },
    {
        "district_id": 6, "code": "city_center", "display_name": "City Center", "kind": "city",
        "gamedata_district": "CityCenter", "crime_multiplier": 1.2,
        "bbox_min_x": -2395.0, "bbox_min_y": -350.0, "bbox_max_x": -900.0, "bbox_max_y": 750.0,
        "vanilla_gangs": [],
    },
    {
        "district_id": 7, "code": "badlands", "display_name": "Badlands", "kind": "badlands",
        "gamedata_district": "Badlands", "crime_multiplier": 1.0,
        "bbox_min_x": -6660.0, "bbox_min_y": -6655.0, "bbox_max_x": 6165.0, "bbox_max_y": 6265.0,
        "vanilla_gangs": ["Aldecaldos", "Wraiths"],
    },
    {
        "district_id": 8, "code": "dogtown", "display_name": "Dogtown", "kind": "dogtown",
        "gamedata_district": "Dogtown", "crime_multiplier": 1.0,
        "bbox_min_x": -2640.0, "bbox_min_y": -3245.0, "bbox_max_x": -1165.0, "bbox_max_y": -1770.0,
        "vanilla_gangs": ["Barghest"],
    },
    {
        "district_id": 9, "code": "morro_rock", "display_name": "Morro Rock", "kind": "city",
        "gamedata_district": "MorroRock", "crime_multiplier": 1.0,
        "bbox_min_x": -4800.0, "bbox_min_y": -400.0, "bbox_max_x": -2950.0, "bbox_max_y": 1150.0,
        "vanilla_gangs": [],
    },
]

# Tuple fields:
# (district_id, gamedata_subdistrict, code, display_name, x, y, z, owner_faction_id, owner_kind, income, defense, is_capital)
# Faction IDs from data/factions.json:
#  1=Maelstrom, 2=TygerClaws, 3=Valentinos, 4=SixthStreet, 5=VoodooBoys, 6=Animals,
#  7=Scavengers, 8=Wraiths, 9=Aldecaldos, 10=Barghest, 11=TheMox,
#  20=Arasaka, 21=Militech, 22=KangTao, 23=Biotechnica, 28=OrbitalAir
CURATED_ZONES: list[tuple[int, str, str, str, float, float, float, int, str, int, int, int]] = [
    # --- 1. Watson: Little China (5) ---
    (1, "LittleChina", "lch_dockside_yard",    "Little China Dockside Yard",    -1936.8,  1565.6,   8.6,  1, "gang", 760, 45, 0),
    (1, "LittleChina", "lch_goldsmith_plaza",  "Goldsmith Street Plaza",        -1689.8,  1431.3,  18.2,  1, "gang", 780, 50, 0),
    (1, "LittleChina", "lch_bradbury_market",  "Bradbury & Buran Market",       -1507.2,  1327.3,  23.7,  2, "gang", 820, 55, 1),
    (1, "LittleChina", "lch_farrier_alley",    "Farrier Street Alley",          -1642.3,  1233.6,  17.4,  2, "gang", 760, 45, 0),
    (1, "LittleChina", "lch_canal_overpass",   "Little China Canal Overpass",   -1279.3,  1593.3,  16.7,  2, "gang", 790, 50, 0),

    # --- 1. Watson: Kabuki (5) ---
    (1, "Kabuki", "kab_market_courtyard", "Kabuki Market Courtyard",            -1012.2,  1665.4,  18.2,  2, "gang", 830, 55, 0),
    (1, "Kabuki", "kab_pinewood_block",   "Pinewood Junction",                   -999.7,  2028.4,  43.8,  2, "gang", 770, 50, 0),
    (1, "Kabuki", "kab_allen_street",     "Allen Street Tenements",             -1114.2,  1202.5,  14.6,  2, "gang", 780, 45, 0),
    (1, "Kabuki", "kab_creek_loop",       "Creek Loop Warehouse",               -1178.5,  1947.5,  19.8, 11, "gang", 760, 45, 0),
    (1, "Kabuki", "kab_sutter_hill",      "Sutter Street Overlook",              -787.5,  1872.4,  50.4,  2, "gang", 750, 45, 0),

    # --- 1. Watson: Northside (5) ---
    (1, "Northside", "nid_all_foods_plant",     "All Foods Plant",               -791.9,  2207.5,  52.5,  1, "gang", 860, 70, 0),
    (1, "Northside", "nid_totentanz_yard",      "Totentanz Industrial Yard",    -1755.5,  2372.1,  17.7,  1, "gang", 810, 65, 0),
    (1, "Northside", "nid_martin_st_docks",     "Martin Street Depot",          -1162.1,  2419.5,   6.8,  1, "gang", 790, 60, 0),
    (1, "Northside", "nid_oil_refinery",        "Northside Oil Wharf",          -1115.6,  3314.7,   8.2,  7, "gang", 740, 55, 0),
    (1, "Northside", "nid_pershing_warehouses", "Pershing Street Warehouses",   -1373.1,  2780.7,   3.9,  1, "gang", 780, 55, 0),

    # --- 1. Watson: Arasaka Waterfront (5) ---
    (1, "ArasakaWaterfront", "awf_konpeki_approach",  "Konpeki Plaza Approach",     -2227.6, 1737.2, 19.0, 20, "corp", 1050, 85, 0),
    (1, "ArasakaWaterfront", "awf_ebunike_docks",     "Ebunike Container Docks",    -2155.7, 2875.2,  7.0,  1, "gang",  880, 65, 0),
    (1, "ArasakaWaterfront", "awf_north_pier",        "Arasaka North Cargo Pier",   -2274.6, 2761.6,  6.8, 20, "corp",  980, 75, 0),
    (1, "ArasakaWaterfront", "awf_central_terminal",  "Waterfront Freight Terminal",-2075.2, 2303.6, 18.3, 20, "corp",  960, 75, 0),
    (1, "ArasakaWaterfront", "awf_south_quay",        "Waterfront South Quay",      -2158.7, 1993.1, 18.2, 20, "corp",  950, 70, 0),

    # --- 2. Westbrook: Japantown (5) ---
    (2, "JapanTown", "jpn_cherry_blossom",    "Cherry Blossom Market",           -552.4,   501.6,  16.2,  2, "gang",  940, 65, 1),
    (2, "JapanTown", "jpn_silk_road",         "Silk Road West",                  -558.7,    90.2,  17.3,  2, "gang",  920, 60, 0),
    (2, "JapanTown", "jpn_sagan_terrace",     "Sagan & Diamond Terrace",         -209.2,  1011.3,  65.2,  2, "gang",  900, 55, 0),
    (2, "JapanTown", "jpn_crescent_alley",    "Crescent & Broad Alley",          -735.4,   880.9,  19.8,  2, "gang",  910, 55, 0),
    (2, "JapanTown", "jpn_fourth_wall_plaza", "Fourth Wall Plaza",               -299.3,  1411.9,  43.3,  2, "gang",  880, 50, 0),

    # --- 2. Westbrook: Charter Hill (5) ---
    (2, "CharterHill", "hil_gold_beach",        "Gold Beach Marina",              344.5,  -504.4,   6.1, 21, "corp", 1020, 70, 0),
    (2, "CharterHill", "hil_le_le_park",        "Lele Park Concourse",            -69.9,  -288.0,   7.2,  2, "gang",  940, 60, 0),
    (2, "CharterHill", "hil_power_plant",       "Charter Hill Substation",        572.4,  -455.0,   6.5, 20, "corp",  990, 65, 0),
    (2, "CharterHill", "hil_luxury_apartments", "Charter Hill Terraces",          354.2,  -217.2,  11.7, 20, "corp", 1040, 75, 0),
    (2, "CharterHill", "hil_longshore_canal",   "Charter Hill Canal Bridge",     -191.1,   139.8,  14.3,  2, "gang",  920, 55, 0),

    # --- 2. Westbrook: North Oak (5) ---
    (2, "NorthOaks", "nok_arasaka_estate",  "Arasaka Estate Gate",                320.8,  1054.3, 225.9, 20, "corp", 1120, 85, 0),
    (2, "NorthOaks", "nok_columbarium",     "North Oak Columbarium",              169.7,   542.0, 116.9, 20, "corp",  960, 60, 0),
    (2, "NorthOaks", "nok_sign_overlook",   "North Oak Hills Overlook",           279.4,   807.9, 146.4,  2, "gang",  930, 55, 0),
    (2, "NorthOaks", "nok_villa_ridge",     "North Oak Villa Ridge",              486.0,  1224.2, 229.3, 20, "corp", 1080, 75, 0),
    (2, "NorthOaks", "nok_north_canyon",    "North Oak Canyon Road",               34.6,  1605.1, 121.5,  2, "gang",  920, 60, 0),

    # --- 3. Heywood: Vista Del Rey (5) ---
    (3, "VistaDelRey", "rey_college_street", "College Street Tenements",         -813.7,  -381.4,   8.2,  3, "gang",  790, 55, 0),
    (3, "VistaDelRey", "rey_delamain_block", "Delamain Industrial Block",       -1101.3,  -186.6,   7.2,  3, "gang",  810, 50, 0),
    (3, "VistaDelRey", "rey_skyline_south",  "Skyline & Republic Yard",          -956.5,  -503.0,  17.7,  3, "gang",  780, 50, 0),
    (3, "VistaDelRey", "rey_east_canals",    "Vista East Canals",                -492.7,  -125.9,   7.9,  3, "gang",  760, 45, 0),
    (3, "VistaDelRey", "rey_la_catrina",     "La Catrina Crossing",              -957.8,  -784.4,   8.2,  3, "gang",  770, 50, 0),

    # --- 3. Heywood: The Glen (5) ---
    (3, "Glen", "gle_ventura_skyline",    "Ventura & Skyline",                  -1634.8, -1234.6,  24.5,  3, "gang",  850, 60, 1),
    (3, "Glen", "gle_hanford_overpass",   "Hanford Overpass",                   -1413.6, -1213.1,  26.7, 22, "corp",  880, 60, 0),
    (3, "Glen", "gle_reconciliation_park","Reconciliation Park West",           -1974.2, -1031.2,   7.3,  3, "gang",  820, 50, 0),
    (3, "Glen", "gle_senate_market",      "Senate & Market Plaza",              -1246.9,  -942.3,  31.1,  4, "gang",  800, 50, 0),
    (3, "Glen", "gle_embers_promenade",   "Glen Canal Promenade",               -1454.1,  -521.9,   7.5,  3, "gang",  840, 55, 0),

    # --- 3. Heywood: Wellsprings (5) ---
    (3, "Wellsprings", "spr_pump_station",    "Wellsprings Pump Station",       -2047.9, -1308.9,   7.3,  6, "gang",  780, 55, 0),
    (3, "Wellsprings", "spr_palm_view",       "Palm View Plaza",                -2203.8,  -978.0,  35.8,  3, "gang",  800, 50, 0),
    (3, "Wellsprings", "spr_boardwalk_north", "Wellsprings North Pier",         -2049.8,  -192.7,   8.0,  3, "gang",  790, 50, 0),
    (3, "Wellsprings", "spr_cannery_plaza",   "Cannery Row Promenade",          -2462.7,  -832.5,  12.6,  3, "gang",  770, 45, 0),
    (3, "Wellsprings", "spr_berkeley_bay",    "Berkeley & Bay Yard",            -2259.5,  -630.4,   7.1,  3, "gang",  780, 45, 0),

    # --- 4. Santo Domingo: Arroyo (5) ---
    (4, "Arroyo", "arr_arasaka_industrial", "Arasaka Industrial Park",           -513.2, -1552.9,   6.6, 20, "corp",  960, 80, 1),
    (4, "Arroyo", "arr_petrochem_yard",     "Petrochem Freight Yard",            -255.9, -1480.0,   7.6, 20, "corp",  900, 70, 0),
    (4, "Arroyo", "arr_kendachi_plant",     "Kendachi Foundry",                  -605.0, -1037.5,   6.7,  4, "gang",  820, 60, 0),
    (4, "Arroyo", "arr_megabuilding_h4",    "Megabuilding H4 Plaza",             -951.7, -1502.8,  25.6,  4, "gang",  790, 55, 0),
    (4, "Arroyo", "arr_red_dirt_cross",     "Red Dirt Crossroads",               -884.3, -1009.7,  11.6,  4, "gang",  780, 55, 0),

    # --- 4. Santo Domingo: Rancho Coronado (5) ---
    (4, "RanchoCoronado", "rcr_mallagra_depot",  "Mallagra & Manzanita Depot",    802.6, -1561.6,  47.4,  4, "gang",  770, 60, 0),
    (4, "RanchoCoronado", "rcr_almunecar_strip", "Almunecar Highway Strip",      -159.2, -2184.7,   5.4,  4, "gang",  760, 55, 0),
    (4, "RanchoCoronado", "rcr_tama_viewpoint",  "Rancho East Ridge",             998.3,  -848.0,  29.3,  4, "gang",  740, 50, 0),
    (4, "RanchoCoronado", "rcr_piez_plaza",      "Rancho South Market",           201.6, -2082.3,  17.5,  4, "gang",  760, 50, 0),
    (4, "RanchoCoronado", "rcr_kendal_park",     "Kendal Park Courts",            531.6,  -954.9,  28.6,  4, "gang",  750, 50, 0),

    # --- 5. Pacifica: Coastview (5) ---
    (5, "Coastview", "cvi_grand_imperial_mall", "Grand Imperial Mall",          -2331.9, -2042.5,  11.0,  6, "gang",  680, 65, 1),
    (5, "Coastview", "cvi_pacifica_pier",       "Pacifica Pier Boardwalk",      -2476.1, -2176.9,  15.7,  7, "gang",  620, 55, 0),
    (5, "Coastview", "cvi_east_overpass",       "Coastview East Overpass",      -1213.7, -1728.0,  44.2,  6, "gang",  610, 50, 0),
    (5, "Coastview", "cvi_rollercoaster_beach", "Coastview Amusement Strip",    -2015.1, -1860.7,  18.0,  5, "gang",  640, 55, 0),
    (5, "Coastview", "cvi_south_boulevard",     "Coastview South Boulevard",    -1975.7, -2173.1,  24.3,  5, "gang",  630, 55, 0),

    # --- 5. Pacifica: West Wind Estate (5) ---
    (5, "WestWindEstate", "wwd_apartments_north",  "West Wind North Towers",    -2893.7, -2160.9,   8.0,  7, "gang",  560, 45, 0),
    (5, "WestWindEstate", "wwd_central_courtyard", "West Wind Central Plaza",   -2758.2, -2466.5,  17.3,  7, "gang",  590, 55, 0),
    (5, "WestWindEstate", "wwd_south_projects",    "West Wind South Projects",  -2811.9, -2690.0,  23.4,  7, "gang",  570, 50, 0),
    (5, "WestWindEstate", "wwd_coastline_ruins",   "West Wind Coastal Ruins",   -2573.3, -2422.8,  43.0,  5, "gang",  580, 50, 0),
    (5, "WestWindEstate", "wwd_highway_gate",      "West Wind South Highway",   -2465.3, -2883.6,  43.1,  6, "gang",  560, 45, 0),

    # --- 6. City Center: Downtown (5) ---
    (6, "Downtown", "dtn_skyline_west",      "Skyline & Salinas Plaza",         -1726.1,   508.9,   7.2, 21, "corp", 1180, 75, 0),
    (6, "Downtown", "dtn_goldsmith_dock",    "Downtown West Pier",              -2164.5,   594.7,   6.6, 21, "corp", 1160, 75, 0),
    (6, "Downtown", "dtn_corporation_st",    "Corporation Street Arcade",       -1667.2,   248.7,   8.0,  2, "gang", 1140, 70, 0),
    (6, "Downtown", "dtn_south_waterfront",  "Downtown South Quay",             -2243.0,   -26.9,   8.9,  3, "gang", 1120, 65, 0),
    (6, "Downtown", "dtn_central_concourse", "Downtown Central Concourse",      -2147.3,   273.2,   7.5, 23, "corp", 1170, 70, 0),

    # --- 6. City Center: Corpo Plaza (5) ---
    (6, "CorpoPlaza", "cpz_arasaka_plaza",    "Arasaka Tower Plaza",            -1445.8,   130.7,  15.3, 20, "corp", 1350, 95, 1),
    (6, "CorpoPlaza", "cpz_militech_hq",      "Militech HQ Concourse",          -1307.3,   -55.0,   7.0, 21, "corp", 1300, 90, 0),
    (6, "CorpoPlaza", "cpz_kang_tao_sector",  "Kang Tao North Tower",           -1118.2,   554.1,  18.6, 22, "corp", 1250, 85, 0),
    (6, "CorpoPlaza", "cpz_ring_road_west",   "Memorial Ring West",             -1665.0,    23.0,  14.7, 20, "corp", 1220, 80, 0),
    (6, "CorpoPlaza", "cpz_ring_road_north",  "Corpo Plaza North Overpass",     -1283.1,   344.3,  10.3, 21, "corp", 1240, 80, 0),

    # --- 7. Badlands (10 major named strongholds & strategic landmarks) ---
    (7, "Badlands", "bls_sunset_motel",      "Sunset Motel",                     1634.2,  -738.7,  49.8,  8, "gang",  660, 55, 0),
    (7, "Badlands", "bls_rocky_ridge",       "Rocky Ridge Ghost Town",           2556.9,   -23.9,  82.1,  8, "gang",  680, 60, 0),
    (7, "Badlands", "bls_aldecaldos_camp",   "Aldecaldos Nomad Camp",            3412.9,  -360.1, 120.3,  9, "gang",  720, 70, 1),
    (7, "Badlands", "bls_wraith_compound",   "Wraiths Badlands Compound",        3003.6, -2394.3, 118.5,  8, "gang",  740, 80, 0),
    (7, "Badlands", "bls_militech_outpost",  "Red Peaks Militech Outpost",       3646.4,  -920.5, 120.5, 21, "corp",  780, 80, 0),
    (7, "Badlands", "bls_north_oil_fields",  "North Sunrise Oil Fields",        -1835.7,  3719.3,   6.7, 21, "corp",  760, 70, 0),
    (7, "Badlands", "bls_canyon_depot",      "Badlands Canyon Depot",            2020.5,  2830.5, 109.7, 21, "corp",  790, 80, 0),
    (7, "Badlands", "bls_biotechnica_flats", "Biotechnica Protein Flats",       -1809.5, -4283.5,  74.1, 23, "corp",  820, 75, 0),
    (7, "Badlands", "bls_solar_station",     "Jackson Plains Solar Arrays",        50.4, -5595.4, 212.8, 21, "corp",  840, 85, 0),
    (7, "Badlands", "bls_border_crossing",   "SoCal Border Checkpoint",         -2810.0, -5435.2,  96.8, 21, "corp",  860, 90, 0),

    # --- 8. Dogtown (5 iconic combat hubs, outside Stadium safe-market interior) ---
    (8, "Dogtown", "dt_main_gate",        "Dogtown Checkpoint Gate",            -2062.2, -2310.4,  19.0, 10, "gang", 1050, 85, 0),
    (8, "Dogtown", "dt_black_sapphire",   "Black Sapphire Plaza",               -1928.5, -2313.6,  44.4, 10, "gang", 1150, 95, 1),
    (8, "Dogtown", "dt_longshore_stacks", "Longshore Stacks",                   -2319.8, -2544.0,  17.0, 10, "gang", 1020, 80, 0),
    (8, "Dogtown", "dt_terra_cognita",    "Terra Cognita Ruins",                -1664.4, -2753.0, 103.0,  5, "gang", 1000, 80, 0),
    (8, "Dogtown", "dt_luxor_heights",    "Luxor High Wellness Spa",            -2134.3, -2692.7,  78.6, 10, "gang", 1040, 85, 0),

    # --- 9. Morro Rock (1 Spaceport control center) ---
    (9, "MorroRock", "morro_ncx_spaceport", "Orbital Air NCX Spaceport",        -3562.8,   390.3,  31.8, 28, "corp", 1450, 95, 1),
]


def write_json(name: str, obj: Any) -> None:
    path = DATA_DIR / name
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    factions = json.loads((DATA_DIR / "factions.json").read_text(encoding="utf-8"))
    fac_by_code = {f["code"]: f["faction_id"] for f in factions}
    dist_by_id = {d["district_id"]: d for d in DISTRICTS}

    sub_territories: list[dict[str, Any]] = []
    landmarks: list[dict[str, Any]] = []
    control_centers: list[dict[str, Any]] = []

    for idx, row in enumerate(CURATED_ZONES, start=1):
        (did, subdist, code, name, x, y, z, owner_id, owner_kind, income, defense, is_cap) = row
        d = dist_by_id[did]
        if not (d["bbox_min_x"] <= x <= d["bbox_max_x"] and d["bbox_min_y"] <= y <= d["bbox_max_y"]):
            raise ValueError(f"{code} ({x}, {y}) outside district {d['code']} bbox!")

        sub_territories.append({
            "sub_territory_id": idx,
            "district_id": did,
            "code": code,
            "display_name": name,
            "gamedata_subdistrict": subdist,
            "owner_kind": owner_kind,
            "initial_owner_faction_id": owner_id,
            "claim_strength": 2.0 if owner_kind == "corp" else 1.0,
            "base_income_per_cycle": income,
            "defense_rating": defense,
            "centroid_x": round(x, 3),
            "centroid_y": round(y, 3),
            "centroid_z": round(z, 3),
        })
        landmarks.append({
            "landmark_id": idx,
            "code": f"lm_{code}",
            "display_name": name,
            "kind": "compound" if owner_kind == "corp" else "hq",
            "sub_territory_id": idx,
            "gamedata_district": subdist,
            "x": round(x, 3),
            "y": round(y, 3),
            "z": round(z, 3),
            "purchasable": 0,
            "base_price": None,
        })
        control_centers.append({
            "control_center_id": idx,
            "sub_territory_id": idx,
            "code": f"cc_{code}",
            "display_name": name,
            "landmark_id": idx,
            "x": round(x, 3),
            "y": round(y, 3),
            "z": round(z, 3),
            "capture_radius_m": 45.0,
            "is_capital": is_cap,
        })

    # Link real extracted combat community areas from dist/extract/areas.jsonl to nearest control center.
    spawn_points: list[dict[str, Any]] = []
    if AREAS_PATH.is_file():
        areas = [json.loads(line) for line in AREAS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
        # Map each area to nearest control center within 450m (1200m in Badlands/Morro Rock).
        sp_id = 1
        seen_hashes: set[tuple[int, str]] = set()
        for a in sorted(areas, key=lambda r: (r["debug_name"], r["x"], r["y"])):
            aff = a.get("dominant_faction")
            if not aff or aff not in fac_by_code:
                continue
            if (a.get("affiliated_count") or 0) <= 0:
                continue
            ax, ay, az = float(a["x"]), float(a["y"]), float(a["z"])
            best_cc = None
            best_d2 = float("inf")
            for cc in control_centers:
                dx, dy = ax - cc["x"], ay - cc["y"]
                d2 = dx * dx + dy * dy
                if d2 < best_d2:
                    best_d2 = d2
                    best_cc = cc
            if best_cc is None:
                continue
            st = sub_territories[best_cc["sub_territory_id"] - 1]
            max_r = 1200.0 if st["district_id"] in (7, 9) else 450.0
            if best_d2 > max_r * max_r:
                continue
            chash = str(a.get("community_hash") or a["debug_name"])
            key = (best_cc["control_center_id"], chash)
            if key in seen_hashes:
                continue
            seen_hashes.add(key)
            spawn_points.append({
                "spawn_point_id": sp_id,
                "control_center_id": best_cc["control_center_id"],
                "sub_territory_id": best_cc["sub_territory_id"],
                "faction_id": fac_by_code[aff],
                "encounter_type": "community",
                "community_hash": chash,
                "community_template": a["debug_name"],
                "x": round(ax, 3),
                "y": round(ay, 3),
                "z": round(az, 3),
                "yaw": None,
                "spawn_weight": min(200, max(50, int(a["affiliated_count"]) * 15)),
                "min_era": "dogtown" if st["district_id"] == 8 else "any",
                "max_era": "any",
            })
            sp_id += 1

    write_json("districts.json", DISTRICTS)
    write_json("sub_territories.json", sub_territories)
    write_json("landmarks.json", landmarks)
    write_json("control_centers.json", control_centers)
    write_json("spawn_points.json", spawn_points)

    manifest = json.loads((DATA_DIR / "MANIFEST.json").read_text(encoding="utf-8"))
    manifest["counts"] = {
        "districts": len(DISTRICTS),
        "factions": len(factions),
        "sub_territories": len(sub_territories),
        "control_centers": len(control_centers),
        "landmarks": len(landmarks),
        "spawn_points": len(spawn_points),
    }
    write_json("MANIFEST.json", manifest)

    print(
        f"Generated seeds OK: {len(DISTRICTS)} districts, {len(sub_territories)} sub_territories/control_centers, "
        f"{len(spawn_points)} spawn_points"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
