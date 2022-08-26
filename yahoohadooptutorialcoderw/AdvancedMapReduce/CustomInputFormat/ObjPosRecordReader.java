import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.input.LineRecordReader;


class ObjPosRecordReader extends RecordReader<Text, Point3D> {

	private LineRecordReader lineReader;
	private Text lineValue;
	private Text key;
	private Point3D value;
	

	

	private boolean next() throws IOException {
		// get the next line

		
		if (!lineReader.nextKeyValue()) {
			return false;
		}

		key = new Text();
		value = new Point3D();
		lineValue=lineReader.getCurrentValue();

		// parse the lineValue which is in the format:
		// objName, x, y, z
		String [] pieces = lineValue.toString().split(",");
		if (pieces.length != 4) {
			throw new IOException("Invalid record received");
		}

		// try to parse floating point components of value
		float fx, fy, fz;
		try {
			fx = Float.parseFloat(pieces[1].trim());
			fy = Float.parseFloat(pieces[2].trim());
			fz = Float.parseFloat(pieces[3].trim());
		} catch (NumberFormatException nfe) {
			throw new IOException("Error parsing floating point value in record");
		}

		// now that we know we'll succeed, overwrite the output objects

		key.set(pieces[0].trim()); // objName is the output key.

		value.x = fx;
		value.y = fy;
		value.z = fz;

		return true;
	}

	
	@Override
	public Text getCurrentKey() throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		return key;
	}

	@Override
	public Point3D getCurrentValue() throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		return value;
	}

	@Override
	public void initialize(InputSplit inputSplit, TaskAttemptContext context)
			throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		lineReader = new LineRecordReader();
		lineReader.initialize(inputSplit, context);
		
	}

	@Override
	public boolean nextKeyValue() throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		return next();
	}

	@Override
	public void close() throws IOException {
		// TODO Auto-generated method stub
		lineReader.close();
		
	}

	@Override
	public float getProgress() throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		return lineReader.getProgress();
	}
}