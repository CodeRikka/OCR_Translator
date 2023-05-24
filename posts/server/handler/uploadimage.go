package handler

import (
	"fmt"
	"log"
	"net/http"

	"main/service"

	"github.com/gin-gonic/gin"
)

func Uploadimage(c *gin.Context) {
	// 单文件
	file, _ := c.FormFile("file")
	log.Println("文件名为" + file.Filename)
	// 获取参数
	//FONT_SIZE THRESH_LINE THRESH_BOX DEWARP llama
	// THRESH_LINE := c.PostForm("THRESH_LINE") // 参数名为THRESH_LINE
	// THRESH_BOX := c.PostForm("THRESH_BOX")
	// FONT_SIZE := c.PostForm("FONT_SIZE")
	// DEWARP := c.PostForm("DEWARP")
	// LLAMA := c.PostForm("LLAMA")
	THRESH_LINE := "10"
	THRESH_BOX := "160"
	FONT_SIZE := "35"
	DEWARP := "False"
	LLAMA := "false"
	filename, _ := service.Rename(file.Filename)
	filePath := "E:/img/" + filename
	outputPath := "E:/img/output_" + filename
	fmt.Println("filePath = " + filePath)

	// 上传文件至指定目录
	err := c.SaveUploadedFile(file, filePath)
	if err != nil {
		fmt.Println(err)
		c.String(http.StatusInternalServerError, "文件上传失败")
		return
	}
	err = service.SolvePOST("http://127.0.0.1:25000/export", filePath, filePath, THRESH_LINE, THRESH_BOX, FONT_SIZE, DEWARP, LLAMA, outputPath)
	if err != nil {
		c.String(http.StatusInternalServerError, fmt.Sprintf("发送POST请求失败：%s", err.Error()))
		return
	}
	c.File(outputPath)
	c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
}
