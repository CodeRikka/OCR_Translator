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
	err = service.SolvePOST("http://cn-yw-plc-2.openfrp.top:25000/export", filePath, filePath, "10", "160", outputPath)
	if err != nil {
		c.String(http.StatusInternalServerError, fmt.Sprintf("发送POST请求失败：%s", err.Error()))
	}
	c.File(outputPath)
	c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
}
