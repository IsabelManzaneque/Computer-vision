# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 01/11/2023
Description: Segmentacion sin conocimiento del dominio - Apartado 5.2
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans


img = cv2.imread(".\\assets\\brain1.png", cv2.IMREAD_GRAYSCALE)
rows, cols = img.shape[:2]
k = 5

pixels = img.reshape((-1, 1))

kmeans = KMeans(n_clusters=k)
kmeans.fit(pixels)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

segmentedImg = centroids[labels].reshape(img.shape)

cv2.imshow("Original", cv2.resize(img, (cols//2, rows//2)))
cv2.imshow("Segmentada", cv2.resize(segmentedImg.astype(np.uint8), (cols//2, rows//2)))
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.destroyAllWindows()