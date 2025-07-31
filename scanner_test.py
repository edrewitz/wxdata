from wxdata.utils.scanner import( 
    file_scanner, 
    url_scanner
)

model = "GEFS0p25"
cat = "Control"
proxies = None
step = 3

url, run = url_scanner(f"{model}", f"{cat}", proxies)
download = file_scanner(f"{model}", f"{cat}", url, run, step)