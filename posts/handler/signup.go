package handler

import (
	"github.com/CodeRikka/OCR_Translator/posts/repository"
	"github.com/CodeRikka/OCR_Translator/posts/service"
	"github.com/gin-gonic/gin"
)

func Signup(c *gin.Context) {
	var user repository.User
	var errstr string
	err := c.BindJSON(&user)
	if err != nil {
		// fmt.Println("绑定出错")
		errstr = "绑定出错"
	}
	_ = service.SignupUser(&user)
	c.JSON(200, gin.H{
		"err": errstr,
	})
}
