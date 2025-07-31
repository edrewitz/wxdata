from wxdata.soundings.wyoming_soundings import get_observed_sounding_data

df = get_observed_sounding_data(
    station_id="RIW"
)
print(df)