from ascii_earth import get_sun_vector, get_current_season, HIT, N_HIT, CELLS, get_surface_data
import json
from datetime import datetime, timezone

SUN_DATA = [
    # random dates
    datetime(2026, 1, 1, 1, 30, 0, 0, tzinfo=timezone.utc), 
    datetime(2026, 3, 6, 3, 10, 0, 0, tzinfo=timezone.utc),
    datetime(2026, 5, 12, 5, 21, 0, 0, tzinfo=timezone.utc),
    datetime(2026, 7, 18, 7, 59, 0, 0, tzinfo=timezone.utc),
    datetime(2026, 9, 24, 9, 0, 0, 0, tzinfo=timezone.utc),
    datetime(2026, 11, 30, 11, 15, 0, 0, tzinfo=timezone.utc),
    
    # solstice limit dates
    datetime(2026, 3, 20, 23, 59, 0, 0, tzinfo=timezone.utc), 
    datetime(2026, 3, 21, 0, 1, 0, 0, tzinfo=timezone.utc), # spring solstice
    datetime(2026, 6, 20, 5, 21, 0, 0, tzinfo=timezone.utc),
    datetime(2026, 6, 21, 23, 59, 0, 0, tzinfo=timezone.utc), # summer solstice
    datetime(2026, 9, 21, 9, 0, 0, 0, tzinfo=timezone.utc),
    datetime(2026, 9, 22, 5, 30, 0, 0, tzinfo=timezone.utc), # autumn solstice
    datetime(2026, 12, 20, 11, 15, 0, 0, tzinfo=timezone.utc),
    datetime(2026, 12, 21, 0, 0, 1, 0, tzinfo=timezone.utc), # winter solstice
    
]

SHADING_DATA = [
    #random data
    {"spin": 0.0, "tilt": 0.0, "date": datetime(2026, 1, 1, 1, 30, 0, 0, tzinfo=timezone.utc)},
    {"spin": 0.5, "tilt": 0.4, "date": datetime(2026, 1, 1, 1, 30, 0, 0, tzinfo=timezone.utc)},
    {"spin": 1.0, "tilt": 0.8, "date": datetime(2026, 1, 1, 1, 30, 0, 0, tzinfo=timezone.utc)},
    {"spin": -0.5, "tilt": 1.2, "date": datetime(2026, 1, 1, 1, 30, 0, 0, tzinfo=timezone.utc)},
    {"spin": -1.0, "tilt": 1.4, "date": datetime(2026, 1, 1, 1, 30, 0, 0, tzinfo=timezone.utc)},
    {"spin": -10.0, "tilt": -0.9, "date": datetime(2026, 1, 1, 1, 30, 0, 0, tzinfo=timezone.utc)}, # out of bounds spin
    {"spin": 4.0, "tilt": 0.3, "date": datetime(2026, 6, 20, 5, 21, 0, 0, tzinfo=timezone.utc)},
    {"spin": 10.0, "tilt": -0.5, "date": datetime(2026, 9, 21, 9, 0, 0, 0, tzinfo=timezone.utc)},
    {"spin": -10.0, "tilt": 0.9, "date": datetime(2026, 12, 20, 11, 15, 0, 0, tzinfo=timezone.utc)},
]

def sun():
    sun_vectors = []
    for d in SUN_DATA:
        sun_vectors.append({"date": d.isoformat(), "vector": get_sun_vector(d).tolist(), "season": get_current_season(d)})
    return sun_vectors

def geometry():
    return [{"hit": HIT[::5].tolist(), "n_hit": N_HIT[::50].tolist(), "cells": CELLS[::50].tolist()}]
    
def shading():
    shading_data = []
    for i in SHADING_DATA:
        land, lum = get_surface_data(i["spin"], i["tilt"], i["date"])
        shading_data.append({"spin": i["spin"], "tilt": i["tilt"], "date": i["date"].isoformat(), "land": land.tolist(), "lum": lum.tolist()})
    return shading_data

def main():
    fixture = {"sun": sun(), "geometry": geometry(), "shading": shading()}
    with open("data/fixtures.json", "w") as f:
        json.dump(fixture, f, indent=2)

if __name__ == "__main__":
    main()