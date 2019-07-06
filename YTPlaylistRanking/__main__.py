from YTPlaylistRanking.YTPlaylistRanking import SortType, main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Gets statistics about videos in a YouTube playlist using the playlist's id to write to a file"
                     " the list of videos in ascending order according to a certain criteria (ex view count)."
                     "\nWarning: the output file is overwritten with each run!!"),
        epilog="https://github.com/TheDigitalPhoenixX/YTPlaylistRanking"
    )

    parser.add_argument("id", help="Playlist ID")
    parser.add_argument("-d", "--debug",
                        help="write intermediate api responses to files(default: %(default)s)",
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
                        help="reverse the order of the list(default: %(default)s)",
                        action="store_true")
    parser.add_argument("-rn", "--removeNumbering",
                        help="remove numbering(default: %(default)s)",
                        action="store_true")

    args = parser.parse_args()
    main(args.id, args.debug, args.sortTypes if args.sortTypes != None else [SortType.ViewCount],
     not args.reverse, args.removeNumbering)
