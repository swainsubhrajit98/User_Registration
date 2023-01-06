from django.shortcuts import render
from App.forms import *
from django.http import HttpResponse,HttpResponsePermanentRedirect
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.


def Home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'Home.html',d)
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
            
            
            send_mail('registration',
                'Successfully Registered',
                '99swain@gmail.com',
                [USO.email],
                fail_silently=False)
            
            return HttpResponse('Register Successfully Done!!!')
    return render(request,'Registration.html',d)


def User_Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponsePermanentRedirect(reverse('Home'))
    return render(request,'User_Login.html')
@login_required
def User_LogOut(request):
    logout(request)
    return HttpResponsePermanentRedirect(reverse(Home))