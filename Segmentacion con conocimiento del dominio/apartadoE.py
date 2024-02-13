# -*- coding: utf-8 -*-
"""
File: apartadoE.py
Author: Isabel Manzaneque
Date: 14/12/2023 
Description: Segmentación con conocimiento del dominio.

"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets, linear_model

img = cv2.imread(".\\assets\\lineaRuidosa.png")
height, width = img.shape[:2]

n_samples = 0
X_list = []
y_list = []

# iterar sobre la imagen original
for py in range(height):
    for px in range(width):
        if np.array_equal(img[py, px], [0, 0, 0]):
            # Si el pixel es negro se incrementan las muestras
            # y se guardan las coordenadas 
            n_samples += 1
            X_list.append([px])
            # ajustar origen
            y_list.append(height - py)

# convertir listas en numpy arrays
X = np.array(X_list)
y = np.array(y_list)

_, _, coef = datasets.make_regression(
    n_samples=n_samples,
    n_features=1,
    n_informative=1,
    noise=10,
    coef=True,
    random_state=0,
)

# Robustly fit linear model with RANSAC algorithm
ransac = linear_model.RANSACRegressor()
ransac.fit(X, y)
inlier_mask = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)

# Predict data of estimated models
line_X = np.arange(X.min(), X.max())[:, np.newaxis]
line_y_ransac = ransac.predict(line_X)

# Compare estimated coefficients
print("Estimated coefficients (true, linear regression, RANSAC):")
print(coef, ransac.estimator_.coef_)

# Dibujar plot
lw = 2
plt.scatter(X[inlier_mask], y[inlier_mask], color="yellowgreen", marker=".", label="Inliers")
plt.scatter(X[outlier_mask], y[outlier_mask], color="gold", marker=".", label="Outliers")
plt.plot(line_X, line_y_ransac,color="cornflowerblue", linewidth=lw,label="RANSAC regressor",)
plt.legend(loc="lower right")
plt.xlabel("Input")
plt.ylabel("Response")
plt.show()


