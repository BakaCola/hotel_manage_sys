import os
import uuid

from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import RegexValidator

# from bootstrap_datepicker_plus.widgets import DateTimePickerInput
import bcrypt

from hotel.utils.bootstrapForm import BootStrapModelForm, BootStrapForm
from hotel.models import Account, Customer, Notice, Room, RoomType


# from hotel.utils.encrypt import md5


class AccountModelForm(BootStrapModelForm):
	account_phone = forms.CharField(
		label="手机号",
		validators=[RegexValidator(r'1[3-9]\d{9}', "手机号格式错误"), ],
		max_length=11,
	)

	account_user = forms.CharField(
		label="用户名",
		max_length=32,
		min_length=4,
		validators=[RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_]{3,31}$', "用户名须以字母开头，仅包含字母、数字、下划线"), ],

	)

	def clean_account_phone(self):
		phone = self.cleaned_data.get("account_phone")
		exist_data = Account.objects.exclude(pk=self.instance.pk).filter(account_phone=phone).exists()
		if exist_data:
			raise ValidationError("手机号已存在")
		return phone

	def clean_account_user(self):
		user = self.cleaned_data.get("account_user")
		exist_data = Account.objects.exclude(pk=self.instance.pk).filter(account_user=user).exists()
		if exist_data:
			raise ValidationError("用户名已存在")
		return user

	def clean_account_email(self):
		email = self.cleaned_data.get("account_email")
		exist_data = Account.objects.exclude(pk=self.instance.pk).filter(account_email=email).exists()
		if exist_data:
			raise ValidationError("邮箱已存在")
		return email

	class Meta:
		model = Account
		fields = ['account_user', 'account_name', 'account_phone', 'account_email', 'account_type', 'account_status']


class AccountAddModelForm(AccountModelForm):
	account_password = forms.CharField(
		label="密码",
		widget=forms.PasswordInput(),
		max_length=32,
		min_length=8,
	)

	confirm_password = forms.CharField(
		label="确认密码",
		widget=forms.PasswordInput(),
		max_length=32,
		min_length=8,
	)

	def save(self, commit=True):
		user = super().save(commit=False)
		# 对密码进行加密
		account_password = self.cleaned_data['account_password']
		salt = bcrypt.gensalt()
		hash = bcrypt.hashpw(account_password.encode(), salt)
		# 将加密后的哈希值存储到数据库中
		user.account_password = hash.decode()
		if commit:
			user.save()
		return user

	def clean(self):
		cleaned_data = super().clean()
		account_password = cleaned_data.get('account_password')
		confirm_password = cleaned_data.get('confirm_password')
		# 检查两次密码是否一致
		if account_password and confirm_password:
			if account_password != confirm_password:
				raise forms.ValidationError('两次密码输入不一致，请重新输入')
		return cleaned_data

	def clean_account_password(self):
		account_password = self.cleaned_data['account_password']
		# 如果是更新用户，需要验证用户输入的密码是否正确
		if self.instance.pk:
			# 从数据库中获取原始的哈希值
			hash = self.instance.account_password.encode()
			# 使用bcrypt来比较哈希值是否匹配
			if not bcrypt.checkpw(account_password.encode(), hash):
				raise forms.ValidationError('密码错误')
		return account_password

	class Meta:
		model = Account
		fields = ['account_user', 'account_name', 'account_password', 'confirm_password', 'account_phone',
		          'account_email', 'account_type', 'account_status']


class CustomerModelForm(BootStrapModelForm):
	customer_phone = forms.CharField(
		label="手机号",
		validators=[RegexValidator(r'1[3-9]\d{9}', "手机号格式错误"), ],
		max_length=11,
	)
	customer_idNumber = forms.CharField(
		label="身份证号",
		validators=[RegexValidator(r'\d{17}[\dXx]', "身份证号格式错误"), ],
		max_length=18,
	)

	def clean_customer_idNumber(self):
		idNumber = self.cleaned_data.get("customer_idNumber")
		idNumber = idNumber.upper()
		wList = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
		sum = 0
		for i in range(18):
			sum += int(idNumber[i]) * wList[i]
			if (i == 17 and idNumber[i] == 'X'):
				sum += 10 * wList[i]
		if (sum % 11 != 1):
			raise ValidationError("身份证号错误")
		return idNumber

	class Meta:
		model = Customer
		exclude = ['id', 'customer_status']


class NoticeModelForm(BootStrapModelForm):
	class Meta:
		model = Notice
		fields = "__all__"
		widgets = {
			"notice_time": forms.DateTimeInput(attrs={"type": "datetime-local", }),
			"notice_expiration": forms.DateTimeInput(attrs={"type": "datetime-local"}),
		}


class RoomModelForm(BootStrapModelForm):
	class Meta:
		model = Room
		fields = "__all__"


class LoginForm(BootStrapForm):
	account_user = forms.CharField(
		label="用户名",
		max_length=32,
		min_length=4,
		validators=[RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_]{3,31}$', "用户名须以字母开头，仅包含字母、数字、下划线"), ],

	)
	account_password = forms.CharField(
		label="密码",
		widget=forms.PasswordInput(),
		max_length=32,
		min_length=8,
	)

	class Meta:
		fields = ['account_user', 'account_password']


class RoomModelForm(BootStrapModelForm):
	class Meta:
		model = Room
		fields = "__all__"


class RoomTypeModelForm(BootStrapModelForm):

	def save(self, commit=True):
		# 调用父类的save方法，获取模型实例，但不保存到数据库
		image = super().save(commit=False)
		# 获取图片文件对象
		file = image.roomType_img
		# 修改图片文件的name属性，使用uuid来生成随机字符串
		file.name = str(uuid.uuid4()) + os.path.splitext(file.name)[1]
		# 根据commit参数的值来决定是否保存到数据库
		if commit:
			image.save()
		# 返回模型实例
		return image

	class Meta:
		model = RoomType
		fields = "__all__"
