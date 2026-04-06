import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
)

sp = spotipy.Spotify(auth_manager=auth_manager)

# Genre and keyword mapping based on mood transition
MOOD_SEARCH_TERMS = {
    "sadness": {
        "calm":     "relaxing ambient peaceful",
        "focus":    "study focus instrumental",
        "energise": "upbeat motivational happy",
    },
    "anger": {
        "calm":     "calming meditation peaceful",
        "focus":    "deep focus concentration",
        "energise": "positive energy upbeat",
    },
    "fear": {
        "calm":     "soothing gentle calm",
        "focus":    "focus instrumental steady",
        "energise": "confidence boost upbeat",
    },
    "disgust": {
        "calm":     "peaceful relaxing soft",
        "focus":    "instrumental focus minimal",
        "energise": "happy feel good dance",
    },
    "joy": {
        "calm":     "chill mellow relaxed",
        "focus":    "lo-fi focus productive",
        "energise": "party dance high energy",
    },
    "surprise": {
        "calm":     "ambient relaxing soft",
        "focus":    "focus deep work",
        "energise": "energetic upbeat fun",
    },
    "neutral": {
        "calm":     "relaxing peaceful ambient",
        "focus":    "focus study instrumental",
        "energise": "upbeat energetic motivational",
    },
}


def get_recommendations(detected_emotion, target_mood, limit=8):
    """
    Searches Spotify for tracks matching the mood transition
    and returns a list of tracks.
    """
    try:
        emotion = detected_emotion.lower()
        target = target_mood.lower()

        if emotion not in MOOD_SEARCH_TERMS:
            emotion = "neutral"

        query = MOOD_SEARCH_TERMS[emotion][target]

        results = sp.search(q=query, type="track", limit=limit)

        tracks = []
        for track in results["tracks"]["items"]:
            tracks.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "uri": track["uri"],
                "url": track["external_urls"]["spotify"]
            })

        return tracks

    except spotipy.exceptions.SpotifyException as e:
        return {"error": f"Spotify API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}