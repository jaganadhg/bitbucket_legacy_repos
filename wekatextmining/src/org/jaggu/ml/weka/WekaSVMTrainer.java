package org.jaggu.ml.weka;

import java.io.File;
import weka.classifiers.functions.LibSVM;
import weka.core.Instances;
import weka.core.SelectedTag;
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

public class WekaSVMTrainer {
	/**
	 * @param args
	 * @throws Exception 
	 */
	
	public static void buildSVMClassifier(String strDirPath) throws Exception{
		NGramTokenizer ngt = new NGramTokenizer();
		ngt.setNGramMaxSize(3);
		TextDirectoryLoader tdl = new TextDirectoryLoader();
		tdl.setDirectory(new File(strDirPath));
		Instances instances = tdl.getDataSet();
		StringToWordVector stwv = new StringToWordVector();
		stwv.setTokenizer(ngt);
		stwv.setTFTransform(true);
		stwv.setIDFTransform(true);
		stwv.setStopwords(new File("/usr/share/nltk_data/corpora/stopwords/english"));
		stwv.setLowerCaseTokens(true);
		stwv.setInputFormat(instances);
		
		Instances filterdInstances = Filter.useFilter(instances, stwv);
		
		LibSVM svm = new LibSVM();
		SelectedTag kt = new SelectedTag(0, LibSVM.TAGS_KERNELTYPE);
		SelectedTag svmt = new SelectedTag(0, LibSVM.TAGS_SVMTYPE);
		svm.setKernelType(kt);
		svm.setSVMType(svmt);
		svm.setProbabilityEstimates(true);
		svm.buildClassifier(filterdInstances);
		System.out.println(svm);
		SerializationHelper sh = new SerializationHelper();
		sh.write("SVM_NG_3_Movie.model", svm);
	}

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		String strDirPath = "/usr/share/nltk_data/corpora/movie_reviews";
		buildSVMClassifier(strDirPath);

	}

}
