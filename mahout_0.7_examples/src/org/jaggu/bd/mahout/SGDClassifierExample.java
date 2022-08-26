package org.jaggu.bd.mahout;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.ngram.NGramTokenFilter;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.util.Version;
import org.apache.mahout.classifier.sgd.AdaptiveLogisticRegression;
import org.apache.mahout.classifier.sgd.CrossFoldLearner;
import org.apache.mahout.classifier.sgd.L1;
import org.apache.mahout.classifier.sgd.ModelSerializer;
import org.apache.mahout.common.RandomUtils;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.math.Vector;
import org.apache.mahout.vectorizer.encoders.ConstantValueEncoder;
import org.apache.mahout.vectorizer.encoders.Dictionary;
import org.apache.mahout.vectorizer.encoders.FeatureVectorEncoder;
import org.apache.mahout.vectorizer.encoders.StaticWordValueEncoder;
import org.apache.mahout.vectorizer.encoders.TextValueEncoder;

import com.google.common.collect.HashMultiset;

public class SGDClassifierExample {

	@SuppressWarnings({ "unchecked", "rawtypes" })
	public static Set<Set> words_stop = new HashSet(
			Arrays.asList(StandardAnalyzer.STOP_WORDS_SET));

	public static  int features = 10000;
	public static StandardAnalyzer analyzer = new StandardAnalyzer(
			Version.LUCENE_36, words_stop);
	public static TextValueEncoder encoder = new TextValueEncoder("body");
	public static ConstantValueEncoder line = new ConstantValueEncoder("line");
	public static ConstantValueEncoder loglines = new ConstantValueEncoder(
			"log(line)");
	public static ConstantValueEncoder bias = new ConstantValueEncoder(
			"intercept");
	public static Random rand = RandomUtils.getRandom();
	
	
	public static Vector createVect() throws IOException {
		FeatureVectorEncoder encoder = new StaticWordValueEncoder("text");
		Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_36);
		StringReader in = new StringReader(
				"The movie sherk was very cool and attractive one. We like the movie"
						+ "because of the theme and directon. All the actores were excellent");

		TokenStream ts = analyzer.tokenStream("body", in);
		
		NGramTokenFilter ngt = new NGramTokenFilter(ts, 1, 3);

		CharTermAttribute termAtt = ts.addAttribute(CharTermAttribute.class);
		CharTermAttribute termAtta = ngt.addAttribute(CharTermAttribute.class);
		Vector v1 = new RandomAccessSparseVector(10000);

		while (ngt.incrementToken()) {
			char[] termBuffer = termAtta.buffer();
			int termLen = termAtta.length();
			String w = new String(termBuffer, 0, termLen);
			encoder.addToVector(w, 1, v1);
		}
		
		v1.normalize();
		return v1;
	}

	public static void main(String[] args) throws IOException {
		String data = "/home/u179995/my_corpora";
		String model = "/home/u179995/SGDT/mov.model";
		String dict = "/home/u179995/SGDT/mov.dict";

		trainSGD(data, model, dict);
	}

	public static void trainSGD(String strTrainPath, String strModelPath,
			String strDictFile) throws IOException {
		Dictionary dictionary = new Dictionary();
		//OnlineLogisticRegression olr = new OnlineLogisticRegression(numCategories, numFeatures, prior);
		AdaptiveLogisticRegression learningalgo = new AdaptiveLogisticRegression(
				20, features, new L1());
		learningalgo.setInterval(800);
		learningalgo.setAveragingWindow(500);
		ArrayList<File> files = new ArrayList<File>();
		File[] dir = new File(strTrainPath).listFiles();

		for (File file : dir) {
			if (file.isDirectory()) {
				dictionary.intern(file.getName());
				for (File f : file.listFiles()) {
					files.add(f);
				}
			}
		} 
		Collections.shuffle(files);
		System.out.println(files.size() + " files " + dir.length + " class ");

		for (File file : files) {
			String ng = file.getParentFile().getName();
			int actualClass = dictionary.intern(ng);
			RandomAccessSparseVector vector = ecodeFeatureVect(file);
			learningalgo.train(actualClass, vector);

		}

		learningalgo.close();

		CrossFoldLearner learner = learningalgo.getBest().getPayload()
				.getLearner();
		System.out.println("AUC=" + learner.auc() + ", %-correct="
				+ learner.percentCorrect()+ " MMMM " + learner.validModel());
		ModelSerializer.writeBinary(strModelPath, learner.getModels().get(0));
		PrintWriter serializedDict = new PrintWriter(strDictFile);
		for (String dict : dictionary.values()) {
			serializedDict.println(dict);
		}
		serializedDict.flush();
		serializedDict.close();
		
		Vector k = createVect();
		Map<Integer, String> mylabels = getCatLables(strDictFile);
		//learner.
		
		System.out.println(learner.classify(k).maxValueIndex() + " " + mylabels.get(learner.classify(k).maxValueIndex()));

	}

	public static RandomAccessSparseVector ecodeFeatureVect(File file)
			throws IOException {
		RandomAccessSparseVector vector = new RandomAccessSparseVector(features);
		HashMultiset<String> words = HashMultiset.create();
		int numlines = 0;
		
		FileReader fr = new FileReader(file);
		BufferedReader br = new BufferedReader(fr);
		String lines = "";

		while ((lines = br.readLine()) != null) {
			coutWords(lines, words);
			numlines += 1;
		}

		bias.addToVector("", 1, vector);
		line.addToVector("", numlines / 30, vector);
		loglines.addToVector("", Math.log(numlines) + 1, vector);

		for (String word : words) {
			encoder.addToVector(word, Math.log(1 + words.count(word)), vector);
		}

		return vector;
	}

	public static void coutWords(String line, HashMultiset<String> words)
			throws IOException {
		ArrayList<String> wordsa = new ArrayList<String>();
		TokenStream tokenstream = analyzer.tokenStream("text",
				new StringReader(line));
		tokenstream.addAttribute(CharTermAttribute.class);
		
		NGramTokenFilter nngtf = new NGramTokenFilter(tokenstream, 1, 3);
		nngtf.addAttribute(CharTermAttribute.class);
		while (nngtf.incrementToken()) {
			CharTermAttribute attr = tokenstream
					.addAttribute(CharTermAttribute.class);
			wordsa.add(new String(attr.buffer(), 0, attr.length()));
		}

	}
	
	public static Map<Integer, String> getCatLables(String strLabelFileName) throws IOException{
		Map<Integer,String> lables = new HashMap<Integer, String>();
		FileReader ffr = new FileReader(new File(strLabelFileName));
		BufferedReader bbur = new BufferedReader(ffr);
		int lineno = 0;
		String l = "";
		while((l = bbur.readLine()) != null){
			//System.out.println(l);
			lables.put(lineno, l);
			lineno += 1;
		}
		return lables;
	}

}
