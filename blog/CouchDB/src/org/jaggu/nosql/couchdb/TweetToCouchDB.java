package org.jaggu.nosql.couchdb;

import java.util.List;

import com.fourspaces.couchdb.Database;
import com.fourspaces.couchdb.Document;
import com.fourspaces.couchdb.Session;

import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Tweet;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;

public class TweetToCouchDB {

	/**
	 * @param strQuery
	 * @throws TwitterException
	 * @return queryResult
	 */

	public static QueryResult getTweets(String strQuery)
			throws TwitterException {
		Twitter twitter = new TwitterFactory().getInstance();
		Query query = new Query(strQuery);
		QueryResult queryResult = twitter.search(query);
		return queryResult;

	}

	/**
	 * @param strDBName
	 * @return dbCouchDB
	 */

	public static Database connectCouchDB(String strDBName) {
		Database dbCouchDB = null;
		Session dbCouchDBSession = new Session("localhost", 5984);
		List<String> databases = dbCouchDBSession.getDatabaseNames();
		if (databases.contains(strDBName)) {
			dbCouchDB = dbCouchDBSession.getDatabase(strDBName);
		} else {
			dbCouchDBSession.createDatabase(strDBName);
			dbCouchDB = dbCouchDBSession.getDatabase(strDBName);
		}

		return dbCouchDB;

	}

	/**
	 * @param tweet
	 * @return couchDocument
	 */

	@SuppressWarnings("deprecation")
	public static Document tweetToCouchDocument(Tweet tweet) {

		Document couchDocument = new Document();

		couchDocument.setId(String.valueOf(tweet.getId()));
		couchDocument.put("Tweet", tweet.getText().toString());
		couchDocument.put("UserName", tweet.getFromUser().toString());
		couchDocument.put("Time", tweet.getCreatedAt().toGMTString());
		couchDocument.put("URL", tweet.getSource().toString());

		return couchDocument;

	}

	/**
	 * @param tweetQury
	 * @param dbName
	 * @throws TwitterException
	 */

	public static void writeTweetToCDB(String strTweetQury, String strdbName)
			throws TwitterException {
		QueryResult tweetResults = getTweets(strTweetQury);
		Database dbInstance = connectCouchDB(strdbName);
		dbInstance.getAllDocuments();
		for (Tweet tweet : tweetResults.getTweets()) {
			Document document = tweetToCouchDocument(tweet);
			dbInstance.saveDocument(document);
		}

	}

	/**
	 * @param args
	 * @throws TwitterException
	 */
	public static void main(String[] args) throws TwitterException {
		String query = "java";
		String dbName = "javatweets";
		System.out.println("Started");
		writeTweetToCDB(query, dbName);
		System.out.println("Finished");

	}

}
