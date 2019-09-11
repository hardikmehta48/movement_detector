
def getHori(x,y, xp,yp): # Detection of movement of object in horizantal direction
	if x>xp:
		return "Right "
	elif xp>x:
		return "Left "
	else:
		return "Still "

#===================================================================================================
def getVerti(w,h, wp,hp): # Detection of movement in vertical direction
	thresh = 8
	dif0 = (w-wp)**2
	dif1 = (h-hp)**2

	if dif0<thresh or dif1<thresh:
		return " "
	else:
		if w<wp and h<hp:
			return "and away from the camera"
		else :
			return "and towards the camera"

#===================================================================================================
