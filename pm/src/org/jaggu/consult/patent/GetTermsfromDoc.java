package org.jaggu.consult.patent;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Map;

import com.sree.textbytes.jtopia.TermDocument;
import com.sree.textbytes.jtopia.TermsExtractor;

public class GetTermsfromDoc {

	public static void getEntity(String filename) throws FileNotFoundException {

		FileInputStream fis = new FileInputStream(filename);
		// InputStreamReader is = new InputStreamReader(fis);

		DataInputStream dis = new DataInputStream(fis);
		BufferedReader br = new BufferedReader(new InputStreamReader(dis));

		StringBuffer sb = new StringBuffer();
		String line = "";
		try {
			while ((line = br.readLine()) != null) {
				if (!line.toString().startsWith("TABLE")
						|| !line.toString().startsWith("-----")
						||!line.toString().startsWith("[[") ||
						!line.toString().startsWith("______")) {
					sb.append(line);

				} else {
					
				}

			}
		} catch (Exception e) {
			e.printStackTrace();
		}

		TermsExtractor te = new TermsExtractor();
		TermDocument td = new TermDocument();

		// td = te.extractTerms(doc,
		// "/home/u179995/Public/jtopia/model/english-lexicon.txt");
		td = te.extractTerms(sb.toString(),
				"/home/u179995/Public/jtopia/model/english-lexicon.txt");
		//for (t: td.getTerms()){}
		//System.out.println(td.getFinalFilteredTerms());
		//System.out.println(td.getTerms());
		Map<String, ArrayList<Integer>> s = td.getFinalFilteredTerms();
		for(int i = 0; i < td.getFinalFilteredTerms().size(); i++){
			System.out.println(td.getFinalFilteredTerms().get(i) + "    AAAAAAA");
		}
	}

	/**
	 * @param args
	 * @throws FileNotFoundException
	 */
	public static void main(String[] args) throws FileNotFoundException {
		String fn = "/home/u179995/Desktop/patents/PT_5866601.txt";
		getEntity(fn);

	}

}
