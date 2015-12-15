#from apps.hello.forms import ContactForm
#from apps.hello.models import User
from apps.hello.models import User
from django.shortcuts import render

# Create your views here.
def home(request):
    queryset = User.objects.get(pk=1)
    context = {
        "contacts": queryset
    }
    print(queryset)
    return render(request, "base.html", context)
