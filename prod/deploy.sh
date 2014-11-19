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
sudo ln -s /etc/nginx/sites-available/iteam-maintenance /etc/nginx/sites-enabled/iteam
sudo service nginx reload

# save database if something fail
cp ../db.sqlite3 ../db.sqlite3_$(date +"%F_%R:%S")

# Delete old branch if exists
git branch -D $1
# Switch to new tag (Server has git < 1.9, git fetch --tags doesn't retrieve commits...)
git fetch --tags
git fetch
# Checkout the tag
git checkout $1

# compute front stuff
compass compile assets/

# Update application data
source ../bin/activate
pip install --upgrade -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
deactivate

# Restart iteam
sudo supervisorctl restart iteam

# Exit maintenance mode
sudo rm /etc/nginx/sites-enabled/iteam
sudo ln -s /etc/nginx/sites-available/iteam-prod /etc/nginx/sites-enabled/iteam
sudo service nginx reload

# Display current branch and commit
DEPLOYED_HASH=$(git show-ref --tags | grep $1 | cut -d " " -f 1)
DEPLOYED_TAG=$(git show-ref --tags | grep $1 | cut -d " " -f 2 | cut -d "/" -f 3)
HEAD_HASH=$(git rev-parse HEAD)

echo "$DEPLOYED_TAG" > git_version.txt

echo "Commit deployé :"
echo "tag  - $DEPLOYED_TAG"
echo "hash - $DEPLOYED_HASH"
echo "head - $HEAD_HASH"
