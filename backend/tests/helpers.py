def parcel_geojson_payload(**props):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-5.03, 7.69], [-5.02, 7.69], [-5.02, 7.70], [-5.03, 7.70], [-5.03, 7.69],
            ]],
        },
        "properties": {
            "name": "Nouvelle parcelle",
            "crop_type": "maize",
            "health_status": "good",
            "soil_moisture": 60.0,
            **props,
        },
    }
