from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import RegexValidator

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from hotel.utils.modelform import BootStrapModelForm
from hotel.models import Account, Customer, Notice, Room
from hotel.utils.encrypt import md5


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

	def clean_account_password(self):
		password = self.cleaned_data.get("account_password")
		if len(password) < 8:
			raise ValidationError("密码长度不能小于8位")
		if len(password) > 32:
			raise ValidationError("密码长度不能大于32位")
		return md5(password)

	def clean_account_email(self):
		email = self.cleaned_data.get("account_email")
		exist_data = Account.objects.exclude(pk=self.instance.pk).filter(account_email=email).exists()
		if exist_data:
			raise ValidationError("邮箱已存在")
		return email

	class Meta:
		model = Account
		exclude = ['account_password']


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

	def clean_confirm_password(self):
		pwd = self.cleaned_data.get("account_password")
		confirm = self.cleaned_data.get("confirm_password")
		if md5(confirm) != pwd:
			raise ValidationError("密码不一致!")
		return md5(confirm)

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
		return idNumber

	class Meta:
		model = Customer
		exclude = ['id', 'customer_status']


class NoticeModelForm(BootStrapModelForm):
	class Meta:
		model = Notice
		fields = "__all__"
		widgets = {
			"notice_time": DateTimePickerInput(options={"format": "YYYY-MM-DD HH:mm", "locale": "zh-cn"}),
			"notice_expiration": DateTimePickerInput(options={"format": "YYYY-MM-DD HH:mm", "locale": "zh-cn"}),
		}


class RoomModelForm(BootStrapModelForm):
	class Meta:
		model = Room
		fields = "__all__"
