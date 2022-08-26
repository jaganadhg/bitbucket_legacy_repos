import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Mapper;


public class IndexMapper<K,V,L,M> extends Mapper<K,V,L,M> {

	public static final String HDFS_STOPWORD_LIST = "/data/stop_words.txt";
	private HashSet<String> stopWords;
	@Override
	protected void setup(Context context)
			throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		try {
			String stopwordCacheName = new Path(HDFS_STOPWORD_LIST).getName();
			Path [] cacheFiles = context.getLocalCacheFiles();
			if (null != cacheFiles && cacheFiles.length > 0) {
				for (Path cachePath : cacheFiles) {
					if (cachePath.getName().equals(stopwordCacheName)) {
						loadStopWords(cachePath);
						break;
					}
				}
			}
		} catch (IOException ioe) {
			System.err.println("IOException reading from distributed cache");
			System.err.println(ioe.toString());
		}

	}
	void loadStopWords(Path cachePath) throws IOException {
		// note use of regular java.io methods here - this is a local file now
		BufferedReader wordReader = new BufferedReader(
				new FileReader(cachePath.toString()));
		try {
			String line;
			this.stopWords = new HashSet<String>();
			while ((line = wordReader.readLine()) != null) {
				this.stopWords.add(line);
			}
		} finally {
			wordReader.close();
		}
	}

	/* actual map() method, etc go here */

}
