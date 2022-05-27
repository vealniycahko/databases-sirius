package redis_samples_group;

import com.google.gson.Gson;
import io.lettuce.core.RedisClient;

import javax.servlet.http.*;
import javax.servlet.annotation.WebServlet;
import java.util.List;

@WebServlet("/user_actions")
public class UserActionsServlet extends HttpServlet {
    private static final RedisClient redisClient = RedisClient.create("redis://redis@localhost:26596");

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) {
        try {
            response.setContentType("text/html; charset=UTF-8");

            var name = request.getParameter("name");

            List<String> actions;
            try (var connection = redisClient.connect()) {
                actions = connection.sync().lrange(name, 0, -1);
            }

            response.getWriter().println(new Gson().toJson(actions));
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) {
        try {
            var name = request.getParameter("name");
            var action = request.getParameter("action");

            try (var connection = redisClient.connect()) {
                connection.sync().lpush(name, action);
            }
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    @Override
    public void doDelete(HttpServletRequest request, HttpServletResponse response) {
        try {
            var name = request.getParameter("name");

            try (var connection = redisClient.connect()) {
                connection.sync().lpop(name);
            }
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }
}
