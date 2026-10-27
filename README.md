# 🎬 Movie Recommender System

A content-based movie recommender. Pick a movie and the app shows 5 similar movies with their posters.

- **Dataset:** TMDB 5000 Movie Dataset (Kaggle)
- **Technique:** Bag-of-words (CountVectorizer) + cosine similarity
- **Features used to build tags:** overview, genres, keywords, top 3 cast, director
- **Frontend:** Streamlit
- **Posters:** TMDB API

## Project structure

```
movie-recommender/
├── app.py              # Streamlit web app
├── build_model.py      # Builds the model (.pkl files) from the data
├── test_tmdb.py        # Checks your TMDB key / internet access
├── requirements.txt
├── model/              # movie_list.pkl, similarity.pkl
└── data/               # CSV files (not included in the repo)
```

## How to run

1. Clone the repo and go into the folder.
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Get a free TMDB API key: https://www.themoviedb.org -> Settings -> API -> **API Key (v3 auth)**.
4. Put the key in `.streamlit/secrets.toml` (this file is never pushed to GitHub):
   ```toml
   TMDB_API_KEY = "your_key_here"
   ```
5. Start the app:
   ```
   streamlit run app.py
   ```

The `.pkl` files are already in the `model/` folder. To rebuild the model, download
`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from Kaggle, place them in `data/`,
and run `python build_model.py`.

## Note

TMDB is blocked by some ISPs (for example in India). If posters do not show up,
try a VPN (such as Cloudflare WARP) or a mobile hotspot. Run `python test_tmdb.py`
to check your connection.
