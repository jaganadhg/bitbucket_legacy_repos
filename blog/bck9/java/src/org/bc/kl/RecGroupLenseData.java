package org.bc.kl;

import java.io.File;
import java.util.List;

import org.apache.mahout.cf.taste.example.grouplens.GroupLensDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

public class RecGroupLenseData {

    public static List<RecommendedItem> groupLenseRec() throws Exception {
	DataModel gldm = new GroupLensDataModel(
		new File(
			"/home/jaganadhg/backup/jaganadhg/Desktop/hate-training-new/million-ml-data.tar__0_FILES/ratings.dat"));
	//UserSimilarity usim = new PearsonCorrelationSimilarity(gldm);
	UserSimilarity usim = new LogLikelihoodSimilarity(gldm);
	// UserSimilarity usim = new EuclideanDistanceSimilarity(gldm);
	// ThresholdUserNeighborhood usima = new ThresholdUserNeighborhood(0.7,
	// usim, gldm);
	UserNeighborhood unigh = new NearestNUserNeighborhood(100, usim, gldm);
	Recommender recommender = new GenericUserBasedRecommender(gldm, unigh,
		usim);
	List<RecommendedItem> recommendation = recommender.recommend(10, 100);
	return recommendation;

    }

    public static void main(String[] args) throws Exception {

	List<RecommendedItem> br = groupLenseRec();

	for (RecommendedItem rec : br) {
	    System.out.println(rec);
	}
	System.out.println("User Based");

    }

}
