from flask import Flask, abort, jsonify
from config import my_pyrable as cfg

app = Flask(__name__)

def getIndex():
    return {
        "content": {
            "entries": [
                {
                    "id": ["frontiersmart", "directory", "radio"],
                    "title": cfg["name"],
                    "url": "https://airable.wifiradiofrontier.com/frontiersmart/x_streams"
                }
            ]
        },
        "id": ["airable", "listing", "index"],
        "title": "Index",
        "url": "https://airable.wifiradiofrontier.com/"
    }
    return datas

def formatStreams():
    stations = []
    for idx, stream in enumerate(cfg["stations"]):
        stations.append({
            "contains": ["feeds", "networks"],
            "id": ["frontiersmart", "radio", idx+1],
            "images": [stream["image"]],
            "title": stream["title"],
            "url": f"https://airable.wifiradiofrontier.com/frontiersmart/radio/{idx+1}"
        })
    return stations

def getStreams():
    return {
        "content": {
            "entries": formatStreams()
        },
        "id": ["airable", "listing", "index"],
        "description": cfg["description"],
        "id": ["frontiersmart", "network", "x_streams"],
        "images": [cfg["image"]],
        "slogan": cfg["slogan"],
        "title": cfg["name"],
        "url": "https://airable.wifiradiofrontier.com/frontiersmart/x_streams"
    }

def getLiveDetails(station_id):
    station = None
    if station_id <= len(cfg["stations"]):
        print(f"Station {station_id} found")
        station = cfg["stations"][station_id - 1]
    else:
        print(f"Station {station_id} not found")
        abort(404)

    return {
        "title": station["title"],
        "description": station["description"],
        "slogan": station["slogan"],
        "image": station["image"]
    }

def getRadioPlay(station_id, station):
    station = None
    if station_id <= len(cfg["stations"]):
        print(f"Station {station_id} found")
        station = cfg["stations"][station_id - 1]
    else:
        print(f"Station {station_id} not found")
        abort(404)
    live_details = getLiveDetails(station_id)

    return {
        "content": {
            "description": "NOT USED",
            "description": live_details["description"],
            "id": ["frontiersmart", "radio", station_id],
            "images": [live_details["image"]],
            "slogan": live_details["slogan"],
            "streams": [
                {
                    "id": ["frontiersmart", "stream", station_id],
                    # Can be wrong but it must be set to something
                    "codec": {
                        "bitrate": 96,
                        "name": "AAC"
                    },
                    # Useless but must be set
                    "reliability": 1,
                    # Not used ?
                    "title": "nya :3",
                    "url": f"https://airable.wifiradiofrontier.com/frontiersmart/radio/{station_id}/play"
                }
            ],
            "title": live_details["title"],
            "url": f"https://airable.wifiradiofrontier.com/frontiersmart/radio/{station_id}"
        },
        "id": ["frontiersmart", "redirect", station_id],
        "url": station["url"]
    }

def getRadio(station_id):
    station = None
    if station_id <= len(cfg["stations"]):
        print(f"Station {station_id} found")
        station = cfg["stations"][station_id - 1]
    else:
        print(f"Station {station_id} not found")
        abort(404)
    live_details = getLiveDetails(station_id)
    
    return {
        "content": {
            "entries": []
        },
        "description": live_details["description"],
        "id": ["frontiersmart", "radio", station_id],
        "images": [live_details["image"]],
        # this MUST exist
        "language": {
            "id": ["frontiersmart", "language", "7146148681174964"],
            "iso": "eng",
            "title": "English"
        },
        # this MUST exist
        "place": {
            "id": ["frontiersmart", "place", "4358624062035233"],
            "title": "London",
            "type": "city"
        },
        "slogan": live_details["slogan"],
        "streams": [
            {
                # This can be wrong
                "codec": {
                    "bitrate": 96,
                    "name": "AAC"
                },
                "id": ["frontiersmart", "stream", station_id],
                "reliability": 0.99,
                "title": "nya :3",
                "url": f"https://airable.wifiradiofrontier.com/frontiersmart/radio/{station_id}/play"
            }
        ],
        "title": live_details["title"],
        "url": f"https://airable.wifiradiofrontier.com/frontiersmart/radio/{station_id}"
    }

@app.route("/")
def hello():
    return jsonify(getIndex())

@app.route("/frontiersmart/x_streams")
def frontiersmart__x_streams():
    return jsonify(getStreams())

@app.route("/frontiersmart/radio/<int:station_id>/play")
def frontiersmart__radio__xxx__play(station_id):
    print(f"Station {station_id} requested to play")
    station = None
    if station_id <= len(cfg["stations"]):
        print(f"Station {station_id} found")
        station = cfg["stations"][station_id - 1]
    else:
        print(f"Station {station_id} not found")
        abort(404)
    return jsonify(getRadioPlay(station_id, station))

@app.route("/frontiersmart/radio/<int:station_id>")
def frontiersmart__radio(station_id):
    print(f"Station {station_id} requested")
    return jsonify(getRadio(station_id))

@app.route("/player/state")
def player__state():
    if cfg["fsapi"]["enabled"]:
        pass
        # get the fsapi thingy etc. https://github.com/Half-Shot/fairable/blob/main/lib/index.mjs#L33
    else:
        abort(404, "Feature not enabled\n")


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))