import json
from urllib.request import urlopen, Request
import csv
import urllib.error
import urllib.parse

api_key = 'YOUTUBE_DATA_API_KEY'
count = 0

class Youtube:
    def __init__(self):
        pass

    def get_video_id(self, link: str):
        link = link.split('=',1)[1]
        return link

    def store_data(self, url1, url2):

        self.data1 = urllib.request.urlopen(url1)
        self.jsonfile1 = json.loads(self.data1.read())
        header = {'User-Agent': 'Mozilla/5.0'}
        self.req = Request(url2, headers=header)
        self.data2 = urlopen(self.req)
        self.jsonfile2 = json.loads(self.data2.read())

        try:
            global count
            count += 1


            with open('Video_Statistics.csv', 'a', encoding='utf-8') as f:
                fieldnames = ['ID', 'Title', 'Upload_Date', 'Views', 'Likes', 'Dislikes', 'Comments']
                writer = csv.DictWriter(f, fieldnames, dialect='excel')
                writer.writerow({'ID': self.jsonfile1["items"][0]["id"],
                                 'Title': self.jsonfile2["items"][0]["snippet"]["title"],
                                 'Upload_Date': self.jsonfile2["items"][0]["snippet"]["publishedAt"],
                                 'Views': self.jsonfile1["items"][0]["statistics"]["viewCount"],
                                 'Likes': self.jsonfile1["items"][0]["statistics"]["likeCount"],
                                 'Dislikes': self.jsonfile1["items"][0]["statistics"]["dislikeCount"],
                                 'Comments': self.jsonfile1["items"][0]["statistics"]["commentCount"]})
        except KeyError as e:
            pass
        except urllib.error.HTTPError as u:
            pass
        except IndexError:
            pass


if __name__ == "__main__":

    youtube = Youtube()

    print('Index\tTitle\tUpload_Date\tViews\tLikes\tDislikes\tComments')
    with open('stats.csv','w') as f:
        header = ['Key', 'Title', 'Upload_Date', 'Views', 'Likes', 'Dislikes', 'Comments']
        writer = csv.writer(f)
        writer.writerow(header)
    f.close()

    with open('Links.csv','r') as file:
        vurl = file.readlines()

    for link in vurl:
        link = link.rstrip()
        video_id = youtube.get_video_id(link)
        params = {'part': 'snippet', 'id': f'{video_id}', 'key': 'AIzaSyAVtcurxxUyQznBtLU5UmxqrRSENZ6gAIA'}
        querystring = urllib.parse.urlencode(params)
        stats_url = 'https://www.googleapis.com/youtube/v3/videos' + '?' + querystring
        title_url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}'
        youtube.store_data(title_url, stats_url)




