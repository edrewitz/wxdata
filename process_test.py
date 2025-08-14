from wxdata.preprocess.process import process_data

ds = process_data('gefs0p50', 'mean', 3, False)

print(ds)