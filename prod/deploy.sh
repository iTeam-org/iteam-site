#!/bin/bash
#
# iTeam deployment script
#
# Deploys specified version of Zeste de Savoir
#
# Usage:
# - This script has exactly 1 parameter : the tag name to deploy

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <tag name>" >&2
    exit 1
fi

cd /opt/iteam-env/iteam-site/

# Maintenance mode
sudo rm /etc/nginx/sites-enabled/iteam
sudo ln -s /etc/nginx/sites-available/iteam-maintenance /etc/nginx/sites-enabled/iteam-maintenance
sudo service nginx reload

# Delete old branch if exists
git checkout prod
git branch -D $1
# Switch to new tag
git fetch --tags
# Server has git < 1.9, git fetch --tags doesn't retrieve commits...
git fetch
# Checkout the tag
git checkout $1
# Create a branch with the same name - required to have version data in footer
git checkout -b $1

# Update application data
source ../bin/activate
pip install --upgrade -r requirements.txt
python manage.py migrate
deactivate

# Restart iteam
sudo supervisorctl restart iteam

# Exit maintenance mode
sudo rm /etc/nginx/sites-enabled/iteam-maintenance
sudo ln -s /etc/nginx/sites-available/iteam /etc/nginx/sites-enabled/iteam
sudo service nginx reload

# Display current branch and commit
git status
echo "Commit deployé : `git rev-parse HEAD`"
