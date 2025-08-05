from wxdata.utils.scanner import( 
    file_scanner, 
    url_scanner
)

model = "GFS0P25"
#model = 'GEFS0P25'
cat = "Spread"
proxies = None
step = 3

url, run = url_scanner(f"{model}", f"{cat}", proxies, 'atmos')
download = file_scanner(f"{model}", f"{cat}", url, run, step)