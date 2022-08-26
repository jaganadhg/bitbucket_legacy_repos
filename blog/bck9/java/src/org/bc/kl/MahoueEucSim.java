package org.bc.kl;

import java.io.File;
import java.util.List;

import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.SpearmanCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

import com.sun.org.apache.xalan.internal.xsltc.runtime.Hashtable;

public class MahoueEucSim {
	public static Recommender seteuRecommener() throws Exception{
		DataModel dm = new FileDataModel(new File(
		"/home/jaganadhg/Desktop/bck9/pci.csv"));
		UserSimilarity us = new SpearmanCorrelationSimilarity(dm);
		UserNeighborhood un = new NearestNUserNeighborhood(2, us, dm);
		//Recommender recommender = new GenericUserBasedRecommender(dm, un, us);
		Recommender recommender = new GenericUserBasedRecommender(dm, un, us);
		return recommender;
		
	}

	 public static void main(String[] args) throws Exception {
	    	
		    GetData data = new GetData();
		    
		    Hashtable userData = data.getUserData();
		    Hashtable moveData = data.getMovieData();
		    //Enumeration userids = userData.keys();
		    
		    

			Recommender br = seteuRecommener();
			List<RecommendedItem> recommendation = br.recommend(5, 3);
			

			for (RecommendedItem rec : recommendation) {
			    //System.out.println(rec);
			    long itemId = rec.getItemID();
			    String item = Long.toString(itemId);
			    String movieName = (String) moveData.get(item);
			    System.out.println("Recommended movie for " + (String) userData.get("5") + " is " +movieName);
			}

		    }
}
