import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import csv



url = 'https://www.youtube.com/playlist?list=PL11E57E1166929B60'
query = parse_qs(urlparse(url).query, keep_blank_values=True)
playlist_id = query["list"][0]
print(f'get all playlist items links from {playlist_id}')
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "YOUTUBE_DATA_API_KEY")

request = youtube.playlistItems().list(
    part = "snippet",
    playlistId = playlist_id,
    maxResults = 50
)
response = request.execute()

playlist_items = []

while request is not None and len(playlist_items)<451:
    response = request.execute()
    playlist_items += response["items"]
    request = youtube.playlistItems().list_next(request, response)

print(f"total: {len(playlist_items)}")

fieldnames = ['LINK', 'VIEWS','UPLOADDATE','COMMENTS','LIKES','DISLIKES']
file = open('Links.csv','w')
writer = csv.DictWriter(file, fieldnames=fieldnames)


init = 'https://www.youtube.com/watch?v='
writer.writeheader()
for t in playlist_items:
    link = (init + t["snippet"]["resourceId"]["videoId"])
    writer.writerow({"LINK":link})


