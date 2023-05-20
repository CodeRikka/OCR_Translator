package main

import (
	"os"

	"github.com/CodeRikka/OCR_Translator/posts/handler"
	"github.com/CodeRikka/OCR_Translator/posts/repository"
	"github.com/gin-gonic/gin"
)

func Init() error {
	if err := repository.Init(); err != nil {
		return err
	}
	return nil
}

func main() {
	if err := Init(); err != nil {
		os.Exit(-1)
	}
	router := gin.Default()
	router.POST("/uploadimage", func(c *gin.Context) {
		handler.Uploadimage(c)
	})
	router.POST("/signup", func(c *gin.Context) {

		handler.Signup(c)

	})
	router.POST("/login", func(c *gin.Context) {

	})
	err := router.Run(":15565")
	if err != nil {
		return
	}
}
