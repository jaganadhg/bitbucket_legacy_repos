import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.io.WritableUtils;

public class Point3D implements WritableComparable<Point3D> {
	public float x;
	public float y;
	public float z;

	public Point3D(float x, float y, float z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}

	public Point3D() {
		this(0.0f, 0.0f, 0.0f);
	}

	@Override
	public void write(DataOutput out) throws IOException{
		out.writeFloat(x);
		out.writeFloat(y);
		out.writeFloat(z);
	}

	@Override
	public void readFields(DataInput in) throws IOException {
		x = in.readFloat();
		y = in.readFloat();
		z = in.readFloat();
	}

	public String toString() {
		return Float.toString(x) + ", "
				+ Float.toString(y) + ", "
				+ Float.toString(z);
	}

	/** return the Euclidean distance from (0, 0, 0) */
	public float distanceFromOrigin() {
		return (float)Math.sqrt(x*x + y*y + z*z);
	}

	@Override
	public int compareTo(Point3D other) {
		float myDistance = distanceFromOrigin();
		float otherDistance = other.distanceFromOrigin();

		return Float.compare(myDistance, otherDistance);
	}

	public boolean equals(Object o) {
		if (!(o instanceof Point3D)) {
			return false;
		}

		Point3D other = (Point3D)o;
		return this.x == other.x && this.y == other.y
				&& this.z == other.z;
	}

	public int hashCode() {
		return Float.floatToIntBits(x)
				^ Float.floatToIntBits(y)
				^ Float.floatToIntBits(z);
	}
	public static class Comparator extends WritableComparator {
		public Comparator() {
			super(Text.class);
		}

		public int compare(byte[] b1, int s1, int l1,
				byte[] b2, int s2, int l2) {
			int n1 = WritableUtils.decodeVIntSize(b1[s1]);
			int n2 = WritableUtils.decodeVIntSize(b2[s2]);
			return compareBytes(b1, s1+n1, l1-n1, b2, s2+n2, l2-n2);
		}
		static {
			// register this comparator
			WritableComparator.define(Text.class, new Comparator());
		}
	}

}