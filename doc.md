# Deployment Guide
### Prerequisites
Ensure that you have Python 3.6 or newer installed on your Ubuntu server. You can check your Python version by running python3 --version in the terminal.

## Steps
1. Transfer the code to your server. You can use SCP to transfer the code to your server.

2. Install the necessary Python packages. Navigate to the directory containing the code and run pip3 install -r requirements.txt to install the necessary Python packages. The requirements.txt file lists all the Python packages that your project depends on.

3. Set up a virtual environment (optional). This step is optional, but it's a good practice to use a virtual environment for your Python projects. You can set up a virtual environment using the venv module: python3 -m venv env. Activate the virtual environment with `source env/bin/activate`.

4. Run the Flask application. You can start the Flask application with `python3 app.py`. By default, the application will run on port 5000.

5. Set up a reverse proxy (optional). If you want to make your API accessible on port 80 (the default HTTP port), you can set up a reverse proxy with a web server like Nginx or Apache.

6. Set up a process manager (optional). If you want your Flask application to keep running even after you close the terminal, you can use a process manager like Supervisor or systemd.

## Code Explanation
The provided code is a Flask application that applies sunglasses to an image. The main class is PutOn, which is responsible for applying the sunglasses.

When an instance of `PutOn` is created, it initializes a face detector and loads the sunglasses asset. The sunglasses asset is a PNG image of sunglasses, and it's loaded along with its corresponding points that define the region of interest.

The `save_landmarks` and `save_results` methods are left in the class definition for future debugging. 

The `run` method takes the image loaded by the Flask endpoint and loads it into the face alignment detector after which the sunglasses are properly transformed and placed on the head of the wearer. If the face is too small, it will be blurred. The method returns the image that the Flask app enodes and returns. 

The Flask application exposes a single endpoint (/insert_sunglasses) that accepts POST requests. When a request is received, it reads the image from the request, applies the sunglasses using an instance of PutOn, and returns the resulting image.

## Steps for running locally
Open your terminal and create a Python virtual environment for the project to install all the dependencies (libraries):

`$ python -m venv .env //optional`

Activating the environment to start working: 

`$ source .env/bin/activate `

Install all the dependencies (external libraries) necessary to run the code: 
`$ pip intall -r requirements.txt `

Run the API endpoint where the images will be sent and received from: 
`$ python app.py`

Run the `test_api_folder.py` file to send the images and save the results:

`$ python test_api_folder.py`

 Make sure that the images are saved in the folder called `faces` and the results will be saved in a folder called `results` that will be created automatically if it does not exist. 