#coding:utf8
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView,CreateView,DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Me,Assumption,Income,Other,Record,Deposit,Loan
from .forms import SearchForm
# Create your views here.
@login_required
def me(request):
    user = Me.objects.get(user_id__exact=request.user.id)
    return render_to_response('me.html',{'me':user},context_instance=RequestContext(request))

class me_update(UpdateView):
    model = Me
    fields = ['realname','sex','birth']
    template_name = 'update.html'
    success_url = '/funds/me/'

    def get_object(self, queryset=None):
        obj = super(me_update, self).get_object()
        if not obj == Me.objects.get(user_id__exact=self.request.user.id):
            raise Http404('NO PERMISSION')
        return obj

##    def get(self, request, **kwargs):
##        self.object = Me.objects.get(user_id__exact=request.user.id)
##        form_class = self.get_form_class()
##        form = self.get_form(form_class)
##        context = self.get_context_data(object=self.object, form=form)
##        return self.render_to_response(context)

class record(ListView):
    queryset = []
    template_name = 'record.html'

    def get_context_data(self, **kwargs):
        context = super(record, self).get_context_data(**kwargs)
        u = Me.objects.get(user_id__exact=self.request.user.id)
        context['Income'] = Income.objects.filter(owner__exact=u)[0:10]
        context['Other'] = Other.objects.filter(owner__exact=u)[0:10]
        context['Assumption'] = Assumption.objects.filter(owner__exact=u)[0:10]
        return context

class assum_create(CreateView):
    model = Assumption
    template_name = 'create_assum.html'
    success_url = '/funds/record/'
    fields = ['date','place','amount','items']

    def form_valid(self, form):
        obj = form.save(commit=False)
        owner = Me.objects.get(user_id__exact=self.request.user.id)
        owner.cash -= obj.amount
        owner.save()
        obj.owner = owner
        obj.save()
        return HttpResponseRedirect(self.success_url)

class income_create(CreateView):
    model = Income
    template_name = 'create_income.html'
    success_url = '/funds/record/'
    fields = ['date','place','amount','source']

    def form_valid(self, form):
        obj = form.save(commit=False)
        owner = Me.objects.get(user_id__exact=self.request.user.id)
        owner.cash += obj.amount
        owner.save()
        obj.owner = owner
        obj.save()
        return HttpResponseRedirect(self.success_url)

class other_create(CreateView):
    model = Other
    template_name = 'create_other.html'
    success_url = '/funds/record/'
    fields = ['date','place','details']

    def form_valid(self, form):
        obj = form.save(commit=False)
        owner = Me.objects.get(user_id__exact=self.request.user.id)
        obj.owner = owner
        obj.save()
        return HttpResponseRedirect(self.success_url)

class assum(ListView):
    model = Assumption
    paginate_by = 15
    template_name = 'record_assum.html'

    def get_context_data(self, **kwargs):
        context = super(assum, self).get_context_data(**kwargs)
        if 'y' in self.request.GET:
            context['y']=self.request.GET['y']
        if 'm' in self.request.GET:
            context['m']=self.request.GET['m']
            form = SearchForm(self.request.GET)
            if not form.is_valid():
                context['err']=True
            else:
                queryset = context['object_list']
                s = 0
                for obj in queryset:
                    s+=obj.amount
                context['sum']=s
        else:
            form = SearchForm()
        context['searchform']=form
        return context

    def get_queryset(self):
        u = Me.objects.get(user_id__exact=self.request.user.id)
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return Assumption.objects.filter(owner__exact=u,date__year= \
                form.cleaned_data['y'],date__month=form.cleaned_data['m'])
        return Assumption.objects.filter(owner__exact=u)


class income(ListView):
    model = Income
    paginate_by = 15
    template_name = 'record_income.html'

    def get_context_data(self, **kwargs):
        context = super(income, self).get_context_data(**kwargs)
        if 'y' in self.request.GET:
            context['y']=self.request.GET['y']
        if 'm' in self.request.GET:
            context['m']=self.request.GET['m']
            form = SearchForm(self.request.GET)
            if not form.is_valid():
                context['err']=True
            else:
                queryset = context['object_list']
                s = 0
                for obj in queryset:
                    s+=obj.amount
                context['sum']=s
        else:
            form = SearchForm()
        context['searchform']=form
        return context

    def get_queryset(self):
        u = Me.objects.get(user_id__exact=self.request.user.id)
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return Income.objects.filter(owner__exact=u,date__year=form.cleaned_data['y'],\
                    date__month=form.cleaned_data['m'])
        return Income.objects.filter(owner__exact=u)

class other(ListView):
    model = Other
    paginate_by = 15
    template_name = 'record_other.html'

    def get_context_data(self, **kwargs):
        context = super(other, self).get_context_data(**kwargs)
        if 'y' in self.request.GET:
            context['y']=self.request.GET['y']
        if 'm' in self.request.GET:
            context['m']=self.request.GET['m']
            form = SearchForm(self.request.GET)
            if not form.is_valid():
                context['err']=True
        else:
            form = SearchForm()
        context['searchform']=form
        return context

    def get_queryset(self):
        u = Me.objects.get(user_id__exact=self.request.user.id)
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return Other.objects.filter(owner__exact=u,date__year=form.cleaned_data['y'],\
                    date__month=form.cleaned_data['m'])
        return Other.objects.filter(owner__exact=u)

class deposit_create(CreateView):
    model = Deposit
    template_name = 'create_deposit.html'
    success_url = '/funds/account/'
    fields = ['name','balance','deposit_type','bank','opening_date']

    def form_valid(self, form):
        obj = form.save(commit=False)
        owner = Me.objects.get(user_id__exact=self.request.user.id)
        obj.owner = owner
        obj.save()
        return HttpResponseRedirect(self.success_url)

class loan_create(CreateView):
    model = Loan
    template_name = 'create_loan.html'
    success_url = '/funds/account/'
    fields = ['name','amount','loan_type','bank','opening_date']

    def form_valid(self, form):
        obj = form.save(commit=False)
        owner = Me.objects.get(user_id__exact=self.request.user.id)
        obj.owner = owner
        obj.save()
        return HttpResponseRedirect(self.success_url)

class account(ListView):
    queryset = []
    template_name = 'account.html'
    def get_context_data(self, **kwargs):
        context = super(account, self).get_context_data(**kwargs)
        u = Me.objects.get(user_id__exact=self.request.user.id)
        context['loan'] = Loan.objects.filter(owner__exact=u)
        context['deposit'] = Deposit.objects.filter(owner__exact=u)
        return context

class deposit_delete(DeleteView):
    model = Deposit
    template_name = 'delete_confirm.html'
    success_url = '/funds/account/'

    def get_object(self, queryset=None):
        obj = super(deposit_delete, self).get_object()
        if not obj.owner == Me.objects.get(user_id__exact=self.request.user.id):
            raise Http404('NO PERMISSION')
        return obj

class loan_delete(DeleteView):
    model = Loan
    template_name = 'delete_confirm.html'
    success_url = '/funds/account/'

    def get_object(self, queryset=None):
        obj = super(loan_delete, self).get_object()
        if not obj.owner == Me.objects.get(user_id__exact=self.request.user.id):
            raise Http404('NO PERMISSION')
        return obj

class deposit_update(UpdateView):
    model = Deposit
    fields = ['name','balance','deposit_type','bank','opening_date']
    template_name = 'update.html'
    success_url = '/funds/account/'

    def get_object(self, queryset=None):
        obj = super(deposit_update, self).get_object()
        if not obj.owner == Me.objects.get(user_id__exact=self.request.user.id):
            raise Http404('NO PERMISSION')
        return obj

class loan_update(UpdateView):
    model = Loan
    fields = ['name','amount','loan_type','bank','opening_date']
    template_name = 'update.html'
    success_url = '/funds/account/'

    def get_object(self, queryset=None):
        obj = super(deposit_update, self).get_object()
        if not obj.owner == Me.objects.get(user_id__exact=self.request.user.id):
            raise Http404('NO PERMISSION')
        return obj

class assum_update(UpdateView):
    model = Assumption
    template_name = 'update.html'
    success_url = '/funds/record/assum/'
    fields = ['date','place','amount','items']

    def get_object(self, queryset=None):
        obj = super(assum_update, self).get_object()
        if not obj.owner == Me.objects.get(user_id__exact=self.request.user.id):
            raise Http404('NO PERMISSION')
        return obj

class income_update(UpdateView):
    model = Income
    template_name = 'update.html'
    success_url = '/funds/record/income/'
    fields = ['date','place','amount','source']

    def get_object(self, queryset=None):
        obj = super(income_update, self).get_object()
        if not obj.owner == Me.objects.get(user_id__exact=self.request.user.id):
            raise Http404('NO PERMISSION')
        return obj

class other_update(UpdateView):
    model = Other
    template_name = 'update.html'
    success_url = '/funds/record/other/'
    fields = ['date','place','details']

    def get_object(self, queryset=None):
        obj = super(other_update, self).get_object()
        if not obj.owner == Me.objects.get(user_id__exact=self.request.user.id):
            raise Http404('NO PERMISSION')
        return obj
