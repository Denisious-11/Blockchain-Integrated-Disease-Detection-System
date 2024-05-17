from .models import *
from django.http import HttpResponse, JsonResponse

def temp_del(request):
	obj1=Requests.objects.all().delete()
	obj1=Patient.objects.all().delete()
	obj1=Record.objects.all().delete()

	return HttpResponse("<script>alert('Data Deleted Successfully');window.location.href='/show_home_admin/'</script>")