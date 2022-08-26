package org.jaggu.tm.pig;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.pig.EvalFunc;
import org.apache.pig.data.BagFactory;
import org.apache.pig.data.DataBag;
import org.apache.pig.data.DataType;
import org.apache.pig.data.Tuple;
import org.apache.pig.data.TupleFactory;
import org.apache.pig.impl.logicalLayer.schema.Schema;

public class PigTokenizer extends EvalFunc<DataBag> {

	private TupleFactory tfTokTf = TupleFactory.getInstance();
	private BagFactory bfTokTF = BagFactory.getInstance();

	public DataBag exec(Tuple strInput) throws IOException {
		if (strInput == null || strInput.size() < 1 || strInput.isNull(0))
			return null;

		DataBag tokenBag = bfTokTF.newDefaultBag();
		// StringReader strInputString = new StringReader((String)
		// strInput.get(1)
		// .toString());

		Object sometext = strInput.get(0);

		String strCleanedText = sometext.toString().replaceAll("\\p{Punct}+",
				"");

		// String strCleanedText = strInputString.toString().replaceAll(
		// "\\p{Punct}+", "");

		StringTokenizer tokenizer = new StringTokenizer(strCleanedText);

		while (tokenizer.hasMoreTokens()) {
			String currentToken = tokenizer.nextToken().toLowerCase()
					.replaceAll("\\p{Punct}+", "");
			if (currentToken.length() > 1) {
				Tuple strFinalWords = tfTokTf.newTuple(currentToken.toString());
				tokenBag.add(strFinalWords);
			}
		}
		return tokenBag;

	}

	public Schema outputSchema(Schema input) {
		try {
			Schema bagSchema = new Schema();
			bagSchema.add(new Schema.FieldSchema("token", DataType.CHARARRAY));

			return new Schema(new Schema.FieldSchema(getSchemaName(this
					.getClass().getName().toLowerCase(), input), bagSchema,
					DataType.BAG));
		} catch (Exception e) {
			return null;
		}
	}

}
