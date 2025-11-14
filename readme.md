# UGC Downloader

A simple local **Social media downloader** with a React front-end and a Flask backend that uses **yt-dlp** to download videos. The UI lets you queue multiple URLs, set filenames, start downloads, and monitor live progress.

---

## Features

- Web UI (React) served as a single `index.html` file
- Background downloads using `yt-dlp` (non-blocking via Python `threading`)
- Live progress polling from backend (`/progress/<id>`)
- Custom file naming and queue management
- Download folder auto-created on the Desktop (`YT-Downloads`)

---

## Project structure (example)

```
project-root/
├─ app.py                # Flask backend (server + yt-dlp integration)
├─ index.html            # React UI (single-file, loaded with Babel)
├─ run.bat               # Optional: script to start the server on Windows
├─ requirements.txt      # Python dependencies
└─ README.md             # (this file)
```

---

## Requirements

- Python 3.8+ (3.10+ recommended)
- `pip` package manager
- Windows / macOS / Linux (tested on Windows)
- Internet connection (for downloading videos)

Python packages (install below):

- Flask
- Flask-CORS
- yt-dlp

You can install with:

```bash
pip install -r requirements.txt
```

_or install individually:_

```bash
pip install flask flask-cors yt-dlp
```

If you don't have a `requirements.txt`, create one with:

```
flask
flask-cors
yt-dlp
```

---

## How it works (high level)

1. The React UI (`index.html`) runs in your browser and lets you paste one or more YouTube URLs.
2. The UI POSTs to `/download` on the Flask backend with `{ url, filename, id }`.
3. Flask starts `yt-dlp` in a background thread and returns immediately.
4. The UI polls `/progress/<id>` to get live updates about download status and percentage.
5. Completed files are saved to `~/Desktop/YT-Downloads` by default.

---

## Usage

1. Clone or copy the repository to your machine.

2. Install dependencies (see **Requirements**).

3. Start the Flask server:

On Windows you may use a `run.bat` file with content like:

```bat
@echo off
python app.py
pause
```

Or run directly from terminal:

```bash
python app.py
```

4. When the server starts it should print the download folder path and open `http://localhost:5000` in your default browser.

5. In the browser: paste one or more YouTube URLs (one per line), set a description (used for naming), click **Add to Queue**, then **Start Downloads**.

6. Files will appear in `Desktop/YT-Downloads` (or the folder printed by the backend).

---

## Endpoints (backend)

- `GET /` or `/index.html` — serves the frontend file
- `POST /download` — start a download; expects JSON `{ url, filename, id }`
- `GET /progress/<id>` — returns download progress for an item id
- `GET /download-folder` — returns JSON `{ folder: '<path>' }`
- `GET /health` — health check; returns `{ status: 'ok' }`

---

## Configuration

- **Download folder**: by default the backend sets `DOWNLOAD_FOLDER` to `~/Desktop/YT-Downloads`. Change this in `app.py`:

```python
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "YT-Downloads")
```

- **Port**: Flask runs on port `5000` by default in `app.py`. Change `app.run(..., port=5000)` if needed.

- **CORS**: `CORS(app)` is enabled so the UI (served from same machine) can fetch the API. If you host the frontend on another domain, configure `flask_cors.CORS` accordingly.

---

## Security & Notes

- This project is intended to run **locally** (localhost). Do NOT expose the server to the public internet without adding authentication and access controls.
- `yt-dlp` can download from many sources — only use it where you have permission to download content.
---

## Troubleshooting

- **Server not connected**: Confirm Flask is running and listening at `http://localhost:5000`. Check terminal for errors.
- **CORS errors**: Ensure `CORS(app)` in `app.py`. If frontend served from a different origin, allow that origin specifically.
- **Progress stuck**: Inspect Flask logs for exceptions in `progress_hook`. `yt-dlp` uses `_percent_str` in hooks — if absent, progress may remain at 0.
- **Permission errors saving files**: Ensure the user running the script has write permission to the download folder.

---

## Improvements / Next steps

- Build the frontend with a proper bundler (Vite/webpack) instead of Babel in browser for production.
- Replace polling with WebSocket or Server-Sent Events for real-time progress.
- Add authentication and role checks if hosting on a network.
- Improve concurrency control (limit parallel downloads)
- Sanitize filenames and validate input URLs.

---

## Contributing

PRs are welcome. Please open an issue first to discuss major changes.

---

## License

This project is provided under the **MIT License**. Feel free to adapt and reuse.

---

## Contact

If you want changes to this README (more details, examples, or add badges), tell me what to include and I will update it.

