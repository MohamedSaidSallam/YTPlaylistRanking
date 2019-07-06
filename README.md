# YouTube Playlist Ranking

As the name implies this script's purpose is to provide a ranking to videos in a YT playlist given it the playlist's id. Arranging the videos based on a certain criteria (Ex: view count).

## Getting Started

These instructions will help you run a project on your local machine.

### Prerequisites

This script requires Youtube Data API V3. Quick Start and installation can be found [here](https://developers.google.com/youtube/v3/quickstart/python).

Note that this script only uses the "Google APIs Client Library for Python". "google-auth-oauthlib" and "google-auth-httplib2" are not needed.

Pip install Command:

```shell
pip install --upgrade google-api-python-client
```

### Installing

* Obtain an API key for Youtube Data API V3.
* Duplicate the ".env.example" file.
* Paste the key inside the new file.
* Rename it to ".env".

### Usage Example

Full Usage Documentation can be found in [doc/YTPlaylistRanking.md](doc/YTPlaylistRanking.md).

#### Command

```bash
py -m YTPlaylistRanking PL59FEE129ADFF2B12
```

#### Output

Found in output/output.txt

```shell
1	284246284		1309028		44010		dsUXAEzaC3Q Michael Jackson - Bad (Shortened Version)
2	8047926		23983		1219		nnsSUqgkDwU Parisian Love
3	7037503		5392		985		BrXPcaRlBqo What is a browser?
4	5489860		7019		884		Hhgfz0zPmH4 Google Goggles
5	5488774		3327		850		xgrcK9Ozb_Q Cake
6	1033751		542		225		ZNbHGrGJu8Q Locking SafeSearch
7	956688		2960		336		EjN5avRvApk The Google Story
8	859495		3689		1599		oXHHkROejik Real Time Search Event
9	118045		233		68		EKuG2M6R4VM Personalized Search
10	XXXX		XXXX		XXXX		yi50KlsCBio Private video
------------------------------------------------------------------------------------------------------------------
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Thanks PurpleBooth for [README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2).
