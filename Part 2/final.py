import cv2
import numpy as np
from random import randint   


global no_stop 
no_stop = True

def game():
    #defining the ball & its steps
    dx, dy = 4,4 #vitesse du ballon
    x1,y1 = 90,150 #init top left
    x2,y2 = 100,160 #init bottom right
    offset_mvt = 50
    bar_lvl = 410
    bricks_start_x = 10
    bricks_start_y = 50
    largeur_brick = 60
    hauteur_brick =20
    pts=0
    whole_wid = 640
    bricks = []
    surfacemin, surfacemax = 5000,500000

    #définir nos bricks
    for i in range(4):
        bricks.append([])
        for j in range(18):
            bricks[i].append([]) 
        for j in range(18):
            new_brick_x = bricks_start_x + largeur_brick*j
            new_brick_y = bricks_start_y + hauteur_brick*i
            bricks[i][j] = str(new_brick_x)+"_"+str(new_brick_y)

    cap = cv2.VideoCapture(0)
    while(1):
        _, frame = cap.read( )
        frame = cv2.flip(frame, 1,frame)
        hsv = cv2.cvtColor( frame ,cv2.COLOR_BGR2HSV ) #frame in hsv format
        lower_blue = np.array([110,50,50]) #lower hsv range of blue colour
        upper_blue = np.array( [ 113 ,255 ,255 ] ) #upper hsv range of blue colour
        mask = cv2.inRange(hsv,lower_blue ,upper_blue ) 
        mask = cv2.erode( mask ,None ,iterations=2 )
        mask = cv2.dilate( mask,None ,iterations=2 )
        contours= cv2.findContours(mask ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        for i in range( 0, len(contours)):
            if ( i % 1 == 0 ):
                cnt = contours[i] #on prend l'elt
                if cv2.contourArea(cnt) > surfacemin and cv2.contourArea(cnt) < surfacemax:
                    x,y,w,h = cv2.boundingRect(cnt)
                    rayon = w//2
                    frame = cv2.circle(frame,(x,y),rayon,(100,120,20),5)
                    if(rayon > 50):
                        img = cv2.rectangle( frame,( whole_wid-(offset_mvt-25) ,bar_lvl ), ( whole_wid-(offset_mvt+25) ,bar_lvl+10 ), (255 ,255 ,255), -1 )
                        cv2.rectangle( mask, ( x ,y ) ,( x+w ,y+h ) ,( 255 ,0 ,0 ) ,2 )
                    offset_mvt = int( ( x - ( w/2 ) ) )
        x1 = x1 + dx
        y1 = y1 + dy
        y2 = y2 + dy
        x2 = x2 + dx
        img = cv2.rectangle( frame, ( x1 ,y1 ), ( x2 ,y2 ), ( 255 ,255 ,255 ), -1 )
        for i in range(4):
            for j in range(18):
                rec = bricks[i][j]
                if rec != []:
                    rec1 = str(rec)
                    rec_1 = rec1.split("_")
                    x12 = int(rec_1[0])
                    y12 = int(rec_1[1])
                img = cv2.rectangle( frame, ( x12 , y12 ), ( x12+50 , y12+10 ), ( 0 ,0+(10*j) ,0+(20*j) ), -1 )
        if ( x2 >= whole_wid ):
            dx = -(randint(1, 5))
        for i in range(4):
            for j in range(18):
                ree = bricks[i][j]
                if ree != []:
                    ree1 = str(ree)
                    ree_1 = ree1.split("_")
                    x13 = int (ree_1[0])
                    y13 = int (ree_1[1])
                    if (((x13 <= x2 and x13+50 >=x2) or (x13 <= x1 and x13+50 >=x1)) and y1<=y13 ) or (y1<=50):
                        dy = randint(1,5)
                        bricks[i][j]=[]
                        pts = pts+1
                        break                       

        score = "SCORE : "+str(pts)
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = ( 230 ,25 )
        fontScale              = 1
        fontColor              = ( 0 ,0 ,0 )
        lineType               = 2
        cv2.putText( img ,score,bottomLeftCornerOfText ,font ,fontScale ,fontColor ,lineType )
        if ( x1 <= 0 ):
            dx = randint(1,5)
        if ( y2 >= bar_lvl ):
            if (whole_wid-( offset_mvt-25 ) >= x2 and whole_wid-( offset_mvt+25 ) <= x2) or (whole_wid-( offset_mvt-25 ) >= x1 and whole_wid-( offset_mvt+25 ) <= x1):
                dy = -(randint(1, 5))
        if y2 >= bar_lvl:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = ( 230 ,25 )
            fontScale              = 1
            fontColor              = ( 0 ,0 ,0 )
            lineType               = 2
            cv2.putText( img ,'GAME OVER!' ,bottomLeftCornerOfText ,font ,fontScale ,fontColor ,lineType )        
            if y2 > bar_lvl+40:
                break
        #cv2.imshow( 'Mask' ,mask )
        cv2.imshow('frame',frame)
        if cv2.waitKey(10)&0xFF==ord('q'):
            cap.release( )
            cv2.destroyAllWindows( )
            global no_stop
            no_stop = False
            break
while (no_stop):
    game( )