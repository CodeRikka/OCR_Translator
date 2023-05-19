package main

import (
	"os"

	"github.com/CodeRikka/OCR_Translator/posts/handler"
	"github.com/CodeRikka/OCR_Translator/posts/repository"
	"github.com/gin-gonic/gin"
)

func main() {
	if err := Init(); err != nil {
		os.Exit(-1)
	}
	router := gin.Default()
	router.POST("/uploadimage", func(c *gin.Context) {
		handler.Uploadimage(c)
	})
	err := router.Run(":15565")
	if err != nil {
		return
	}
}
func Init() error {
	if err := repository.Init(); err != nil {
		return err
	}
	return nil
}
