
import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
  print("ERROR: User is running a version of Python older than Python 3\nTo use FireWxPy, the user must be using Python 3 or newer.")

setup(
    name = "wxdata",
    version = "1.0",
    packages = find_packages(),
    install_requires=[
        "metpy>=1.5.1",
        "numpy>=1.24",
        "pandas>=2.2",
        "xarray>=2023.1.0",
        "netcdf4>=1.7.1",
        "cartopy>=0.21.0",
        "beautifulsoup4>=4.13.4",
        "requests>=2.32.4",
        "cfgrib>=0.9.10.4"
      
    ],
    author="Eric J. Drewitz",
    description="An open source library for downloading and pre-processing various types of weather data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"

)
