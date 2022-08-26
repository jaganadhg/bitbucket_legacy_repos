import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;


public class LineIndexReducer extends Reducer<Text, Text, Text, Text> {

	@Override
	protected void reduce(Text key, Iterable<Text> values,
			Context context)
					throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		boolean first = true;
        Iterator<Text> valueIterator = values.iterator();
		StringBuilder toReturn = new StringBuilder();
		while (valueIterator.hasNext()){
			if (!first)
				toReturn.append(", ");
			first=false;
			toReturn.append(valueIterator.next().toString());
		}

		context.write(key, new Text(toReturn.toString()));
	}
}


