/**
 * 
 */
package org.jaggu.ml.weka;

import java.io.File;
import weka.classifiers.bayes.NaiveBayes;
import weka.core.Instances;
import weka.core.SerializationHelper;
import weka.core.converters.TextDirectoryLoader;
import weka.core.tokenizers.NGramTokenizer;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;

/**
 * @author Jaganadh G
 * @mail jaganadhg@gmail.com
 * @home http://jaganadhg.in
 * 
 */
public class ClassifierExample {
	/**
	 * @param args
	 * @throws Exception 
	 */

	public static void createClassifier(String strDirPath) throws Exception {
		NGramTokenizer ngt = new NGramTokenizer();
		ngt.setNGramMaxSize(3);
		TextDirectoryLoader loader = new TextDirectoryLoader();
		loader.setCharSet("UTF-8");
		loader.setDirectory(new File(strDirPath));
		Instances rawData = loader.getDataSet();
		System.out.println(rawData.numInstances());
		StringToWordVector stv = new StringToWordVector();
		stv.setIDFTransform(true);
		stv.setLowerCaseTokens(true);
		stv.setStopwords(new File("/home/u179995/english"));
		stv.setTFTransform(true);
		stv.setTokenizer(ngt);
		stv.setInputFormat(rawData);
		Instances filteredData = Filter.useFilter(rawData, stv);
		
		NaiveBayes classifier = new NaiveBayes();
		classifier.buildClassifier(filteredData);
		//System.out.println(classifier.toString());
		//System.out.println(classifier);
		SerializationHelper clsfwriter = new SerializationHelper();
		clsfwriter.write("/home/u179995/Desktop/nm_ng.model", classifier);
		
	}

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		String strTrainingData = "/usr/share/nltk_data/corpora/movie_reviews";
		createClassifier(strTrainingData);

	}

}
