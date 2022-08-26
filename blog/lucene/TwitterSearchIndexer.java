/**
 * 
 */
package org.jaggu.nlp.search;

import java.io.File;
import java.io.IOException;

import org.apache.lucene.analysis.LimitTokenCountAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Tweet;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;

/**
 * @author jaganadhg
 * 
 */
public class TwitterSearchIndexer {
	private IndexWriter writer;

	/**
	 * @param Query
	 *            to get tweets
	 * @throws TwitterException
	 *             Method to get tweets for a particular keyword
	 */

	public static QueryResult getTweets(String strTweetQuerry)
			throws TwitterException {
		Twitter twitter = new TwitterFactory().getInstance();
		Query query = new Query(strTweetQuerry);
		QueryResult result = twitter.search(query);
		return result;
	}

	/**
	 * @param Tweets
	 *            Converts tweets and metadata to Lucene Document format
	 */
	protected Document tweet2Doc(Tweet tweet) {
		Document tweetDoc = new Document();
		tweetDoc.add(new Field("tweet", tweet.getText().toString(),
				Field.Store.YES, Field.Index.ANALYZED));
		tweetDoc.add(new Field("user", tweet.getFromUser().toString(),
				Field.Store.YES, Field.Index.NOT_ANALYZED));
		tweetDoc.add(new Field("time", tweet.getCreatedAt().toString(),
				Field.Store.YES, Field.Index.NOT_ANALYZED));
		tweetDoc.add(new Field("url", tweet.getSource().toString(),
				Field.Store.YES, Field.Index.NOT_ANALYZED));

		return tweetDoc;
	}

	/**
	 * @param allResult
	 *            - result obtained for twitter search
	 * @throws CorruptIndexException
	 * @throws IOException
	 *             Indexes the tweets
	 */

	public void indexTweets(QueryResult allResult)
			throws CorruptIndexException, IOException {
		for (Tweet tweet : allResult.getTweets()) {

			Document docForIndex = tweet2Doc(tweet);
			writer.addDocument(docForIndex);

		}

	}

	/**
	 * to close the index writer
	 * 
	 */
	public void close() throws IOException {
		System.out.println("Total number of tweets in the Index : "
				+ writer.numDocs());
		writer.optimize();
		writer.close();
	}

	/**
	 * @throws IOException
	 * 
	 */

	public TwitterSearchIndexer(String indexDir) throws IOException {
		Directory dir = FSDirectory.open(new File(indexDir));
		IndexWriterConfig idxconfa = new IndexWriterConfig(Version.LUCENE_30,
				new LimitTokenCountAnalyzer(new StandardAnalyzer(
						Version.LUCENE_30), 1000000000));
		writer = new IndexWriter(dir, idxconfa);
	}

	/**
	 * @param args
	 * @throws TwitterException
	 * @throws Exception
	 */
	public static void main(String[] args) throws TwitterException, Exception {
		String indexDir = args[0];
		String strTwitterQueryString = args[1];
		TwitterSearchIndexer lia = new TwitterSearchIndexer(indexDir);
		System.out.println("Searching Twitter for " + strTwitterQueryString);
		QueryResult allTweets = lia.getTweets(strTwitterQueryString);
		System.out.println("Found total "
				+ allTweets.getTweets().toArray().length + " Tweets");
		System.out.println("Started Indexing tweets");
		// int totalIndexed = lia.indexTweets(allTweets);
		lia.indexTweets(allTweets);
		// System.out.println("Total tweets in the index: " + totalIndexed );
		lia.close();

	}

}
