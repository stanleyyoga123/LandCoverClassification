from sklearn.cluster import KMeans
import numpy as np
import cv2
import os

IMAGES_FOLDER = r'static'

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
    
    images = [np.copy(image) for i in range(cluster)]

    for i, arr_el in enumerate(final):
        for j, el in enumerate(arr_el):
            images[el][i][j] = red
    
    if(save):
        # name = path.split('\\')[-1].split('.')[0]
        name = path.split('\\')
        if(len(name) == 1):
            name = path.split('/')
        
        name = name[-1].split('.')[0]
        for i, image in enumerate(images):
            image = cv2.resize(image, (200,200))
            cv2.imwrite(os.path.join(IMAGES_FOLDER, f'{name}_{i}.png'), image)
            # cv2.imwrite(f'{name}_{i}.png', image)
    
    return images

def combine(index):
    images = np.array([cv2.imread(os.path.join(IMAGES_FOLDER, path)) for path in os.listdir(IMAGES_FOLDER)])

    image = images[index[0]]
    shape = image.shape

    red = [0, 0, 255]

    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in index:
                if((images[k][i][j] == red).all()):
                    image[i][j] = red

    return image

def count_pix(filename):
    image = cv2.imread(filename)
    red = [0, 0, 255]
    count = 0
    for row in image:
        for el in row:
            if((el == red).all()):
                count += 1
    return count