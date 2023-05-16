package redis_samples_group;

import org.apache.catalina.Context;
import org.apache.catalina.WebResourceRoot;
import org.apache.catalina.startup.ContextConfig;
import org.apache.catalina.startup.Tomcat;
import org.apache.catalina.webresources.StandardRoot;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) throws Exception {
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(8080);
        Context ctx = tomcat.addContext("", Paths.get(".").toAbsolutePath().toString());
        ctx.addLifecycleListener(new ContextConfig());
        WebResourceRoot root = new StandardRoot(ctx);
        root.createWebResourceSet(WebResourceRoot.ResourceSetType.PRE,
                "/WEB-INF/classes",
                Main.class.getProtectionDomain().getCodeSource().getLocation(),
                "/");
        ctx.setResources(root);
        tomcat.start();
        tomcat.getServer().await();
    }
}
