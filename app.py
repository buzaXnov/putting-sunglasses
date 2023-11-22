from flask import Flask, request, send_file
from io import BytesIO
from sunglasses import PutOn  # replace with your actual import
import cv2
import numpy as np

app = Flask(__name__)


@app.route('/insert_sunglasses', methods=['POST'])
def insert_sunglasses():
    # Get the image from the request
    image_file = request.files['image']
    image_bytes = image_file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Get the format of the image from the content type
    img_format = image_file.filename.split('.')[-1]

    # Create an instance of your sunglasses inserting program
    inserter = PutOn()

    # Insert the sunglasses
    result = inserter.run(image)  # replace with your actual method

    # Convert the result into bytes
    is_success, buffer = cv2.imencode(f".{img_format}", result)

    if not is_success:
        print(f"Error when converting results into bytes. {is_success}")

    byte_io = BytesIO(buffer)

    # Return the result
    return send_file(byte_io, mimetype=f"image/{img_format.lower()}")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
