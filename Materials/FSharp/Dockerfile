FROM mcr.microsoft.com/dotnet/sdk:6.0.402 AS build_api
WORKDIR /src_api
COPY FSharpApi.fsproj .
COPY appsettings.json .
COPY Program.fs .
COPY Controllers/ ./Controllers/
RUN dotnet build "FSharpApi.fsproj" -c Release -o /fs_api/build
RUN dotnet publish "FSharpApi.fsproj" -c Release -o /fs_api/publish

FROM mcr.microsoft.com/dotnet/aspnet:6.0.10
WORKDIR /fs_api
COPY --from=build_api /fs_api/publish .
ENTRYPOINT ["dotnet", "FSharpApi.dll"]
