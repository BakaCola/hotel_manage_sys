import codecs
import subprocess

from django.http import HttpResponse
from django.shortcuts import render, redirect

from hotel.forms.forms import RecoverDBForm


def backup_db(request):
	output = subprocess.check_output(['python', 'manage.py', 'dumpdata'])
	with open('database_backup.json', 'wb') as file:
		file.write(output)

	response = HttpResponse(content_type='application/json')
	response['Content-Disposition'] = 'attachment; filename="database_backup.json"'
	response.write(output)
	return response


def recover_db(request):
	if request.method == "GET":
		form = RecoverDBForm()
		return render(request, 'recover_db.html', {'form': form})
	form = RecoverDBForm(request.POST, request.FILES)
	if form.is_valid():
		file = request.FILES.get('file')
		try:
			with open('database_backup.json', 'wb') as f:
				for chunk in file.chunks():
					chunk = chunk.decode('GBK').encode('utf-8')
					f.write(chunk)
			subprocess.check_output(['python', 'manage.py', 'loaddata', 'database_backup.json'])
		except Exception as e:
			print(e)
			return redirect('/alert/?code=405')
		return redirect('/alert/?code=201')
	return render(request, 'recover_db.html', {'form': form})
