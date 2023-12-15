# -*- coding: utf-8 -*-
"""
File: apartadosAyB.py
Author: Isabel Manzaneque
Date: 15/12/2023 
Description: Descriptores de puntos característicos.

"""
import numpy as np
import cv2


MIN_MATCH_COUNT = 10

img1 = cv2.imread(".\\assets\\box.png", 0)  # query img
img2 = cv2.imread(".\\assets\\box_in_scene.png", 0) # train img

# Find SIFT features -----------------------------------

# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)
    

if len(good)>MIN_MATCH_COUNT:
    # extract the locations of matched keypoints in both the images.
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    
    # dst contiene las coordenadas de los vértices transformados
    dst = cv2.perspectiveTransform(pts,M)
    for i in range(dst.shape[0]):
        print(f"Vértice {i+1}: ({dst[i][0][0]}, {dst[i][0][1]})")

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None
 
# draw our inliers (if successfully found the object) or matching keypoints (if failed)       

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)





cv2.imshow("Matched", img3)

cv2.waitKey(0)
cv2.destroyAllWindows()