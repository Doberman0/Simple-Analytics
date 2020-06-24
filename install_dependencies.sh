
#!/bin/bash
# Run this script to install dependencies. This only works on Linux systems obviously.
# I assume you have pip3 installed.

# install virtualenv
eval "pip3 install virtualenv"

# install flask
eval "virtualenv flask"
eval "flask/bin/pip3 install flask"

# install requests
eval "flask/bin/pip3 install pandas"