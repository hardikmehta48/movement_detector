import numpy as np
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("--yolo", default = r'yolo-coco')
ap.add_argument("--confidence", type=float, default=0.8) # minimum probability required to display
ap.add_argument("--threshold", type=float, default=0.3) # threshold fors non-maxima suppression
args = vars(ap.parse_args())

#===================================================================================================
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

#===================================================================================================
# load our YOLO object detector trained on COCO dataset (80 classes) and determine only
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

#===================================================================================================
def detect(frame, W=None, H=None, eq_fact=1.0):
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	boxes = []
	confidences = []
	classIDs = []

	# construct a blob from the input frame and then perform a forward pass of
	# the YOLO object detector, giving us our bounding boxes and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)

	net.setInput(blob)
	layerOutputs = net.forward(ln)

	#===============================================================================================
	for output in layerOutputs:
		for detection in output:
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			# if detection belong ot class 0 (Its a person)
			if classID == 0:
				# filter out weak predictions by ensuring the detected probability is
				# greater than the minimum probability
				if confidence > args["confidence"]:
					# scale the bounding box coordinates back relative to the size of the image,
					# YOLO actually returns he center (x, y)-coordinates of the bounding box
					# followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					op = (centerX, centerY, width, height)

					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					# update our list of bounding box coordinates, confidences, and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

	#===============================================================================================
	# apply non-maxima suppression to suppress weak, overlapping bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])

	if len(idxs) > 0:
		for i in idxs.flatten():
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			cv2.rectangle(frame, (x, y), (x + w, y + h), 1, 2)
			return op

	else :
		return None
#===================================================================================================