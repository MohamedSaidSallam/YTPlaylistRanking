# YTPlaylistRanking Usage Documentation

All of the following command line arguments can be accessed using

```bash
py -m YTPlaylistRanking -h

or

py -m YTPlaylistRanking --help
```

## Required Arguments

| Name  | Description | Ex  |
| ------------- |-------------| -----|
| id    | Playlist ID   | PL59FEE129ADFF2B12    |

## Optional Arguments

| Name  | Description | Default |
| ------------- |:-------------| -----|
|-h, --help|            show this help message and exit||
|-d, --debug|           write intermediate api responses to files|False|
|-vc, --viewCount|      Sort according to ViewCount(default)||
|-lc, --likeCount|      Sort according to Like Count||
|-dlc, --dislikeCount|  Sort according to Dislike Count||
|-ltvc, --likeToViewCount| Sort according to LikeToViewCount||
|-ltdlc, --likeToDislikeCount| Sort according to LikeToDislikeCount||
|-r, --reverse|         reverse the order of the list|False|
|-rn, --removeNumbering| remove numbering |False|
