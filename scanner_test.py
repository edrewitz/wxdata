from wxdata.scanners.url_scanners import( 
    gefs_url_scanner,
    rtma_url_scanner
)


model = "GEFS0P50 SECONDARY PARAMETERS"
#model = 'GEFS0P25'
cat = "Control"
proxies = None
step = 3
directory = 'chem'
final_forecast_hour = 240

url, run = gefs_url_scanner(model, cat, proxies, directory, final_forecast_hour, members=None)
#download = file_scanner(f"{model}", f"{cat}", url, run, step)

#url, file = rtma_url_scanner('rtma', 'forecast', None)

print(url)
