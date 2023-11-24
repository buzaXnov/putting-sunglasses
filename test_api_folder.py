import os
import glob
import requests

# Check if the directory exists
if not os.path.exists('results'):
    # If the directory doesn't exist, create it
    os.makedirs('results')

# Open the image file in binary mode
for image_file in glob.glob("faces/*"):
    with open(image_file, 'rb') as f:
        # Send the POST request
        response = requests.post('http://localhost:5000/insert_sunglasses', files={'image': f})

    # The response will be the image with sunglasses inserted, you can save it as follows:
    output_file = "results/" + image_file.split("/")[-1]
    with open(output_file, 'wb') as f:
        f.write(response.content)