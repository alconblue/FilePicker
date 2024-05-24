import io

from flask import Flask, render_template, request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file_id = request.form.get("fileId")
    token = request.form.get("token")
    credentials = Credentials(token=token)
    service = build('drive', 'v3', credentials=credentials)
    download_request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, download_request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    # This should be sent to a separate database, currently we will store it in the same disk
    with open(file_id, 'wb') as f:
        f.write(fh.getvalue())
    # Get more metadata about the files and store it in the metadata storage, e.g. mime type
    # TODO (zoebm): integrate with sqlite3 quickly if time permits
    return "Successful"


# Periodic sync hook to be added
@app.route("/sync", methods=["POST"])
def sync():
    # Excecute: file_ids = SELECT FILE_ID FROM METADATA_TABLE WHERE DIRTY=FALSE
    # for file_id in file_id:
    # file_id="1f8JRLLmPwiK3zEHEl4Mzx6GzuKeUqXR6"
    # Send request:
    '''POST https://www.googleapis.com/drive/v3/files/{file_id}/watch
        Authorization: Bearer CURRENT_USER_AUTH_TOKEN
        Content-Type: application/json
        {
            "id": "01234567-89ab-cdef-0123456789ab", // Your channel ID.
            "type": "web_hook",
            "address": "https://mydomain.com/notifications",
            "token": "target=myApp-myFilesChannelDest", // (Optional) Your files channel token.
            "expiration": 1426325213000 // (Optional) Your requested channel expiration date and time.
        }'''
    return True


@app.route("/notifications", methods=["POST"])
def notifications(watch_response):
    # for resourceUri in watch_response['resourceUri']:
    # update the blob in blob store after fetching with resource Uri
    return True


@app.route("/view/<file_id>", methods=["GET"])
def view(file_id):
    return render_template("view.html", file_id=file_id)


if __name__ == "__main__":
    app.run()
