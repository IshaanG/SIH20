import os
from flask import Flask, request, Response, jsonify
import cv2
from FaceAction import FaceAction
from PIL import Image
import numpy
from flask import render_template

app = Flask(__name__)

# for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')  # Put any other methods you need here
    return response


@app.route('/')
def index():
    return Response(open('./static/local.html').read(), mimetype="text/html")


@app.route('/image', methods=['POST'])
def image():

    image_file = request.files['image']  # get the image

    #print("-----------", image_file)

    # print(image_file)
    # # finally run the image through tensor flow object detection`
    image_object = numpy.array(Image.open(image_file).convert('RGB'))
    image_object = image_object[:, :, ::-1].copy()
    drow, yawn, pos = FaceAction().run_frame(image_object)

    print(drow, yawn, pos)
    d = {"drow": drow, "yawn": yawn, "pos": pos}
    return jsonify(d)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
