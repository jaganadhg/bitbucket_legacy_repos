package org.jaggu.bd.mahout;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.Charset;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.SequenceFile;
import org.apache.hadoop.io.SequenceFile.Writer;
import org.apache.hadoop.io.Text;

public class PrepareDocs {

	public static String readFile(File path) throws IOException {
		FileInputStream stream = new FileInputStream(path);
		try {
			FileChannel fc = stream.getChannel();
			MappedByteBuffer bb = fc.map(FileChannel.MapMode.READ_ONLY, 0,
					fc.size());
			return Charset.defaultCharset().decode(bb).toString();
		} finally {
			stream.close();
		}
	}

	public static void main(String args[]) throws IOException {
		Configuration conf = new Configuration();
		FileSystem fs = FileSystem.get(conf);
		Path path = new Path(args[1]);
		Writer writer = new SequenceFile.Writer(fs, conf, path, Text.class,
				Text.class);

		File[] dirs = new File(args[0]).listFiles();

		for (File dir : dirs) {
			String label = dir.getName();

			for (File file : dir.listFiles()) {
				String text = readFile(file);
				System.out.println(text);
				writer.append(new Text("/" + label), new Text(text));
			}
		}
		writer.close();

	}

}
