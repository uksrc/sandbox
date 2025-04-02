import pyvo as vo
import requests
import os

url_tap = "http://localhost:8080/tap"
service = vo.dal.TAPService(url_tap)
obs_id = 'TS8004_C_001_20190801'
uuid_query = "SELECT id FROM Observation WHERE uri="+"'"+obs_id+"'"
resultset = service.search(uuid_query)

if len(resultset) > 1:
    print("Duplicate Records found:")
    for row in resultset:
        print(row['id'])
elif len(resultset) == 1:
    print(resultset[0]['id'])
else:
    print("No existing record found for" + obs_id)

