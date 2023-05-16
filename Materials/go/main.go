package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v8"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
)

func getPgConnection() *sql.DB {
	var host = "127.0.0.1"

	envHost := os.Getenv("POSTGRES_HOST")

	if envHost != "" {
		host = envHost
	}

	var connectionStr = fmt.Sprintf("dbname=%s user=%s password=%s host=%s port=%s sslmode=disable",
		os.Getenv("POSTGRES_DB"), os.Getenv("POSTGRES_USER"), os.Getenv("POSTGRES_PASSWORD"),
		host, os.Getenv("POSTGRES_PORT"))

	var db, err = sql.Open("postgres", connectionStr)
	if err != nil {
		fmt.Println(err)
	}

	return db
}

var redisCtx = context.Background()

func getRedisConnection() *redis.Client {
	var host = "127.0.0.1"

	envHost := os.Getenv("REDIS_HOST")

	if envHost != "" {
		host = envHost
	}

	var rdb = redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", host, os.Getenv("REDIS_PORT")),
		Password: os.Getenv("REDIS_PASSWORD"),
	})

	return rdb
}

type DbHolder struct {
	Id    string
	Phone string
	Name  string
}

func main() {
	if err := godotenv.Load(); err != nil && !os.IsNotExist(err) {
		log.Fatal(err)
	}

	router := gin.Default()
	router.GET("/holders", getHolders)
	router.POST("/holders/create", createHolder)

	router.Run(fmt.Sprintf(":%s", os.Getenv("APP_PORT")))
}

func getHolders(c *gin.Context) {
	var limit = c.Query("limit")
	var offset = c.Query("offset")
	var redisKey = fmt.Sprintf("holders:offset=%s,limit=%s", limit, offset)

	rdb := getRedisConnection()
	defer rdb.Close()
	redisHolders, _ := rdb.Get(redisCtx, redisKey).Result()

	if redisHolders == "" {
		pg := getPgConnection()
		defer pg.Close()

		rows, err := pg.Query("select id, name, phone from holder limit $1 offset $2", limit, offset)
		if err != nil {
			fmt.Println(err)
			c.Status(http.StatusBadRequest)
			return
		}
		defer rows.Close()

		var holders []DbHolder
		for rows.Next() {
			var holder DbHolder
			if err := rows.Scan(&holder.Id, &holder.Name, &holder.Phone); err != nil {
				fmt.Println(err)
				c.Status(http.StatusBadRequest)
				return
			}
			holders = append(holders, holder)
		}

		res, err := json.Marshal(holders)
		if err != nil {
			fmt.Println(err)
			c.Status(http.StatusBadRequest)
			return
		}

		rdb.Set(redisCtx, redisKey, string(res), 30*time.Second)

		c.Data(http.StatusOK, "application/json", res)
	} else {
		c.Data(http.StatusOK, "application/json", []byte(redisHolders))
	}
}

func createHolder(c *gin.Context) {
	var newHolder DbHolder
	if err := c.BindJSON(&newHolder); err != nil {
		fmt.Println(err)
		c.Status(http.StatusBadRequest)
		return
	}

	pg := getPgConnection()
	defer pg.Close()

	queryResponse := pg.QueryRow("insert into holder (phone, name) values ($1, $2) returning id", newHolder.Phone, newHolder.Name)
	if err := queryResponse.Scan(&newHolder.Id); err != nil {
		fmt.Println(err)
		c.Status(http.StatusBadRequest)
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "holder created", "data": newHolder})
}
