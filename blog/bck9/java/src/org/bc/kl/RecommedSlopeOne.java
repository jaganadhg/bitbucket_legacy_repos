package org.bc.kl;

import java.io.File;
import java.util.List;

import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.recommender.slopeone.SlopeOneRecommender;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;

import com.sun.org.apache.xalan.internal.xsltc.runtime.Hashtable;

public class RecommedSlopeOne {

    public static Recommender slopOneRecommender() throws Exception {
	DataModel dm = new FileDataModel(new File(
		"/home/jaganadhg/Desktop/bck9/pci.csv"));
	Recommender recommender = new SlopeOneRecommender(dm);

	//List<RecommendedItem> recommendation = recommender.recommend(1, 1);

	return recommender;

    }

    /**
     * @param args
     * @throws Exception
     */
    public static void main(String[] args) throws Exception {
    	
    	GetData data = new GetData();
        
        Hashtable userData = data.getUserData();
        Hashtable moveData = data.getMovieData();
	
	Recommender br = slopOneRecommender();
	List<RecommendedItem> recommendation = br.recommend(1, 1);

	for (RecommendedItem rec : recommendation) {
	    //System.out.println(rec);
	    long itemId = rec.getItemID();
	    String item = Long.toString(itemId);
	    String movieName = (String) moveData.get(item);
	    System.out.println("Recommended movie for " + (String) userData.get("1") + " is " +movieName);
	}

    }

}
