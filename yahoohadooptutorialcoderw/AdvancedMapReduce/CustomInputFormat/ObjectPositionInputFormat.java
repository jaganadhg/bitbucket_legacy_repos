import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;

public class ObjectPositionInputFormat extends
    FileInputFormat<Text, Point3D> {

@Override
public RecordReader<Text, Point3D> createRecordReader(InputSplit inputSplit,
		TaskAttemptContext taskAttemptContext) throws IOException, InterruptedException {
	// TODO Auto-generated method stub
	taskAttemptContext.setStatus(inputSplit.toString());
	return new ObjPosRecordReader();
}
}