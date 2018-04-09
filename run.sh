#/bin/sh

# download data
curl https://www.fda.gov/downloads/Drugs/InformationOnDrugs/UCM163762.zip > dl.zip
unzip dl.zip -d raw

# create postgres DB
db="fda_orange"
dropdb $db --if-exists
createdb $db

# insert data
./insert.py $db
