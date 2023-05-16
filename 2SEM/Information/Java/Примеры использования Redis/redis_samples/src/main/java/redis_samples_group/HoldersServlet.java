package redis_samples_group;

import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Types;
import java.util.ArrayList;
import java.util.Properties;

import com.google.gson.Gson;
import io.lettuce.core.RedisClient;

import javax.servlet.http.*;
import javax.servlet.annotation.WebServlet;

import static io.lettuce.core.SetArgs.Builder.ex;

class Holder {
    public String name;
    public String phone;

    public Holder(String name, String phone) {
        this.name = name;
        this.phone = phone;
    }
}

@WebServlet("/holders")
public class HoldersServlet extends HttpServlet {
    private static final RedisClient redisClient = RedisClient.create("redis://redis@localhost:26596");

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) {
        try {
            response.setContentType("text/html; charset=UTF-8");

            var offset = request.getParameter("offset");
            var limit = request.getParameter("limit");

            var redis_key = "holders?offset=" + offset + "&limit=" + limit;
            String result;
            try (var redisConnection = redisClient.connect()) {
                result = redisConnection.sync().get(redis_key);

                if (result == null) {
                    var connectionProps = new Properties();
                    connectionProps.put("user", "postgres");
                    connectionProps.put("password", "postgres");

                    var holders = new ArrayList<Holder>();
                    ResultSet rs;
                    try (var pgConnection = DriverManager
                            .getConnection("jdbc:postgresql://127.0.0.1:38746/postgres", connectionProps)) {
                        var query = "select * from holder offset ? limit ?";
                        var stmt = pgConnection.prepareStatement(query);

                        if (offset != null) stmt.setInt(1, Integer.parseInt(offset));
                        else stmt.setNull(1, Types.BIGINT);

                        if (limit != null) stmt.setInt(2, Integer.parseInt(limit));
                        else stmt.setNull(2, Types.BIGINT);

                        rs = stmt.executeQuery();
                    }

                    while (rs.next()) {
                        holders.add(new Holder(rs.getString("name"), rs.getString("phone")));
                    }

                    result = new Gson().toJson(holders);

                    redisConnection.sync().set(redis_key, result, ex(30));
                }
            }

            response.getWriter().println(result);
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }
}
