package org.jaggu.bd.mahout;

import java.io.IOException;
import java.io.StringReader;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.util.Version;
import org.apache.mahout.classifier.naivebayes.AbstractNaiveBayesClassifier;
import org.apache.mahout.classifier.naivebayes.NaiveBayesModel;
import org.apache.mahout.classifier.naivebayes.StandardNaiveBayesClassifier;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.math.Vector;
import org.apache.mahout.vectorizer.encoders.FeatureVectorEncoder;
import org.apache.mahout.vectorizer.encoders.StaticWordValueEncoder;

public class NaiveBayesClassifierExample {

	public static void loadClassifier(String strModelPath, Vector v)
			throws IOException {
		Configuration conf = new Configuration();

		NaiveBayesModel model = NaiveBayesModel.materialize(new Path(
				strModelPath), conf);
		AbstractNaiveBayesClassifier classifier = new StandardNaiveBayesClassifier(
				model);

		Vector st = classifier.classifyFull(v);
		
		System.out.println(st.toString());
		
	}

	public static Vector createVect() throws IOException {
		FeatureVectorEncoder encoder = new StaticWordValueEncoder("text");
		Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_36);
		StringReader in = new StringReader(
				"The movie sherk was very cool and attractive one. We like the movie"
						+ "because of the theme and directon. All the actores were excellent");

		TokenStream ts = analyzer.tokenStream("body", in);

		CharTermAttribute termAtt = ts.addAttribute(CharTermAttribute.class);
		Vector v1 = new RandomAccessSparseVector(100000);

		while (ts.incrementToken()) {
			char[] termBuffer = termAtt.buffer();
			int termLen = termAtt.length();
			String w = new String(termBuffer, 0, termLen);
			encoder.addToVector(w, 1.0, v1);
		}
		
		v1.normalize();
		return v1;
	}

	public static void main(String[] args) throws IOException {
		Vector v = createVect();
		String mp = "/home/u179995/Downloads/mahout-distribution-0.7/playg/movie_model";
		loadClassifier(mp, v);
	}
}
