
import http.client
import json
import time
import sys
import collections
import requests
import csv

key = input("\n\nPress your API key.")

conn = http.client.HTTPSConnection("api.themoviedb.org", timeout=10)

payload = "{}"

report = ' '
for page in range (0,20):
    ##Here we should use at least (1,5) once the timeout problem is fixed.
    conn.request("GET", "/3/discover/movie?with_genres=18&primary_release_date.gte=2014&page="+str(page)+"&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key="+key, payload)
    
    res = conn.getresponse()
    
    data = res.read()
    
    report = report + data.decode("utf-8")

id = ""
name = ""
line_item=""
id_total = []
total = []
n=0

for line in report.split("},{"):
    if n<350:
        id = line.split("id")[1].split(',')[0].split(':')[1]
        name = line.split("title")[1].split("popularity")[0].split("\"")[2]
        line_item = id+","+name
        id_total.append(id)
        total.append(line_item)
        n=n+1

print(n)

with open('movie_ID_name.csv', mode='w') as f:
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for movie in total:
        w.writerow([movie])



with open('movie_ID_similar.csv', mode='w') as e:
    w = csv.writer(e, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for movie_id in id_total:
        similar = ' '
        id_list = []
        #if m<3:
        conn.request("GET", "/3/movie/"+movie_id+"/similar?page=1&language=en-US&api_key="+key, payload)
        
        res = conn.getresponse()
        data = res.read()
        similar = data.decode("utf-8")
        
        
        #k=0
        #print("\n This is the similar movies for "+movie_id)
        if "id\":" in similar:
            similar_total = []
            for line in similar.split("},{"):
                id = line.split("id\":")[1].split(',')[0]
                id_list.append(id)
            if len(id_list)>5:
                id_list = id_list[0:5]
            for j in id_list:
                if j<movie_id and (j in id_total):
                    id_list.remove(j)
            for similar_each in id_list:
                similar_total.append(movie_id + "," + similar_each)
    
        
        
        for write_each in similar_total:
            w.writerow([write_each])

