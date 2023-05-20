package main

import (
	"fmt"
	"main/handler"
	"main/repository"
	"net/http"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var db *gorm.DB

func setupRouter() *gin.Engine {
	router := gin.Default()
	router.POST("/uploadimage", func(c *gin.Context) {
		handler.Uploadimage(c)
	})
	router.POST("/user/register", func(c *gin.Context) {
		registerUser(c)
	})
	router.POST("/user/login", func(c *gin.Context) {
		loginUser(c)
	})
	return router
}

func registerUser(c *gin.Context) {
	var user repository.User
	err := c.BindJSON(&user)
	if err != nil || user.PhoneNumber == "" && user.OpenID == "" {
		fmt.Println("传入数据格式错误")
		fmt.Println(user)
		c.JSON(200, gin.H{
			"error": "传入数据格式错误",
		})
		return
	}
	if user.PhoneNumber != "" {
		cnt := db.Where("phone = ?", user.PhoneNumber).First(&repository.User{}).RowsAffected
		println("查询个数", cnt)
		if cnt != 0 {
			c.JSON(http.StatusOK, gin.H{
				"error": "该电话已被注册！",
			})
			return
		}
	}
	result := db.Create(&user)
	_ = result.Error
	c.JSON(http.StatusOK, gin.H{
		"ID":       user.ID,
		"UserName": user.UserName,
	})
}

func loginUser(c *gin.Context) {
	// TODO: Add implementation for user login

}

func main() {
	dsn := "root:root@tcp(127.0.0.1:3306)/gorm_class?charset=utf8mb4&parseTime=True&loc=Local"
	var err error
	db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	db.AutoMigrate(&repository.User{})
	router := setupRouter()
	err = router.Run(":15565")
	if err != nil {
		panic(err)
	}
}

// package main

// import (
// 	"main/handler"
// 	"main/repository"
// 	"net/http"

// 	"github.com/gin-gonic/gin"
// 	"gorm.io/driver/mysql"
// 	"gorm.io/gorm"
// )

// var db *gorm.DB

// func main() {
// 	dsn := "root:root@tcp(127.0.0.1:3306)/gorm_class?charset=utf8mb4&parseTime=True&loc=Local"
// 	db, _ := gorm.Open(mysql.Open(dsn), &gorm.Config{})
// 	// if err != nil {
// 	// 	os.Exit(-1)
// 	// }
// 	// if !db.Migrator().HasTable(&repository.User{}) {
// 	// }
// 	db.AutoMigrate(&repository.User{})
// 	router := gin.Default()
// 	router.POST("/uploadimage", func(c *gin.Context) {
// 		handler.Uploadimage(c)
// 	})
// 	router.POST("/user/register", func(c *gin.Context) {
// 		var user repository.User
// 		err := c.BindJSON(&user)
// 		if err != nil || user.PhoneNumber == "" && user.OpenID == "" {
// 			c.JSON(200, gin.H{
// 				"error": "传入数据格式错误",
// 			})
// 			return
// 		}
// 		if user.PhoneNumber != "" {
// 			cnt := db.Where("phone = ?", user.PhoneNumber).First(&repository.User{}).RowsAffected
// 			println("查询个数", cnt)
// 			if cnt != 0 {
// 				c.JSON(http.StatusOK, gin.H{
// 					"error": "该电话已被注册！",
// 				})
// 				return
// 			}
// 		}
// 		result := db.Create(&user)
// 		_ = result.Error
// 		c.JSON(http.StatusOK, gin.H{
// 			"ID":       user.ID,
// 			"UserName": user.UserName,
// 		})
// 	})
// 	router.POST("/user/login", func(c *gin.Context) {

// 	})
// 	err := router.Run(":15565")
// 	if err != nil {
// 		return
// 	}
// }
