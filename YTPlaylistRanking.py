import json
import os
import argparse
from enum import Enum, auto
from dotenv import load_dotenv

from googleapiclient.discovery import build

load_dotenv()

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Gets statistics about videos in a Youtube playlist using the playlist's id to write to a file"
                     " the list of videos in ascending order according to a certain criteria (ex view count)."
                     "\nWarning: the output file is overwritten with each run!!"),
        epilog="https://github.com/TheDigitalPhoenixX/YTPlaylistRanking"
    )

    parser.add_argument("id", help="Playlist ID")
    parser.add_argument("-d", "--debug",
                        help="write intermediate api responses to files(default: false)",
                        action="store_true")

    parser.add_argument("-vc", "--viewCount", dest="sortTypes",
                        help="Sort according to ViewCount(default)",
                        action="append_const", const=SortType.ViewCount)
    parser.add_argument("-lc", "--likeCount", dest="sortTypes",
                        help="Sort according to Like Count",
                        action="append_const", const=SortType.LikeCount)
    parser.add_argument("-dlc", "--dislikeCount", dest="sortTypes",
                        help="Sort according to Dislike Count",
                        action="append_const", const=SortType.DislikeCount)
    parser.add_argument("-ltvc", "--likeToViewCount", dest="sortTypes",
                        help="Sort according to LikeToViewCount",
                        action="append_const", const=SortType.LikeToViewCount)
    parser.add_argument("-ltdlc", "--likeToDislikeCount", dest="sortTypes",
                        help="Sort according to LikeToDislikeCount",
                        action="append_const", const=SortType.LikeToDislikeCount)

    parser.add_argument("-r", "--reverse",
                        help="reverse the order of the list(default: false)",
                        action="store_false")
    parser.add_argument("-rn", "--removeNumbering",
                        help="remove numbering(default: false)",
                        action="store_true")

    args = parser.parse_args()
    main(args.id, args.debug, args.sortTypes if args.sortTypes != None else [SortType.ViewCount], args.reverse, args.removeNumbering)
