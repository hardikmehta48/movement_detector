# Movement Detector
Detect the object and describes its movement.

*Go to this link:- https://drive.google.com/drive/folders/1elA7kaAE1y83vYedm22WuotQ3ZYFYH06?usp=sharing to download yolov3.weights file. Add that file to yolo-coco folder to run the code.

Here the Object Detector Detects objects throught DarkNet YOLO Object detection. That Object detector returns the centroid, height and width of a detected human. So this movement detector detect only for human movements.

Direction Detector Uses the values of current frame and previous frame and see for the change then gives the output for movements. 
