import requests as http



from requests import Response
def geo_location(ip)-> none:
    Response=http.get("https://ipinfo.io/"+ip+"/json")
    if Response.status_code == 200:
        print(Response.json())
if__name__=='__main__':
print(geo_location("88.147.152.239"))
