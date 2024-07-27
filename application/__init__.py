from flask import Flask
from flask_dropzone import Dropzone
import os
from flask_session import Session

app=Flask(__name__)


SESSION_TYPE="filesystem"
app.config.from_object(__name__)
Session(app)
dir_path=os.path.dirname(os.path.realpath(__file__))


app.config.update(
    UPLOADED_PATH=os.path.join(dir_path,"static/uploaded_files"),
    DROPEZONE_ALLOWED_FILE_TYPE='default',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
    AUDIO_FILE_UPLOAD=os.path.join(dir_path,"static/audio_files"),
    TXT_FILE_UPLOAD=os.path.join(dir_path,"static/text_files")
)

app.config['DROPZONE_REDIRECT_VIEW']='decoded'
dropzone = Dropzone(app)
from application import routes

