# Contributing Guidelines

For those who would like to contribute to the WxData Project, please take note of the following guidelines. 

In order for your pull request to be accepted, you must comply with the following guidelines:

1) Your addition must work on VPN/PROXY server connections and allow users to pass in their PROXY settings. The `requests` package is recommended for this.
2) Your addition must have a scanner to prevent repetative downloads.
3) Your addition shall only download PUBLICLY available data. Nothing that requires API Keys or Passwords will be accepted.
4) Your addition must pre-process and post-process data.
5) Do not plagerize anyone else's work.
6) You are not allowed to use packages that are not available on BOTH Anaconda and PYPI (pip) (i.e. pygrib is not allowed and users must use xarray with cfgrib for post-processing)
    - This project must be available on PYPI in addition to Anaconda to maximize access for use.
7) The use of setup.py files is forbidden due to security vulerabilities associated with the use of setup.py. We use pyproject.toml for building our recipe. 
8) Be willing to accept feedback and constructive criticism.
9) Be respectful.
10) Have fun!
    
