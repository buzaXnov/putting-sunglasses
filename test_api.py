import requests

# Open the image file in binary mode
with open("faces/image_7.jpg", 'rb') as f:
    # Send the POST request
    response = requests.post('http://localhost:5000/insert_sunglasses', files={'image': f})

# The response will be the image with sunglasses inserted, you can save it as follows:
with open('output.jpg', 'wb') as f:
    f.write(response.content)