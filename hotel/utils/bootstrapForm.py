from django import forms


class BootStrapModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for _, filed in self.fields.items():
			if filed.widget.attrs:
				filed.widget.attrs["class"] = "form-control"
			else:
				filed.widget.attrs = {
					"class": "form-control",
				}


class BootStrapForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for _, filed in self.fields.items():
			if filed.widget.attrs:
				filed.widget.attrs["class"] = "form-control"
			else:
				filed.widget.attrs = {
					"class": "form-control",
				}