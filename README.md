# Songs service

Flask and MongoDB API for the band website's songs. This project started from the IBM Skills Network capstone template.

## Endpoints

`GET /health`, `GET /count`, `GET /song`, `GET /song/<id>`, `POST /song`, `PUT /song/<id>`, and `DELETE /song/<id>`.

## Configuration

Set `MONGODB_SERVICE` to the MongoDB host, and optionally set `MONGODB_PORT`, `MONGODB_USERNAME`, and `MONGODB_PASSWORD`. Set `PORT` for the Flask development server. For local testing without MongoDB, `MONGODB_SERVICE=mock` uses the `mongomock` package. This mode does not persist data.

Install dependencies from `requirements.txt`, then run `python -m pytest` and `python app.py`. The service seeds an empty songs collection from `backend/data/songs.json`.
