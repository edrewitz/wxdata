from wxdata.utils.scanner import( 
    file_scanner, 
    url_scanner
)

#model = "GFS0P25 SECONDARY PARAMETERS"
model = 'GEFS0P25'
cat = "Mean"
proxies = None
step = 3

url, run = url_scanner(f"{model}", f"{cat}", proxies, 'chem')
download = file_scanner(f"{model}", f"{cat}", url, run, step)