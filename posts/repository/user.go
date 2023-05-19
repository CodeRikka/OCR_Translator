package repository

import (
	"sync"
	"time"

	"gorm.io/gorm"
)

type User struct {
	Id         int64     `gorm:"column:id"`
	Name       string    `gorm:"column:name"`
	CreateTime time.Time `gorm:"column:create_time"`
	ModifyTime time.Time `gorm:"column:modify_time"`
}

func (User) TableName() string {
	return "users"
}

type UserDao struct {
}

var userDao *UserDao
var userOnce sync.Once

func NewUserDaoInstance() *UserDao {
	userOnce.Do(
		func() {
			userDao = &UserDao{}
		})
	return userDao
}

func (*UserDao) QueryUserById(id int64) (*User, error) {
	var user User
	err := db.Where("id = ?", id).Find(&user).Error
	if err == gorm.ErrRecordNotFound {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &user, nil
}
