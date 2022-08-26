import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class LineIndexDriver {
	public static void main(String[] args) throws IOException, InterruptedException, ClassNotFoundException {
		
		Configuration configuration = new Configuration();
        Job job = new Job(configuration);
		
	    job.setJobName("LineIndexer");

	    job.setOutputKeyClass(Text.class);
	    job.setOutputValueClass(Text.class);

	    FileInputFormat.addInputPath(job, new Path("input"));
	    FileOutputFormat.setOutputPath(job, new Path("output"));

	    job.setMapperClass(LineIndexMapper.class);
	    job.setReducerClass(LineIndexReducer.class);
	    
        job.waitForCompletion(true);
	    
	}

}
