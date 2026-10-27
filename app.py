import os
import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")


def get_api_key():

    try:
        return st.secrets["TMDB_API_KEY"]
    except Exception:
        return os.getenv("TMDB_API_KEY", "")


TMDB_API_KEY = get_api_key()
PLACEHOLDER_POSTER = "https://placehold.co/500x750?text=No+Poster"

# TMDB's two official API domains. If one is blocked, the other is tried.
TMDB_HOSTS = ["https://api.themoviedb.org", "https://api.tmdb.org"]


@st.cache_resource
def load_model():
    movies = pickle.load(open("movie_list.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity


@st.cache_data(show_spinner=False, ttl=3600)
def _get_poster_url(movie_id):

    last_error = None
    for host in TMDB_HOSTS:
        try:
            response = requests.get(
                f"{host}/3/movie/{movie_id}",
                params={"api_key": TMDB_API_KEY, "language": "en-US"},
                timeout=5,
            )
            response.raise_for_status()
            poster_path = response.json().get("poster_path")
            if poster_path:  # some movies have no poster (None)
                return "https://image.tmdb.org/t/p/w500" + poster_path
            return PLACEHOLDER_POSTER
        except requests.RequestException as e:
            last_error = e
    raise last_error


def fetch_poster(movie_id):
    # If one poster already failed, skip the rest instead of waiting again
    if "poster_error" in st.session_state:
        return PLACEHOLDER_POSTER
    try:
        return _get_poster_url(int(movie_id))
    except requests.RequestException as e:
        st.session_state["poster_error"] = repr(e)
        return PLACEHOLDER_POSTER


def recommend(title, n=5):
    index = movies.index[movies["title"] == title][0]
    scores = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    names, posters = [], []
    for i, _ in scores[1: n + 1]:  # [0] is the selected movie itself, so skip it
        row = movies.iloc[i]
        names.append(row["title"])
        posters.append(fetch_poster(int(row["movie_id"])))
    return names, posters


# ------------------------------- UI -------------------------------
st.header("🎬 Movie Recommender System")

try:
    movies, similarity = load_model()
except FileNotFoundError:
    st.error("Model files not found in the model/ folder. Run `python build_model.py` first.")
    st.stop()

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown", movies["title"].values
)

if not TMDB_API_KEY:
    st.warning("TMDB API key not found. Add TMDB_API_KEY to .streamlit/secrets.toml (see README).")

if st.button("Show Recommendation"):
    st.session_state.pop("poster_error", None)
    names, posters = recommend(selected_movie)

    cols = st.columns(5)  # NOTE: older tutorials use st.beta_columns; it is now st.columns
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)

    if "poster_error" in st.session_state:
        st.error("Could not fetch posters from TMDB. Actual error: " + st.session_state["poster_error"])
        st.caption(
            "401 = invalid API key | ConnectionError / Timeout = TMDB is blocked on your "
            "network or ISP (try a VPN or a mobile hotspot)"
        )