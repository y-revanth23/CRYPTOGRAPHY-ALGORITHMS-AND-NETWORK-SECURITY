import java.io.*;
import java.util.*;

public class Primitive {

    static long power(long a, long b, int mod) {
        long result = 1;
        a = a % mod;
        while (b > 0) {
            if (b % 2 == 1)
                result = (result * a) % mod;
            a = (a * a) % mod;
            b /= 2;
        }
        return result;
    }

    static Set<Integer> getPrimeFactors(int n) {
        Set<Integer> factors = new HashSet<>();
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                factors.add(i);
                while (n % i == 0)
                    n /= i;
            }
        }
        if (n > 1)
            factors.add(n);
        return factors;
    }

    static int phi(int n) {
        int result = n;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                while (n % i == 0)
                    n /= i;
                result -= result / i;
            }
        }
        if (n > 1)
            result -= result / n;
        return result;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int p = Integer.parseInt(br.readLine().trim());

        int phiValue = p - 1;
        Set<Integer> factors = getPrimeFactors(phiValue);

        int smallestRoot = -1;

        for (int g = 2; g < p; g++) {
            boolean isPrimitive = true;

            for (int q : factors) {
                if (power(g, phiValue / q, p) == 1) {
                    isPrimitive = false;
                    break;
                }
            }

            if (isPrimitive) {
                smallestRoot = g;
                break;
            }
        }

        int totalRoots = phi(phiValue);

        System.out.println(smallestRoot + " " + totalRoots);
    }
}