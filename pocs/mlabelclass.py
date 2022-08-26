#!/usr/bin/env python
import numpy as np

from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.datasets import load_svmlight_file
from sklearn import metrics


def get_data(data_file):
	x,y = load_svmlight_file(data_file,multilabel=True)
	return x,y

def build_classifier(x,y):
	classifier = OneVsRestClassifier(LinearSVC(random_state=0),n_jobs=-1)
	label_binarizer = LabelBinarizer()
	y = label_binarizer.fit_transform(y)
	model = classifier.fit(x,y)
	return model

if __name__ == "__main__":
	X_train,Y_train = get_data("wise2014-train.libsvm")
	X_test,Y_test = get_data("wise2014-test.libsvm")
	Y_test = LabelBinarizer().fit_transform(Y_test)
	#Y_test = Y_test.astype(str)
	model = build_classifier(X_train,Y_train)
	classified = model.predict(X_test)
	print metrics.f1_score(Y_test,classified,average='macro')
	
