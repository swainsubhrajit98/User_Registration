from django.shortcuts import render
from App.forms import *
from django.http import HttpResponse
# Create your views here.

def Home(request):
    return render(request,'Home.html')
def Registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        if UD.is_valid() and PD.is_valid():
            pw=UD.cleaned_data['password']
            USO=UD.save(commit=False)
            USO.set_password(pw)
            USO.save()

            PO=PD.save(commit=False)
            PO.user=USO
            PO.save()
            return HttpResponse('Register Successfully Done!!!')
    return render(request,'Registration.html',d)