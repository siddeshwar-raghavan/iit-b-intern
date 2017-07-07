import numpy as np
import cv2
import glob
import os



def find_marker(image):

	# convert the image to grayscale, blur it, and threshold
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

  	blur = cv2.GaussianBlur(gray,(1,1),1000)
  	flag, thresh = cv2.threshold(blur, 64, 200, cv2.THRESH_BINARY_INV)

	# find the contours in the thresholded image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	(cnts, _) = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if not cnts or not cv2.contourArea:
		return None
	else:
		c = max(cnts, key = cv2.contourArea)
		return cv2.minAreaRect(c)

	# compute the bounding box of the of the paper region and return it


def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth



# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0

# initialize the known object width, which in this case, the piece of
# paper is 11 inches wide
KNOWN_WIDTH = 2.0

# initialize the list of images that we'll be using from the video split into images
#just commenting the capture video part as video is already being stripped into images and stored
#vidcap = cv2.VideoCapture('marker.mp4')
#success,image = vidcap.read()
#count = 1
#IMAGE_PATHS=[]
#success = True
#while success:
#  IMAGE_PATHS[count] = vidcap.read()
  #print 'Read a new frame: ', success
#  count += 1
IMAGE_PATHS = ["2ft_mark.jpg"]

# load the first image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread(IMAGE_PATHS[0])
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
dist = [] #keep the found distance in an array
# loop over the images
#for i in range(1,393):

	# load the image, find the marker in the image
for i in range(0,258):

	name = (“p%d.jpg” %i)
	image = cv2.imread(name)
	marker = find_marker(image)
	#if marker == None
	if not marker:
		continue
	else:
		#if marker find distance else continue
		inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
		#dist[i]=inches # store the found distance for later use
		# draw a bounding box around the image and display it
		box = np.int0(cv2.cv.BoxPoints(marker))
		cv2.drawContours(image, [box], -1, (255, 0, 0), 10)
		image = cv2.resize(image, (500, 500))
		cv2.putText(image, "%.2fft" % (inches / 12), (image.shape[1] - 100, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
		cv2.imshow("image", image)
		cv2.waitKey(0)
