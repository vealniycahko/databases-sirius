namespace FSharpApiSample

open System.Data
open Microsoft.AspNetCore.Builder
open Microsoft.Extensions.DependencyInjection
open Microsoft.Extensions.Hosting
open Npgsql
open StackExchange.Redis

module Program =
    DotNetEnv.Env.Load() |> ignore

    let private pgConnectionString = $"""
Server={DotNetEnv.Env.GetString("POSTGRES_HOST", "127.0.0.1")};
Port={DotNetEnv.Env.GetString "POSTGRES_PORT"};
Database={DotNetEnv.Env.GetString "POSTGRES_DB"};
User Id={DotNetEnv.Env.GetString "POSTGRES_USER"};
Password={DotNetEnv.Env.GetString "POSTGRES_PASSWORD"};
"""

    let private redisConnectionString = $"""
{DotNetEnv.Env.GetString("REDIS_HOST", "127.0.0.1")}:{DotNetEnv.Env.GetString "REDIS_PORT"},
password={DotNetEnv.Env.GetString "REDIS_PASSWORD"}
"""

    [<EntryPoint>]
    let main args =
        let builder = WebApplication.CreateBuilder args

        builder.Services.AddControllers() |> ignore

        builder.Services.AddEndpointsApiExplorer() |> ignore
        builder.Services.AddSwaggerGen() |> ignore

        builder.Services.AddScoped<IDbConnection>(fun _ -> new NpgsqlConnection(pgConnectionString)) |>ignore
        builder.Services.AddSingleton(ConnectionMultiplexer.Connect(redisConnectionString).GetDatabase()) |> ignore

        let app = builder.Build()

        app.UseRouting() |> ignore
        app.UseEndpoints(fun builder -> builder.MapControllers() |> ignore) |> ignore

        app.UseSwagger() |> ignore
        app.UseSwaggerUI() |> ignore

        app.Run()

        0
