package org.jaggu.ml.weka;

/**
 * @author Jaganadh G
 * @mail jaganadhg@gmail.com
 * @home http://jaganadhg.in
 * @credits David Sharpe through weka-list 
 */
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;

public class StringToInstance {

	/**
	 * @param {String} strDocument
	 * @return {@Instances} filtered_vect
	 * @throws Exception
	 */

	public static Instances createInstance(String strDocument) throws Exception {
		// Declaring class attributes with values
		FastVector class_labels = new FastVector(2);
		class_labels.addElement("pos");
		class_labels.addElement("neg");
		Attribute label = new Attribute("classLabel", class_labels);

		// Declare text attribute
		Attribute strText = new Attribute("text", (FastVector) null);

		// Create instance schema
		FastVector test_vect = new FastVector();
		test_vect.addElement(label);
		test_vect.addElement(strText);
		
		//Create instance and set schema
		Instances instances = new Instances("data", test_vect, 1);
		instances.setClassIndex(0);

		Instance instance = new Instance(2);
		instance.setValue(strText, strDocument);
		instance.setValue(label, "pos");
		instances.add(instance);

		//Use StringToWordVector to build a bag of words (word frequency).
		StringToWordVector vectorizer = new StringToWordVector();
		vectorizer.setLowerCaseTokens(true);
		vectorizer.setUseStoplist(true);
		vectorizer.setTFTransform(true);
		vectorizer.setIDFTransform(true);
		vectorizer.setInputFormat(instances);

		Instances filtered_vect = Filter.useFilter(instances, vectorizer);

		System.out.println(filtered_vect.toSummaryString());

		return filtered_vect;

	}

	/**
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		String strInput = "The Dooms Day is a good filim. I like the plot and directon of the movie. It is a must watch movie.";
		createInstance(strInput);

	}

}
