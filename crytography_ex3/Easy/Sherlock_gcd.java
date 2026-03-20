import java.io.*;

public class Sherlock_gcd {

    static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int t = Integer.parseInt(br.readLine());

        while (t-- > 0) {
            int n = Integer.parseInt(br.readLine());
            String[] arr = br.readLine().split(" ");

            int g = 0;

            for (int i = 0; i < n; i++) {
                int num = Integer.parseInt(arr[i]);
                g = gcd(g, num);
            }

            if (g == 1)
                System.out.println("YES");
            else
                System.out.println("NO");
        }
    }
}