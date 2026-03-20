import java.io.*;

public class Poweroflargenumber {

    static final int MOD = 1000000007;

    // fast exponentiation
    static long power(long a, long b) {
        long result = 1;
        a = a % MOD;

        while (b > 0) {
            if (b % 2 == 1)
                result = (result * a) % MOD;

            a = (a * a) % MOD;
            b /= 2;
        }
        return result;
    }

    // convert string to mod value
    static long stringMod(String s, int mod) {
        long result = 0;
        for (int i = 0; i < s.length(); i++) {
            result = (result * 10 + (s.charAt(i) - '0')) % mod;
        }
        return result;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int t = Integer.parseInt(br.readLine());

        while (t-- > 0) {
            String[] input = br.readLine().split(" ");
            String a = input[0];
            String b = input[1];

            long base = stringMod(a, MOD);
            long exponent = stringMod(b, MOD - 1);

            System.out.println(power(base, exponent));
        }
    }
}