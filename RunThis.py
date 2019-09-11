import Object_Detector as od
import Detect_Direction as dd
import cv2

#===================================================================================================
cap = cv2.VideoCapture(0)
op0, op1 = '', ''
i = 0
while(True):
	(grabbed, frame) = cap.read()
	if not grabbed:
		break

	if i==0:
		op = od.detect(frame)
		if op == None:
			print("Not Detected:")
		else:
			xp, yp, wp, hp = op[0], op[1], op[2], op[3]
		if xp==0 and yp==0:
			print('NOT DETECTED')
		print("Start: ")
		i = 1

	else:
		op = od.detect(frame)
		if op == None:
			print("Not Detected:")
		else:
			x, y, w, h = op[0], op[1], op[2], op[3]

		op0 = dd.getHori(x,y, xp,yp)
		op1 = dd.getVerti(w,h, wp,hp)

		xp,yp, wp,hp = x,y, w,h

	print(op0+op1)

	cv2.imshow('object detection', cv2.resize(frame, (800,600)))
	if cv2.waitKey(5) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break

#===================================================================================================
