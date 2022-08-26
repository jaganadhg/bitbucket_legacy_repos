package org.jaggu.ml.weka;

import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;

public class InstanceEx {
		
	/**
	 * @param String strDoc
	 * @return {@link Instances} filterd_data
	 * @throws Exception 
	 */
	
	public static Instances preprocess(String strDoc) throws Exception{
		Attribute test_str = new Attribute("test", (FastVector) null);
		FastVector fv = new FastVector();
		fv.addElement(test_str);
		Instances test_inst = new Instances("test", fv, 1);
		test_inst.add(new Instance(1));
		test_inst.instance(0).setValue(0, strDoc);
		
		StringToWordVector vectorizer = new StringToWordVector();
		vectorizer.setLowerCaseTokens(true);
		vectorizer.setUseStoplist(true);
		vectorizer.setTFTransform(true);
		vectorizer.setIDFTransform(true);
		vectorizer.setInputFormat(test_inst);
		
		Instances filterd_data = Filter.useFilter(test_inst, vectorizer);
		System.out.println(filterd_data.toSummaryString());
		return filterd_data;		
	}
	
	

	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		String str = "this is a good string";
		preprocess(str);

	}

}
