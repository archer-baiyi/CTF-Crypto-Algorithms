import java.util.Random;

public class Example {
    public static void main(String[] args) {
        Random random = new Random();

        for (int i = 0; i < 5; i++) {
            System.out.println(random.nextInt());
        }
    }

//    -1631771576
//    595259081
//    1877836896
//    -926975024
//    -234258569
}