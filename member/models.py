from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('올바른 이메일을 입력하세요.')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user
# 암호화는 qwer1234 -> asfaer231 -> 복호화 ->qwer1234
# 해시화 qwer1234 -> asdasd/zxdfsf -> 암호화(asdasd) -> 암호화를 반복 -> qwerqrq -> 복호화가 불가능
# Django => SHA256
# 비밀번호는 일반적으로 해시화가 된다.. 따라서 'user.password = password' 로 적지 않는다.

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        unique=True,
    )


    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField('nickname', max_length=20, unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    WMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    # user.is_superuser() ==> X
    # user.is_superuser로 쓸수 있게 만드는것이 @property