package org.jb.ml.dc.weka;

import java.io.File;

import weka.core.Attribute;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.SerializationHelper;
import weka.core.converters.TextDirectoryLoader;
import weka.core.tokenizers.NGramTokenizer;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;
/**
 * Author: Jaganadh G(jaganadg@gmail.com), Biju B(bijubkbk@gmail.com)
 * Date: 11/21/12
 * Time: 4:54 PM
 */
public class Preprocessor {
	
    private NGramTokenizer tokenizer;
    private TextDirectoryLoader dataLoader;
    private StringToWordVector vectorizer;
    //private Instances trainingData;
    
    
    /**
     * @param strText
     *            ,instData
     * @throws
     * @return instance
     */

    public Instance makeInstance(String strText, Instances instData) {

        int cIdx = instData.numAttributes() - 1;
        instData.setClassIndex(cIdx);

        Instance instance = new Instance(2);

        Attribute messageAtt = instData.attribute("text");
        instance.setValue(messageAtt, messageAtt.addStringValue(strText));

        instance.setDataset(instData);
        instance.setClassMissing();

        return instance;
    }

    /**
     * @param inst
     *            , i_NgramSize
     * @throws Exception
     * @return
     */
    public void filterer(Instances inst, int i_NgramSize) throws Exception {

        tokenizer = new NGramTokenizer();
        tokenizer.setNGramMaxSize(i_NgramSize);

        vectorizer = new StringToWordVector();
        vectorizer.setLowerCaseTokens(true);
        vectorizer.setUseStoplist(true);
        vectorizer.setTokenizer(tokenizer);
        vectorizer.setTFTransform(true);
        vectorizer.setIDFTransform(true);

        vectorizer.setInputFormat(inst);
        Filter.useFilter(inst, vectorizer);
    }

    /**
     * @param inst
     *            , i_NgramSize
     * @throws Exception
     * @return
     */
    public void filtererTK(Instances inst, int i_NgramSize) throws Exception {

        tokenizer = new NGramTokenizer();
        tokenizer.setNGramMaxSize(i_NgramSize);

        vectorizer = new StringToWordVector();
        vectorizer.setLowerCaseTokens(true);
        vectorizer.setUseStoplist(true);
        vectorizer.setTokenizer(tokenizer);
        vectorizer.setOutputWordCounts(false);

        vectorizer.setInputFormat(inst);
        Filter.useFilter(inst, vectorizer);
    }
    
    /**
     * @param strTrainingDir
     *            ,strModelName, i_Ngram_Size
     * @return preProcessedData
     * @throws Exception
     */

    public Instances genericPreprocess(String strTrainingDir,
                                        String strModelName, int i_Ngram_Size) throws Exception {
        tokenizer = new NGramTokenizer();
        tokenizer.setNGramMaxSize(i_Ngram_Size);

        dataLoader = new TextDirectoryLoader();
        dataLoader.setDirectory(new File(strTrainingDir));

        Instances trainingData = dataLoader.getDataSet();

        vectorizer = new StringToWordVector();
        vectorizer.setLowerCaseTokens(true);
        vectorizer.setUseStoplist(true);
        vectorizer.setTokenizer(tokenizer);
        vectorizer.setTFTransform(true);
        vectorizer.setIDFTransform(true);
        vectorizer.setInputFormat(trainingData);

        Instances preProcessedData = Filter.useFilter(trainingData, vectorizer);

        SerializationHelper.write(strModelName + ".instances", trainingData);

        return preProcessedData;
    }

    /**
     * @param strTrainingDir
     *            ,strModelName, i_Ngram_Size
     * @return preProcessedData
     * @throws Exception
     */

    public Instances textKernalPreProcess(String strTrainingDir,
                                           String strModelName, int i_Ngram_Size) throws Exception {

        tokenizer = new NGramTokenizer();
        tokenizer.setNGramMaxSize(i_Ngram_Size);

        dataLoader = new TextDirectoryLoader();
        dataLoader.setDirectory(new File(strTrainingDir));

        Instances trainingData = dataLoader.getDataSet();

        vectorizer = new StringToWordVector();
        vectorizer.setLowerCaseTokens(true);
        vectorizer.setUseStoplist(true);
        vectorizer.setTokenizer(tokenizer);
        vectorizer.setOutputWordCounts(false);
        vectorizer.setInputFormat(trainingData);

        Instances preProcessedData = Filter.useFilter(trainingData, vectorizer);

        SerializationHelper.write(strModelName + ".instances", trainingData);

        return preProcessedData;

    }

}
