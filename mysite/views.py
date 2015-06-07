#coding utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext

from .forms import LoginForm,ChangepwForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/home')
        else:
            error = True
            return render_to_response('login.html', {'form': form,'error':error})
    elif request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    else:
        form = LoginForm()
        return render_to_response('login.html', {'form': form,})

@login_required
def home(request):
    return render_to_response('index.html',context_instance=RequestContext(request))

@login_required
def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

@login_required
def changepw(request):
    if request.method == 'GET':
        form = ChangepwForm()
        return render_to_response('changepw.html', RequestContext(request, {'form': form,}))
    else:
        form = ChangepwForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword')
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1')
                user.set_password(newpassword)
                user.save()
                return render_to_response('changepwsd.html')
            else:
                return render_to_response('changepw.html', RequestContext(request, {'form': form,'oldpassword_is_wrong':True}))
        else:
            return render_to_response('changepw.html', RequestContext(request, {'form': form,}))