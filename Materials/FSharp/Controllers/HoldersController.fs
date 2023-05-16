namespace FSharpApiSample.Controllers

open System
open System.Data
open System.Text.Json
open System.Threading.Tasks
open Dapper
open Microsoft.AspNetCore.Mvc
open Microsoft.Extensions.Logging
open StackExchange.Redis

[<CLIMutable>]
type Holder = {
    id: int
    name: string
    phone: string
}

type CreateHolderRequest = {
    name: string
    phone: string
}

type UpdateHolderRequest = Holder

type DeleteHolderRequest = {
    id: int
}

[<ApiController>]
[<Route("api/holders")>]
type HoldersController(logger: ILogger<HoldersController>, pgConnection: IDbConnection, redisConnection: IDatabase) =
    inherit ControllerBase()

    [<HttpGet>]
    member x.GetHolders(limit: int, offset: int) = task {
        try
            let redisKey = $"/holders?limit={limit}&offset={offset}"

            let! redisValue = redisConnection.StringGetAsync redisKey
            if redisValue.HasValue then
                let holders = redisValue.ToString() |>JsonSerializer.Deserialize<Holder[]>
                return holders |> ActionResult<seq<Holder>>
            else
                let parameters = dict [("limit", box limit); ("offset", offset)]
                let! holders =
                    pgConnection.QueryAsync<Holder>("select * from holder limit @limit offset @offset", parameters)

                do! redisConnection
                        .StringSetAsync(redisKey, JsonSerializer.Serialize holders, TimeSpan.FromSeconds 30) :> Task

                return holders |> ActionResult<seq<Holder>>
        with
        | err ->
            logger.LogError("GetHolders: {err}", err)
            return x.BadRequest() |> ActionResult<seq<Holder>>
    }

    [<HttpPost("create")>]
    member x.CreateHolder([<FromBody>] body: CreateHolderRequest) = task {
        try
            let parameters = dict [("phone", box body.phone); ("name", body.name)]
            let query = """
insert into holder (phone, name)
values (@phone, @name)
returning id, phone, name
"""
            let! result = pgConnection.QueryAsync<Holder>(query, parameters)

            return Seq.head result |> ActionResult<Holder>
        with
        | err ->
            logger.LogError("CreateHolder: {err}", err)
            return x.BadRequest() |> ActionResult<Holder>
    }

    [<HttpPost("update")>]
    member x.UpdateHolder([<FromBody>] body: UpdateHolderRequest) = task {
        try
            let parameters = dict [("id", box body.id); ("phone", body.phone); ("name", body.name)]
            let query = """
update holder
set name = @name, phone = @phone
where id = @id
returning id, name, phone
"""
            let! result = pgConnection.QueryAsync<Holder>(query, parameters)

            return Seq.head result |> ActionResult<Holder>
        with
        | err ->
            logger.LogError("UpdateHolder: {err}", err)
            return x.BadRequest() |> ActionResult<Holder>
    }

    [<HttpDelete("delete")>]
    member x.DeleteHolder([<FromBody>] body: DeleteHolderRequest) = task {
        try
            let parameters = dict [("id", box body.id)]
            let query = """
delete from holder
where id = @id
returning id, name, phone
"""
            let! result = pgConnection.QueryAsync<Holder>(query, parameters)

            return Seq.head result |> ActionResult<Holder>
        with
        | err ->
            logger.LogError("DeleteHolder: {err}", err)
            return x.BadRequest() |> ActionResult<Holder>
    }
