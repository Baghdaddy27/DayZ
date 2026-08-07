import json
import math
import os
import xml.etree.ElementTree as ET

# Configuration
JSON_PATH = "cfgeffectarea.json"
XML_PATH = "env/zombie_territories.xml" if os.path.exists("env/zombie_territories.xml") else "zombie_territories.xml"

# Buffer distance beyond the gas radius to search for nearby zones (in meters)
PROXIMITY_BUFFER = 150.0 

def analyze_nearby_territories():
    if not os.path.exists(JSON_PATH) or not os.path.exists(XML_PATH):
        print("Error: Input files not found. Check file paths.")
        return

    # 1. Load static gas zones from JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        effect_data = json.load(f)

    static_areas = []
    for area in effect_data.get("Areas", []):
        area_type = str(area.get("Type", ""))
        if "Static" in area_type or "ContaminatedArea_Static" in area_type:
            pos = area.get("Data", {}).get("Pos", [])
            radius = float(area.get("Data", {}).get("Radius", 0.0))

            if len(pos) >= 3:
                cx, cz = float(pos[0]), float(pos[2])
            elif len(pos) == 2:
                cx, cz = float(pos[0]), float(pos[1])
            else:
                continue

            static_areas.append({
                "name": area.get("AreaName", "Static Gas Zone"),
                "x": cx,
                "z": cz,
                "radius": radius
            })

    # 2. Parse zombie_territories.xml
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    print(f"Loaded {len(static_areas)} Static Gas Zone(s) from {JSON_PATH}.\n")

    # 3. Scan territories for proximity to each gas zone
    for gas in static_areas:
        print("=" * 65)
        print(f"GAS ZONE: '{gas['name']}'")
        print(f"Location: X={gas['x']:.1f}, Z={gas['z']:.1f} | Radius: {gas['radius']}m")
        print("=" * 65)

        matched_zones = []

        for territory in root.findall("territory"):
            territory_type = territory.attrib.get("type", "Unknown")

            for zone in territory.findall("zone"):
                zone_name = zone.attrib.get("name", "Unnamed Zone")
                try:
                    zx = float(zone.attrib["x"])
                    zz = float(zone.attrib["z"])
                    zr = float(zone.attrib.get("r", 0.0))
                except (KeyError, ValueError):
                    continue

                # Calculate distance between zone center and static gas center
                dist = math.hypot(zx - gas["x"], zz - gas["z"])
                max_search_dist = gas["radius"] + PROXIMITY_BUFFER

                if dist <= max_search_dist:
                    point_count = len(zone.findall("p"))
                    is_inside = dist <= gas["radius"]
                    matched_zones.append({
                        "territory_type": territory_type,
                        "zone_name": zone_name,
                        "x": zx,
                        "z": zz,
                        "radius": zr,
                        "dist": dist,
                        "is_inside": is_inside,
                        "points": point_count
                    })

        if not matched_zones:
            print("  -> No zombie territories found within or near this gas zone.\n")
        else:
            # Sort closest first
            matched_zones.sort(key=lambda z: z["dist"])

            for item in matched_zones:
                if item["is_inside"]:
                    status = "INSIDE GAS ZONE"
                else:
                    outside_by = item["dist"] - gas["radius"]
                    status = f"NEARBY ({outside_by:.1f}m outside gas perimeter)"

                print(f"  • Territory Type: {item['territory_type']}")
                print(f"    Zone Name:     '{item['zone_name']}'")
                print(f"    Zone Coords:   X={item['x']:.1f}, Z={item['z']:.1f} (Radius: {item['radius']}m)")
                print(f"    Spawn Points:  {item['points']} points inside zone")
                print(f"    Status:        {status} | Center Dist: {item['dist']:.1f}m")
                print()

if __name__ == "__main__":
    analyze_nearby_territories()