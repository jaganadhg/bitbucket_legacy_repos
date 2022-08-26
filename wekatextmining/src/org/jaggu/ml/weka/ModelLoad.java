package org.jaggu.ml.weka;

import weka.classifiers.bayes.NaiveBayes;
import weka.core.SerializationHelper;

public class ModelLoad {
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void loadModel(String strModelPath) throws Exception{
		SerializationHelper sh = new SerializationHelper();
		NaiveBayes nb = (NaiveBayes) sh.read(strModelPath);
		
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
