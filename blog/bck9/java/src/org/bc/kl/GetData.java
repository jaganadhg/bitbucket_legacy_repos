package org.bc.kl;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

import com.sun.org.apache.xalan.internal.xsltc.runtime.Hashtable;

public class GetData {
	public static Hashtable getUserData() throws Exception{
		//Map<Integer,String> mp=new HashMap<Integer, String>();
		Hashtable userData = new Hashtable();

		FileInputStream fstream = new FileInputStream("/home/jaganadhg/Desktop/bck9/users.txt");
		DataInputStream in = new DataInputStream(fstream);
        BufferedReader br = new BufferedReader(new InputStreamReader(in));
        String strLine;
        while ((strLine = br.readLine()) != null)   {
            // Print the content on the console
            //System.out.println (strLine);
           String[] vals ;
           vals = strLine.split(",");
           //System.out.println(vals[0] + " " + vals[1]);
           //mp.put(Integer.parseInt(vals[0]), vals[1]);
           userData.put(vals[0], vals[1]);
          }
        //System.out.println(mp);
		return userData;
		
	}
	
	public static Hashtable getMovieData() throws Exception{
		//Map<Integer,String> mps=new HashMap<Integer, String>();
		Hashtable movieData = new Hashtable();
		FileInputStream fstream = new FileInputStream("/home/jaganadhg/Desktop/bck9/movie.txt");
		DataInputStream in = new DataInputStream(fstream);
        BufferedReader br = new BufferedReader(new InputStreamReader(in));
        String strLine;
        while ((strLine = br.readLine()) != null)   {
            // Print the content on the console
            //System.out.println (strLine);
           String[] vals ;
           vals = strLine.split(",");
           //System.out.println(vals[0] + " " + vals[1]);
           //mps.put(Integer.parseInt(vals[0]) , vals[1]);
           movieData.put(vals[0], vals[1]);
          }
	
		return movieData;
	
	}

}
