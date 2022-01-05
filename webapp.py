"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
import torch
from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import requests
from io import BytesIO
import json
import urllib.parse
import warnings
warnings.simplefilter('ignore')

app = Flask(__name__)
CORS(app)

'''
DETECTION_URL = "/v1/predict"

@app.route(DETECTION_URL, methods=["POST", "GET"])
def api_predict():
    if request.method == "GET":
        url = request.args.get('image', '')
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        results = model(img, size=416)
        data = results.pandas().xyxy[0].to_json(orient="records")
        return data

    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        results = model(img, size=416)
        data = results.pandas().xyxy[0].to_json(orient="records")
        return data
'''

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        url = request.args.get('image', '')

        if url == "":
            return render_template("index.html")
            # return {}

        
        

        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        width, height = img.size

        results = model(img, size=416)

        data = results.pandas().xyxy[0].to_json(orient="records")
        data = json.loads(data)

        items = []

        id = url

        canvas = "{}/canvas/pk1".format(id)

        for i in range(len(data)):
            obj = data[i]

            index = i + 1

            x = int(obj["xmin"])
            y = int(obj["ymin"])
            w = int(obj["xmax"]) - x
            h = int(obj["ymax"]) - y

            xywh = "{},{},{},{}".format(x, y, w, h)

            items.append({
                "id": "{}/annos/{}".format(canvas, index),
                "motivation": "commenting",
                "target": "{}#xywh={}".format(canvas, xywh),
                "type": "Annotation",
                "body": {
                    "type": "TextualBody",
                    "value": "{} {}".format(obj["name"], obj["confidence"])
                }
            })

        manifest = {
            "@context": [
                "http://iiif.io/api/presentation/3/context.json",
                "http://www.w3.org/ns.anno.jsonld"
            ],
            "behavior": [
                "individuals"
            ],
            "id": request.url,
            "items": [
                {
                    "annotations" : [
                        {
                            "id" : "{}/annos".format(canvas),
                            "items" : items,
                            "type": "AnnotationPage"
                        }
                    ],
                    "height": height,
                    "id": "{}".format(canvas),
                    "items": [
                        {
                            "id": "{}/page".format(canvas),
                            "items": [
                                {
                                    "body": {
                                        "format": "image/jpeg",
                                        "height": height,
                                        "id": "{}".format(url),
                                        "type": "Image",
                                        "width": width
                                    },
                                    "id": "{}/page/imageanno".format(canvas),
                                    "motivation": "painting",
                                    "target": "{}".format(canvas),
                                    "type": "Annotation"
                                }
                            ],
                            "type": "AnnotationPage"
                        }
                    ],
                    "label" : "[1]",
                    "type": "Canvas",
                    "width": width
                }
            ],
            "label": url,
            "type": "Manifest",
        }

        # import requests
        url = 'https://api.jsonbin.io/v3/b'
        headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': '$2b$10$unmAqqNkGBsCaaOK3d4QEui0i./fZ0INKty90iDOBMHHRoB.ywT.S',
            'X-Bin-Private': 'false'
        }
        data = manifest

        req = requests.post(url, json=data, headers=headers).json()
        # print(req["metadata"]["id"])

        manifest_uri = "https://api.jsonbin.io/b/" + req["metadata"]["id"]

        viewer = request.args.get('viewer', '')
        if viewer == "1":
            return redirect("http://www.kanzaki.com/works/2016/pub/image-annotator?u=" + manifest_uri) # + urllib.parse.quote(request.url.replace("viewer=1", "")))

        return redirect(manifest_uri)

        '''
        # for debugging
        # data = results.pandas().xyxy[0].to_json(orient="records")
        # return data

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save("static/image0.jpg", format="JPEG")
        # return redirect("static/image0.jpg")

        return manifest
        '''

    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        results = model(img, size=416)

        # for debugging
        # data = results.pandas().xyxy[0].to_json(orient="records")
        # return data

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save("static/image0.jpg", format="JPEG")
        return redirect("static/image0.jpg")

    return render_template("index.html")

def predict2():
    if request.method == "GET":
        url = request.args.get('image', '')

        if url == "":
            return render_template("index.html")

        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        results = model(img, size=416)

        # for debugging
        # data = results.pandas().xyxy[0].to_json(orient="records")
        # return data

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save("static/image0.jpg", format="JPEG")
        return redirect("static/image0.jpg")

    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        results = model(img, size=416)

        # for debugging
        # data = results.pandas().xyxy[0].to_json(orient="records")
        # return data

        results.render()  # updates results.imgs with boxes and labels
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save("static/image0.jpg", format="JPEG")
        return redirect("static/image0.jpg")

    return render_template("index.html")

'''
def copy_attr(a, b, include=(), exclude=()):
    # Copy attributes from b to a, options to only include [...] and to exclude [...]
    for k, v in b.__dict__.items():
        if (len(include) and k not in include) or k.startswith('_') or k in exclude:
            continue
        else:
            setattr(a, k, v)
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt') # .autoshape()  # force_reload = recache latest code
    model.eval()
    
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
    # app.run(host="0.0.0.0", port=args.port, debug=True)  # debug=True causes Restarting with stat
