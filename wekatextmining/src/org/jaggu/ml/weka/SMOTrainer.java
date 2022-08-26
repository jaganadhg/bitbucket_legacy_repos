package org.jaggu.ml.weka;

import java.io.File;
import java.io.IOException;

import weka.classifiers.Classifier;
import weka.classifiers.functions.SMO;
import weka.classifiers.functions.supportVector.PolyKernel;
import weka.classifiers.functions.supportVector.RBFKernel;
import weka.classifiers.functions.supportVector.StringKernel;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.SelectedTag;
import weka.core.converters.TextDirectoryLoader;
import weka.core.tokenizers.NGramTokenizer;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;

public class SMOTrainer {
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void trainSMO(String strDataPath) throws Exception{
		//Tokenizer
		NGramTokenizer tokenizer = new NGramTokenizer();
		tokenizer.setNGramMinSize(1);
		tokenizer.setNGramMaxSize(3);
		
		//Text Directory Loader
		
		TextDirectoryLoader dirloader = new TextDirectoryLoader();
		dirloader.setCharSet("UTF-8");
		
		dirloader.setDirectory(new File(strDataPath));
		Instances rawData = dirloader.getDataSet();
		System.out.println(rawData.numAttributes());
		
		//Vectorizer
		StringToWordVector vectorizer = new StringToWordVector();
		vectorizer.setLowerCaseTokens(true);
		vectorizer.setUseStoplist(true);
		vectorizer.setTFTransform(true);
		vectorizer.setIDFTransform(true);
		vectorizer.setInputFormat(rawData);
		
		
		Instances filteredDate = Filter.useFilter(rawData, vectorizer);
		
		SMO smosvm = new SMO();
		//RBFKernel kernal = new RBFKernel();
		PolyKernel kernal = new PolyKernel();
		smosvm.setKernel(kernal);
		
		smosvm.buildClassifier(filteredDate);
		
		System.out.println(kernal);
		
	}

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		String strTrainingData = "/usr/share/nltk_data/corpora/movie_reviews";
		trainSMO(strTrainingData);

	}

}
