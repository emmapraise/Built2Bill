from flask import Flask, render_template,url_for,request, redirect, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import io
from io import BytesIO
import cv2
import numpy as np
import urllib.request
# import uuid
# import cloudstorage as gcs
# from google.appengine.api import images, app_identity
# import os
# import pickle
# from sklearn.externals import joblib
# from keras.models import model_from_json

# from google.cloud import storage

# storage_client =storage.Client.from_service_account_json('Built2bill-ea533c3e831e.json') #

app = Flask(__name__)

def upload_to_bucket(file, bucket_name):
	"""
	input
	------
	file:
	The image to be uploaded.

	bucket_name:
	The name of the bucket which the image will be uploaded into.

	Return
	-------
	It returns the public url to access the image saved in the bucket.

	"""
	# destination_blob_name = secure_filename(file.filename)
	# bucket = storage_client.get_bucket(bucket_name)
	# blob = bucket.blob(destination_blob_name)

	# blob.upload_from_string(file.read(), content_type=file.content_type)
	# blob.make_public()
	# p_url=blob.public_url
	# # uri = 'gs://%s/%s' % (bucket_name, destination_blob_name)

	# return p_url

def count_lines(p_url):
	"""
	p_url
	-----
	The public url of the image from the upload bucket

	Return
	---------
	The number of lines counted from the image
	"""
	resp = urllib.request.urlopen(p_url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	imge = cv2.imdecode(image, -1)
	blur = cv2.blur(imge,(5,5))
	gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 75, 150)
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)
	for line in lines:
  		x1, y1, x2, y2 = line[0]
  		cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
	pred_value = len(lines)
	
	return pred_value

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/aboutus')
def aboutus():
	return render_template('aboutus.html')

@app.route('/onepage')
def onepage():
	return render_template('onepage-creative.html')

@app.route('/about', methods = ['POST'])
def predict():

	bucket_name = "built2bill-upload"
	file = request.files['file']
	# get_image = upload_to_bucket(file, bucket_name)

	lines = count_lines(file)
	return render_template('aboutus.html', prediction = lines)
