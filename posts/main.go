package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

// 根据图片格式获得保存后的文件名
func Rename(filename string) (string, error) {
	year, month, day := time.Now().Date()
	h, m, s := time.Now().UTC().Clock()
	println(h, m, s)
	rename := fmt.Sprintf("%d%d%d_%d%d%d", year, month, day, h, m, s)

	if strings.HasSuffix(filename, ".png") {
		return rename + ".png", nil
	}
	if strings.HasSuffix(filename, ".jpg") {
		return rename + ".jpg", nil
	}
	return "格式错误", nil
}
func SendPostRequest(urlStr string, postData map[string]string) ([]byte, error) {
	// 构造POST请求参数
	formData := bytes.NewBufferString("")
	for key, value := range postData {
		formData.WriteString(fmt.Sprintf("%s=%s&", key, value))
	}
	formDataString := formData.String()

	// 创建HTTP请求
	req, err := http.NewRequest("POST", urlStr, bytes.NewBufferString(formDataString))
	if err != nil {
		return nil, err
	}

	// 设置请求头
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	// 发送HTTP请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// 读取响应数据
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return body, nil
}
func SolvePOST(urlStr string, root0 string, root1 string, tl string, tb string, output string) error {
	// 构造POST请求参数
	postData := map[string]string{
		"root0":  root0,
		"root1":  root1,
		"tl":     tl,
		"tb":     tb,
		"output": output,
	}
	// 发送HTTP POST请求
	response, err := SendPostRequest(urlStr, postData)
	if err != nil {
		return err
	}
	fmt.Println(string(response))
	return nil
}
func main() {
	router := gin.Default()
	// 为 multipart forms 设置较低的内存限制 (默认是 32 MiB)
	// router.MaxMultipartMemory = 8 << 20  // 8 MiB
	router.POST("/uploadimage", func(c *gin.Context) {
		// 单文件
		file, _ := c.FormFile("file")
		log.Println("文件名为" + file.Filename)

		filename, _ := Rename(file.Filename)
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
		err = SolvePOST("http://cn-yw-plc-2.openfrp.top:25000/export", filePath, filePath, "10", "160", outputPath)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("发送POST请求失败：%s", err.Error()))
		}
		c.File(outputPath)
		c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
	})
	router.Run(":15565")
}
