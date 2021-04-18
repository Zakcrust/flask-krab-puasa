from flask import Flask, send_file
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from datetime import datetime
import pytz

app = Flask(__name__)

TZ = pytz.timezone("Asia/Jakarta")

START_DATE = datetime(2021, 4, 12, tzinfo=TZ)
FONT_PATH = "./NotoSans-Bold.ttf"
BASE_IMAGE_PATH = "./images/base_image.jpg"
SAVE_IMAGE_PATH = "./images"


@app.route("/", methods=["GET"])
def index():
    now = datetime.now(tz=TZ)
    print("Now datetime")
    print(now)
    day_difference = (now - START_DATE).days
    filename = f"{SAVE_IMAGE_PATH}/hari_{day_difference}.jpg"
    try:
        with open(filename) as f:
            print("File already exist")
    except IOError:
        print("File didnt exist, creating new one...")
        create_new_image(filename, day_difference)
    
    return send_file(filename, mimetype="image/jpg")


def create_new_image(filename, day_difference):  
    print("Loading Base Image...")
    img = Image.open(BASE_IMAGE_PATH)
    draw = ImageDraw.Draw(img)
    
    print("Loading Fonts...")
    font = ImageFont.truetype(FONT_PATH, 35, encoding="unic")
    
    top_text = "PUASA"
    bottom_text = f"HARI KE {day_difference}"
    fill_color = (255, 255, 255)
    stroke_color = (0, 0, 0)
    
    print("Adding Texts...")
    draw.text((175, 0), top_text, font=font, fill=fill_color, stroke_width=4, stroke_fill=stroke_color)
    draw.text((150, 310), bottom_text, font=font, fill=fill_color, stroke_width=4, stroke_fill=stroke_color)
    
    print("Saving Images...")
    img.save(filename)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = 0
    return r