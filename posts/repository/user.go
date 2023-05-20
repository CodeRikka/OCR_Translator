package repository

import (
	"sync"

	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	UserName    string `gorm:"column:name, not null"`
	PhoneNumber string `gorm:"column:phone, unique"`
	OpenID      string `gnorm:"column:openid, unique"`
	Password    string `gnorm:"column:password"`
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

func CreateUser(user *User) error {
	result := db.Create(&user)
	err := result.Error
	return err
}
