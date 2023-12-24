from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import time
from geopy.exc import GeocoderTimedOut

def do_geocode(geolocator, address):
    try:
        return geolocator.geocode(address, addressdetails=True, timeout=100)
    except GeocoderTimedOut:
        time.sleep(1)
        return do_geocode(geolocator, address)

def get_district(address):
    geolocator = Nominatim(user_agent='new_geolocator')
    location = do_geocode(geolocator, f'{address} Warszawa')
    #location = geolocator.geocode(f'{address} Warszawa', addressdetails=True, timeout=None)
    time.sleep(1)
    if location:
        district = location.raw.get('address').get('suburb')
        subdistrict = location.raw.get('address').get('quarter')
        if location.raw.get('address').get('road') and location.raw.get('address').get('house_number'):
            street = f"{location.raw.get('address').get('road')} {location.raw.get('address').get('house_number')}"
        else:
            street = location.raw.get('address').get('road')
        neighbourhood = location.raw.get('address').get('neighbourhood')
        return street, neighbourhood, subdistrict, district
    return None, None, None, None

def fix_address(street, subdistrict, district):
    def get_first_non_null(*values):
        for value in values:
            if value is not None and not pd.isna(value) and not '':
                return value
        return None

    if pd.isna(street) or street == '' or street==np.nan:
        str1, nbhd1, subdist1, dist1 = get_district(subdistrict)
        str2, nbhd2, subdist2, dist2 = get_district(district)
        street_res = get_first_non_null(str1, str2)
        nbhd_res = get_first_non_null(nbhd1, nbhd2)
        subdist_res = get_first_non_null(subdist1, subdist2)
        dist_res = get_first_non_null(dist1, dist2)

        return street_res, nbhd_res, subdist_res, dist_res
    
    return get_district(street)