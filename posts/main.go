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
	// SolvePOST("http://cn-yw-plc-2.openfrp.top:25000/export", "E:/Code/Python/ocr/pics/example6.jpg", "E:/Code/Python/ocr/pics/example6.jpg", "10", "160", "E:/img/output_2.jpg")
	router := gin.Default()
	// 为 multipart forms 设置较低的内存限制 (默认是 32 MiB)
	// router.MaxMultipartMemory = 8 << 20  // 8 MiB
	router.POST("/uploadimage", func(c *gin.Context) {
		// 单文件
		file, _ := c.FormFile("file")
		log.Println("文件名为" + file.Filename)

		// 上传文件至指定目录
		filename, _ := Rename(file.Filename)
		filePath := "E:/Code/Go/test/img/" + filename
		fmt.Println("filePath = " + filePath)
		err := c.SaveUploadedFile(file, filePath)
		if err != nil {
			fmt.Println(err)
			c.String(http.StatusInternalServerError, "文件上传失败")
			return
		}
		err = SolvePOST("http://cn-yw-plc-2.openfrp.top:25000/export", filePath, filePath, "10", "160", "E:/img/output_"+filename)
		if err != nil {
			c.String(http.StatusInternalServerError, fmt.Sprintf("发送POST请求失败：%s", err.Error()))
		}
		c.File("E:/img/output_" + filename)
		c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
	})
	router.Run(":15565")
}

//curl -X POST http://cn-yw-plc-2.openfrp.top:15565/uploadimage -F "file=@E:/Wallpaper/6b6e0f92c9bc41d5a549ac9c596872cc.jpg" -o "e:img.jpg"
// func main() {
// 	router := gin.Default()
// 	// 为 multipart forms 设置较低的内存限制 (默认是 32 MiB)
// 	router.MaxMultipartMemory = 8 << 20 // 8 MiB
// 	router.POST("/uploadimage", func(c *gin.Context) {
// 		// Multipart form
// 		form, _ := c.MultipartForm()
// 		files := form.File["upload[]"]

//			for _, file := range files {
//				log.Println(file.Filename)
//				filename, _ := Rename(file.Filename)
//				print(filename)
//				//上传文件至指定目录
//				err := c.SaveUploadedFile(file, "./test/img/"+filename)
//				if err != nil {
//					fmt.Println(err)
//				}
//			}
//			c.String(http.StatusOK, fmt.Sprintf("%d files uploaded!", len(files)))
//		})
//		router.Run(":15565")
//	}

// func SendPostRequest(urlStr string, postData url.Values) ([]byte, error) {
// 	// 编码POST数据
// 	formData := postData.Encode()

// 	// 创建HTTP请求
// 	req, err := http.NewRequest("POST", urlStr, bytes.NewBufferString(formData))
// 	if err != nil {
// 		return nil, err
// 	}

// 	// 设置请求头
// 	// req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

// 	// 发送HTTP请求
// 	client := &http.Client{}
// 	resp, err := client.Do(req)
// 	if err != nil {
// 		return nil, err
// 	}
// 	defer resp.Body.Close()

// 	// 读取响应数据
// 	body, err := ioutil.ReadAll(resp.Body)
// 	if err != nil {
// 		return nil, err
// 	}

//		return body, nil
//	}

// func SolvePOST(urlStr string, root0 string, root1 string, tl string, tb string, output string) error {
// 	postData := url.Values{}
// 	postData.Add("root0", root0)
// 	postData.Add("root1", root1)
// 	postData.Add("tl", tl)
// 	postData.Add("tb", tb)
// 	postData.Add("output", output)
// 	fmt.Println(postData)
// 	// 发送HTTP POST请求
// 	response, err := SendPostRequest(urlStr, postData)
// 	if err != nil {
// 		panic(err)
// 	}
// 	fmt.Println(string(response))
// 	return nil
// }
