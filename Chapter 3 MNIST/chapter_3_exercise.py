# -*- coding: utf-8 -*-
"""Chapter 3: Exercise

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ii9AHsH8YvmNrcYzcf42ViFIt5pCjfhR
"""

# !nvidia-smi

import numpy as np
import sklearn
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

plt.rcParams['figure.figsize'] = (10, 8)

"""## Question 1. Try to build a classifier for the MNIST dataset that achieves over 97% accuracy on the 
`KNeighborsClassifier` test set. Hint: the works quite well for this task; you just need to find good hyperparameter 
values (try a grid search on the `weight` and `n_neighbor` hyperparameters). """

# fetch MNIST datset
data = fetch_openml('mnist_784', version=1)

print(data.data)

print(data.target)

X, y = data.data, data.target

# split data train/test
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
plt.imshow(x_train[4].reshape(28, 28), cmap='binary')
plt.show()
print(y_train[4])

plt.imshow(x_test[7].reshape(28, 28), cmap='binary')
plt.show()
print(y_test[7])

y_test, y_train = y_test.astype(np.uint8), y_train.astype(np.uint8)
print(y_test[7])

## KNN classifier as in question

knnclf = KNeighborsClassifier()

print(y_train)

knnclf.fit(x_train, y_train)

somedigit = x_test[7]
val = knnclf.predict([somedigit])
print(y_test[7], val)

# cross_val_score(knnclf, x_train, y_train, cv=3, scoring='accuracy')
# output: array([0.96583813, 0.96632584, 0.96491765])

parameters = {
    'n_neighbors': [1, 3, 5],
    'weights': ['uniform', 'distance']
}
gscv = GridSearchCV(knnclf, param_grid=parameters, scoring='accuracy', verbose=10, cv=3)

# gscv.fit(x_train, y_train)
# gscv.best_estimator_


"""## 2. Write a function that can shift an MNIST image in any direction (left, right, up, or down) by one pixel.5 
Then, for each image in the training set, create four shifted copies (one per direction) and add them to the training 
set. Finally, train your best model on this expanded training set and measure its accuracy on the test set. You 
should observe that your model performs even better now! This technique of artificially growing the training set is 
called data augmentation or training set expansion """

sample = X[55]
sample = np.roll(sample, 5)
sample = sample.reshape(28, 28)
plt.imshow(sample, cmap='binary')
plt.show()

a = X[55].shape
b = X[55].reshape(28, 28).reshape(-1).shape
print(np.equal(a, b))


# image argumentation definition

def shift_right(img):
    img = img.reshape(28, 28)
    img = np.roll(img, 2)
    img = img.reshape(1, -1)
    return img


def shift_left(img):
    img = img.reshape(28, 28)
    img = np.roll(img, -2)
    img = img.reshape(1, -1)
    return img


def shift_up(img):
    img = img.reshape(28, 28)
    img = np.rot90(img)
    img = np.roll(img, -2)
    img = np.rot90(img, 3)
    img = img.reshape(1, -1)
    return img


def shift_down(img):
    img = img.reshape(28, 28)
    img = np.rot90(img)
    img = np.roll(img, 2)
    img = np.rot90(img, 3)
    img = img.reshape(1, -1)
    return img


X_backup = X.copy()

images, labels = X[:200].copy(), y[:200]  # change number of values being process

print(images.shape, labels.shape)

# from concurrent.futures import ThreadPoolExecutor

# def augmentation(img, lab):
#     np.append(X, shift_right(img), axis=0)
#     np.append(y, lab)
#     np.append(X, shift_left(img), axis=0)
#     np.append(y, lab)
#     np.append(X, shift_up(img), axis=0)
#     np.append(y, lab)
#     np.append(X, shift_down(img), axis=0)
#     np.append(y, lab)

# with ThreadPoolExecutor() as ex:
#     ex.map(augmentation, args=[img, lab])

for i in range(len(images)):
    img, lab = images[i], labels[i]

    images = np.append(images, shift_right(img), axis=0)
    labels = np.append(labels, lab)
    images = np.append(images, shift_left(img), axis=0)
    labels = np.append(labels, lab)
    images = np.append(images, shift_up(img), axis=0)
    labels = np.append(labels, lab)
    images = np.append(images, shift_down(img), axis=0)
    labels = np.append(labels, lab)

    print(f">>>>> END {i} <<<<<<<")

print(images.shape, labels.shape)

number = 78
plt.imshow(images[number].reshape(28, 28))
plt.show()
print(labels[number])
