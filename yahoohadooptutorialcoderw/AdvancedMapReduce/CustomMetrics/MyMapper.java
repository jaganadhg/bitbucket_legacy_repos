import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class MyMapper extends Mapper<Text,Text,Text,Text>{

	static enum RecordCounters { TYPE_A, TYPE_B, TYPE_UNKNOWN };

	// actual definitions elided
	public boolean isTypeARecord(Text input) { /** Write code for checking for record type A */ return false;  }
	public boolean isTypeBRecord(Text input) { /** Write code for checking for record type B */ return false; }
	@Override
	protected void map(Text key, Text value,
			Context context)
					throws IOException, InterruptedException {
		if (isTypeARecord(key)) {
			context.getCounter(RecordCounters.TYPE_A).increment(1);
		} else if (isTypeBRecord(key)) {
			context.getCounter(RecordCounters.TYPE_B).increment(1);
		} else {
			context.getCounter(RecordCounters.TYPE_UNKNOWN).increment(1);
		}

		// actually process the record here, call
		// output.collect( .. ), etc.
	}

}
