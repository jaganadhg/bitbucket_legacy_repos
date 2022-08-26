package org.jb.ml.dc.weka;

import weka.classifiers.Classifier;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.bayes.NaiveBayesMultinomial;
import weka.classifiers.bayes.NaiveBayesSimple;
import weka.classifiers.functions.LibSVM;
import weka.classifiers.functions.SMO;
import weka.classifiers.functions.supportVector.*;
import weka.core.Instances;
import weka.core.SelectedTag;
import weka.core.SerializationHelper;

/**
 * Author: Jaganadh G(jaganadg@gmail.com), Biju B(bijubkbk@gmail.com)
 * Date: 11/21/12
 * Time: 4:54 PM
 */


public class Trainer {

	private Classifier classifier;
    private Kernel kernal;
    private LibSVM svm_classifier;
    private SMO smo_svm;
    private Preprocessor preprocessor;

    public Trainer() {
    	preprocessor = new Preprocessor();

    }



    /**
     * @param strDataDir
     *            ,ModelName,i_ng_size, strNBType
     * @throws Exception
     */

    public void naiveBayesTrainer(String strDataDir, String strModelName,
                                  int i_ng_size, String strNBType) throws Exception {

        if (strNBType.equalsIgnoreCase("smiple")) {
            classifier = new NaiveBayesSimple();
        } else if (strNBType.equalsIgnoreCase("mnomial")) {
            classifier = new NaiveBayesMultinomial();
        } else if (strNBType.equalsIgnoreCase("base")) {
            classifier = new NaiveBayes();
        } else {
            System.err.println("Naive Bayes Opetion is not valid. You selected"
                    + strNBType);
        }

        Instances data = preprocessor.genericPreprocess(strDataDir, strModelName, i_ng_size);
        classifier.buildClassifier(data);

        SerializationHelper.write(strModelName + ".model", classifier);
    }

    /**
     * @param strDataDir
     *            ,ModelName,i_ng_size
     * @throws Exception
     */

    public void trainSMOStringKernal(String strDataDir, String strModelName,
                                     int i_ng_size) throws Exception {

        classifier = new SMO();
        kernal = new StringKernel();

        Instances data = preprocessor.textKernalPreProcess(strDataDir, strModelName,
                i_ng_size);

        kernal.buildKernel(data);
        classifier.buildClassifier(data);

        SerializationHelper.write(strModelName + ".model", classifier);
    }

    /**
     * @param strDataDir
     *            ,ModelName,i_ng_size
     * @throws Exception
     */

    public void trainSVM(String strTrainDir, String strModelName,
                         int i_ngram_size) throws Exception {

        svm_classifier = new LibSVM();

        SelectedTag kernal_type = new SelectedTag(0, LibSVM.TAGS_KERNELTYPE);
        SelectedTag svm_type = new SelectedTag(0, LibSVM.TAGS_SVMTYPE);

        svm_classifier.setKernelType(kernal_type);
        svm_classifier.setSVMType(svm_type);
        svm_classifier.setProbabilityEstimates(true);

        Instances data = preprocessor.genericPreprocess(strTrainDir, strModelName,
                i_ngram_size);

        svm_classifier.buildClassifier(data);
        SerializationHelper.write(strModelName + ".model", svm_classifier);

    }

    /**
     * @param strDataDir
     *            ,ModelName,i_ng_size,strKernalType
     * @throws Exception
     */

    public void traimSMO(String strTrainDir, String strModelName,
                         int i_ngram_size, String strKernalType) throws Exception {

        if (strKernalType.equalsIgnoreCase("rbf")) {
            kernal = new RBFKernel();
        } else if (strKernalType.equalsIgnoreCase("poly")) {
            kernal = new PolyKernel();
        } else if (strKernalType.equalsIgnoreCase("npoly")) {
            kernal = new NormalizedPolyKernel();
        } else {
            System.err.println("Kernal option not valid. You selected "
                    + strKernalType);
        }

        smo_svm = new SMO();

        Instances data = preprocessor.genericPreprocess(strTrainDir, strModelName,
                i_ngram_size);

        kernal.buildKernel(data);
        smo_svm.setKernel(kernal);
        smo_svm.buildClassifier(data);
        SerializationHelper.write(strModelName + ".model", smo_svm);

    }

    public static void main(String[] args){
        //TODO Add option handling , Use Logger.Test
    }

}

