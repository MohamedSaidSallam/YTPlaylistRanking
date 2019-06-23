import json
import os

from googleapiclient.discovery import build

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
API_KEY = os.environ.get("YT_DATA_API_V3")

FILE_NAME_PLAYLISTITEMS = "playlistItems.json"
FILE_NAME_VIDEOS = "videos.json"
FILE_NAME_OUTPUT = "output.txt"

class Entry():
    videosIds = []
    
    def __init__(self, title, videoId):
        self.title = title
        self.videoId = videoId
        self.viewCount = 0
        self.likeCount = 0
        self.dislikeCount = 0
        self.none = True

        Entry.videosIds.append(videoId)

    def __str__(self):
        if self.none:
            return f"XXXX\tXXXX\tXXXX\t{self.videoId} {self.title}"
        else:
            return f"{self.viewCount}\t{self.likeCount}\t{self.dislikeCount}\t{self.videoId} {self.title}"


def main(playlistID, debug):
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    playListResponse = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlistID,
        maxResults=50 #todo more than 50 results require multiple pages
    ).execute()

    if debug:
        with open(FILE_NAME_PLAYLISTITEMS, "w") as outputFile:
            json.dump(playListResponse, outputFile)

    entries = {}
    for item in playListResponse["items"]:
        videoId = item["snippet"]["resourceId"]["videoId"]
        if videoId not in Entry.videosIds:
            entries[videoId] = Entry(item["snippet"]["title"], videoId)

    videosResponse = youtube.videos().list(
        part="statistics",
        id=",".join(Entry.videosIds)
    ).execute()

    if debug:
        with open(FILE_NAME_VIDEOS, "w") as outputFile:
            json.dump(videosResponse, outputFile)

    for video in videosResponse["items"]:
        stat = video["statistics"]

        entry = entries[video["id"]]
        entry.viewCount = int(stat["viewCount"])
        entry.likeCount = int(stat["likeCount"])
        entry.dislikeCount = int(stat["dislikeCount"])
        entry.none = False

    writeOutputToFile(entries)

def writeOutputToFile(entries):
    entries = [k for k in entries.values()]

    with open(FILE_NAME_OUTPUT, "w+") as outputFile:
        printVideos(entries,lambda x: x.viewCount, outputFile)
        printVideos(entries,lambda x: x.likeCount, outputFile)
        printVideos(entries,lambda x: x.dislikeCount, outputFile)
        printVideos(entries,lambda x: x.likeCount / x.viewCount if x.viewCount != 0 else 0, outputFile)
        printVideos(entries,lambda x: x.likeCount / x.dislikeCount if x.dislikeCount != 0 else x.likeCount, outputFile)
        
def printVideos(entries, key, outputFile):
    entries.sort(key=key, reverse=True)
    for enteryIndex, entery in enumerate(entries, 1):
        outputFile.write(f"{enteryIndex}\t{entery}\n")
    outputFile.write("-" *250 + "\n")

if __name__ == "__main__":
    main("PLEraF4t6Ap6RfBHrme4xztHZZBuwwivME", True)