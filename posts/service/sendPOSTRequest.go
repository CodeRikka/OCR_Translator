package service

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"time"
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
