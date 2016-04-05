import org.junit.runner.JUnitCore;
import org.junit.runner.Request;
import org.junit.runner.Result;

public class SingleJUnitTestRunner {
    public static void main(String... args) throws ClassNotFoundException {
        String[] classAndMethod = args[0].split("#");
        Request request = Request.method(Class.forName(classAndMethod[0]),
                classAndMethod[1]);

        Result result = new JUnitCore().run(request);
	System.out.println(result.wasSuccessful());
	System.out.println("runcount="+result.getRunCount());
	System.out.println("getFailureCount="+result.getFailureCount());
        System.exit(result.wasSuccessful() ? 0 : 1);
    }
}
