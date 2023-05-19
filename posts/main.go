package main

import (
	"github.com/CodeRikka/OCR_Translator/posts/handler"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.POST("/uploadimage", func(c *gin.Context) {
		handler.Uploadimage(c)
	})
	router.Run(":15565")
}
