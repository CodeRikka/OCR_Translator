package repository

import (
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/schema"
)

var db *gorm.DB

func Init() error {
	var err error
	db, err := gorm.Open(mysql.New(mysql.Config{
		DSN:               "root:root@tcp(127.0.0.1:3306)/gnorm_class?charset=utf8mb4&parseTime=True&loc=Local",
		DefaultStringSize: 191,
	}), &gorm.Config{
		NamingStrategy: schema.NamingStrategy{
			SingularTable: false,
		},
		DisableForeignKeyConstraintWhenMigrating: true,
	})
	M := db.Migrator()
	if M.HasTable(&User{}) {
		M.CreateTable(&User{})
	}
	
	return err
}
