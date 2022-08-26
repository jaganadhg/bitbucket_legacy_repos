package org.jb.ml.dc.weka;

import weka.classifiers.Classifier;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.SerializationHelper;
import weka.core.tokenizers.NGramTokenizer;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;

/**
 * Author: Jaganadh G(jaganadg@gmail.com), Biju B(bijubkbk@gmail.com)
 * Date: 11/21/12
 * Time: 4:54 PM
 */

public class DocumentClassifier {


    private Instances trainingData;
    private Classifier classifier;
    private Preprocessor preprocessor;
    
    private StringToWordVector vectorizer;
    private NGramTokenizer tokenizer;

    public DocumentClassifier(String strModel, String strData) throws Exception {
    	preprocessor = new Preprocessor();
    	classifier = (Classifier) SerializationHelper.read(strModel);
    	trainingData = (Instances) SerializationHelper.read(strData);
    	
    	vectorizer = new StringToWordVector();
    	tokenizer = new NGramTokenizer();
    	
    	vectorizer.setLowerCaseTokens(true);
        vectorizer.setUseStoplist(true);
        vectorizer.setTokenizer(tokenizer);
        vectorizer.setTFTransform(true);
        vectorizer.setIDFTransform(true);
        vectorizer.setInputFormat(trainingData);
        Filter.useFilter(trainingData, vectorizer);

    }



    
    public String classify(String strText) throws Exception{
    	
    	String label = "None";
    	
    	Instance testInstance = preprocessor.makeInstance(strText, trainingData);
    	vectorizer.input(testInstance);
    	
    	Instance filteredVector = vectorizer.output();
    	
    	double result = classifier.classifyInstance(filteredVector);
    	
    	label = trainingData.classAttribute().value((int) result);
    	
    	
    	return label;
    }

}
