import requests

response = requests.get(f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/gefs.20250804/18/chem/pgrb2ap25/gefs.chem.t18z.a2d_0p25.f120.grib2", stream=True)

print(response.status_code)