# Smart Contact Extractor (Streamlit)
https://data-exctractor-9wa7sxs9g8umzmavhet9c5.streamlit.app/
A simple Streamlit app that extracts:

- Egyptian mobile numbers (matches `01[0125]` followed by 8 digits)
- Email addresses

## Run locally

```bash
pip install -r requirements.txt
streamlit run extractor_app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. In Streamlit Community Cloud, create a new app and select your repo.
3. Set **Main file path** to `extractor_app.py`.

