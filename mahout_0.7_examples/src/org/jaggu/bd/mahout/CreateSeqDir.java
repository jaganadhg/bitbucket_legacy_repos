package org.jaggu.bd.mahout;

import org.apache.hadoop.conf.Configuration;
import org.apache.mahout.driver.MahoutDriver;
import org.apache.mahout.text.SequenceFilesFromDirectory;
import org.apache.mahout.text.SequenceFilesFromDirectoryFilter;

public class CreateSeqDir {
	
	/**
	 * @param args
	 */
	
	public static void createSeqDir(String strDirPath){
	
		SequenceFilesFromDirectory sffd = new SequenceFilesFromDirectory();
		Configuration config = new Configuration();
		config.set("input", strDirPath);
		config.set("output", "FromJava");
		
		sffd.setConf(config);
		//sffd.run(0);
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
