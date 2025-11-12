from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import os
import threading
import webbrowser
import time

app = Flask(__name__, static_folder='.')
CORS(app)

# Download folder - Files will be saved here
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "YT-Downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Store download progress
download_progress = {}

def progress_hook(d, item_id):
    """Track download progress"""
    if d['status'] == 'downloading':
        try:
            # Extract percentage
            percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
            percent = float(percent_str)
            download_progress[item_id] = {
                'status': 'downloading',
                'progress': percent
            }
        except:
            pass
    elif d['status'] == 'finished':
        download_progress[item_id] = {
            'status': 'completed',
            'progress': 100
        }

def download_video(url, filename, item_id):
    """Download video using yt-dlp"""
    try:
        download_progress[item_id] = {
            'status': 'downloading',
            'progress': 0
        }
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{filename}.%(ext)s'),
            'progress_hooks': [lambda d: progress_hook(d, item_id)],
            'quiet': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    except Exception as e:
        download_progress[item_id] = {
            'status': 'error',
            'error': str(e),
            'progress': 0
        }

# Route to serve index.html
@app.route('/')
@app.route('/index.html')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/download', methods=['POST'])
def start_download():
    """Endpoint to start a download"""
    data = request.json
    url = data.get('url')
    filename = data.get('filename')
    item_id = data.get('id')
    
    # Start download in background thread
    thread = threading.Thread(target=download_video, args=(url, filename, item_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'id': item_id})

@app.route('/progress/<item_id>', methods=['GET'])
def get_progress(item_id):
    """Get download progress for a specific item"""
    progress = download_progress.get(str(item_id), {'status': 'pending', 'progress': 0})
    return jsonify(progress)

@app.route('/download-folder', methods=['GET'])
def get_download_folder():
    """Return the download folder path"""
    return jsonify({'folder': DOWNLOAD_FOLDER})

@app.route('/health', methods=['GET'])
def health_check():
    """Check if server is running"""
    return jsonify({'status': 'ok'})

def open_browser():
    """Open browser after server starts"""
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 YT-DOWNLOADER SERVER STARTED!")
    print("="*60)
    print(f"📁 Downloads will be saved to:")
    print(f"   {DOWNLOAD_FOLDER}")
    print(f"\n🌐 Opening browser...")
    print(f"   If browser doesn't open, go to: http://localhost:5000")
    print("\n⚠️  Keep this window open while using the app!")
    print("   Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Open browser automatically
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask server
    app.run(debug=False, port=5000, use_reloader=False)