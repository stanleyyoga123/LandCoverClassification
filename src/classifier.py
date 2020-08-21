from sklearn.cluster import KMeans
import numpy as np
import cv2
import os

IMAGES_FOLDER = r'images'

def run(path, cluster, save=True):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    shape = gray.shape
    data = gray.reshape(-1, 1)

    km = KMeans(n_clusters=cluster)
    km.fit(data)
    km.predict(data)

    final = km.labels_.reshape(shape)

    red = [0, 0, 255]
    # green = [0, 255, 0]
    # blue = [255, 0, 0]

    images = [np.copy(image) for i in range(cluster)]

    for i, arr_el in enumerate(final):
        for j, el in enumerate(arr_el):
            images[el][i][j] = red
    
    # for i in range(len(images)):
    #     images[i] = cv2.resize(images[i], (200, 200))

    if(save):
        for i, image in enumerate(images):
            cv2.imwrite(os.path.join(IMAGES_FOLDER, f'{i}.png'), image)
    
    return images