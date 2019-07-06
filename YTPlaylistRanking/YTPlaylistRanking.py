import json
import os

from enum import Enum
from dotenv import load_dotenv
from pathlib import Path

from googleapiclient.discovery import build

load_dotenv()

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
API_KEY = os.environ.get("YT_DATA_API_V3")

FOLDER_NAME_OUTPUT = "output/"
FILE_NAME_PLAYLISTITEMS = FOLDER_NAME_OUTPUT + "playlistItems.json"
FILE_NAME_VIDEOS = FOLDER_NAME_OUTPUT + "videos.json"
FILE_NAME_OUTPUT = FOLDER_NAME_OUTPUT + "output.txt"

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
            return f"XXXX\t\tXXXX\t\tXXXX\t\t{self.videoId} {self.title}"
        else:
            return f"{self.viewCount}\t\t{self.likeCount}\t\t{self.dislikeCount}\t\t{self.videoId} {self.title}"


class SortType(Enum):
    ViewCount = lambda x:x.viewCount
    LikeCount= lambda x:x.likeCount
    DislikeCount= lambda x:x.dislikeCount
    LikeToViewCount= lambda x:x.likeCount / x.viewCount if x.viewCount != 0 else 0
    LikeToDislikeCount= lambda x:x.likeCount / x.dislikeCount if x.dislikeCount != 0 else x.likeCount


def main(playlistID, debug, sortTypes, reverse, removeNumbering):
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    playListResponse = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlistID,
        maxResults=50  # todo more than 50 results require multiple pages
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

    writeOutputToFile(entries, sortTypes, reverse, removeNumbering)


def writeOutputToFile(entries, sortTypes, reverse, removeNumbering):
    entries = [k for k in entries.values()]

    with open(FILE_NAME_OUTPUT, "w") as outputFile:
        for sortType in sortTypes:
                entries.sort(key=sortType, reverse=reverse)
                for enteryIndex, entery in enumerate(entries, 1):
                    outputFile.write(("" if removeNumbering else f"{enteryIndex}\t") + f"{entery}\n")
                outputFile.write("-" * 250 + "\n")