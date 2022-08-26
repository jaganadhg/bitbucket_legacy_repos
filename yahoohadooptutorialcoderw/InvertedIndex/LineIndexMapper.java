import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;


public class LineIndexMapper extends Mapper<LongWritable, Text, Text, Text> {

	private final static Text word = new Text();
	private final static Text location = new Text();
	@Override
	protected void map(LongWritable key, Text value,
			Context context)
					throws IOException, InterruptedException {
		FileSplit fileSplit = (FileSplit)context.getInputSplit();
		String fileName = fileSplit.getPath().getName();
		location.set(fileName);

		String line = value.toString();
		StringTokenizer itr = new StringTokenizer(line.toLowerCase());
		while (itr.hasMoreTokens()) {
			word.set(itr.nextToken());
			context.write(word, location);
		}

	}


}
