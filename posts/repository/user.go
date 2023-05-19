package repository

import (
	"sync"

	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Name  string `gorm:"column:name, not null, unique"`
	Email string `gorm:"column:email, not null"`
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

// func CreateUser(email string, userName string, password string) (*User, error) {

// }
