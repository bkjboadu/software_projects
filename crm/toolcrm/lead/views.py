from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,View
from django.views.generic.edit import UpdateView,CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import lead_form,comment_form,file_form
from .models import Lead
from django.contrib import messages
from client.models import Client
from team.models import Team
from django.http import HttpResponse
from client.models import Client,Comment as ClientComment
import csv

@login_required
def lead_export(request):
    leads = Lead.objects.filter(created_by=request.user)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition':'attachment; filename="leads.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Lead','Description','Created_at','Created_by'])
    for lead in leads:
        writer.writerow([lead.name,lead.description,lead.created_at,lead.created_by])
    return response

class ConvertToClientView(LoginRequiredMixin,View):

    def get(self,request,pk,*args,**kwargs):
        lead = get_object_or_404(Lead,created_by=request.user,pk=pk)
        team = Team.objects.filter(created_by=request.user).filter()
        client = Client.objects.create(name=lead.name,email=lead.email,
                                       description=lead.description,created_by=request.user,
                                       team=team)
        lead.converted_to_client = True
        lead.save()

        comments = lead.comments.all()

        for comment in comments:
            ClientComment.objects.create(team=team,
                                         client=client,
                                         content=comment.content,
                                         created_by=request.user
                                         )


        messages.success(request,'Lead converted to client')
        return redirect('leads:list')
    
    def post(self,request,*args,**kwargs):
        return HttpResponseRedirect(reverse_lazy('leads:list'))
    

class LeadUpdateView(LoginRequiredMixin,UpdateView):
    model = Lead
    form_class = lead_form
    success_url = reverse_lazy('leads:list')
    template_name = 'lead/leads_edit.html'

    def get_object(self):
        return get_object_or_404(Lead,created_by=self.request.user,pk=self.kwargs['pk'])
    
    def form_valid(self,form):
        messages.success(self.request,'This lead has been edited')
        return super().form_valid(form)


class LeadCreateView(LoginRequiredMixin,CreateView):
    model = Lead
    template_name = 'lead/add_lead.html'
    form_class = lead_form
    success_url = reverse_lazy('leads:list')

    def form_valid(self,form):
        team = Team.objects.filter(created_by=self.request.user).first()
        form.instance.created_by = self.request.user
        form.instance.team = team
        messages.success(self.request,'The lead was created')
        return super().form_valid(form)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.filter(created_by=self.request.user).first()
        return context

class LeadDetailView(LoginRequiredMixin,DetailView):
    model = Lead
    template_name = 'lead/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        return Lead.objects.filter(created_by=self.request.user,pk=self.kwargs['pk'])
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form']= comment_form()
        context['fileform'] = file_form()
        return context

class AddFileView(View):
    def post(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        form = file_form(request.POST,request.FILES)

        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user).first()
            fileform = form.save(commit=False)
            fileform.team = team
            fileform.lead_id = pk
            fileform.created_by = request.user
            fileform.save()

            messages.success(request,'File added')
        return redirect('leads:detail',pk=pk)
    
class AddCommentView(View):
    def post(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        form = comment_form(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user)[0]
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk

            comment.save()
        return redirect('leads:detail',pk=pk)

        

class LeadListView(LoginRequiredMixin,ListView):
    model = Lead
    template_name = 'lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        return Lead.objects.filter(created_by=self.request.user,converted_to_client=False)


@login_required
def leads_delete(request,pk):
    lead = get_object_or_404(Lead,created_by=request.user,pk=pk)
    lead.delete()
    messages.success(request,'The lead was deleted')
    return redirect('leads:list')

@login_required
def lead_edit(request,pk):
    lead = get_object_or_404(Lead,created_by=request.user,pk=pk)

    if request.method == 'POST':
        form = lead_form(request.POST,instance=lead)

        if form.is_valid():
            form.save()
            messages.success(request,'This lead has been edited')
            return redirect('leads:list')
    else:
        form = lead_form(instance=lead)
    return render(request,'lead/leads_edit.html',{'form':form})

@login_required
def convert_to_client(request,pk):
    lead = get_object_or_404(Lead,created_by=request.user,pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]
    client = Client.objects.create(name=lead.name,
                                   email=lead.email,
                                   description=lead.description,
                                   created_by = request.user,
                                   team=team)
    lead.converted_to_client = True
    lead.save()

    messages.success(request,'lead convert to client')
    return redirect('leads:list')


# class LeadDeleteView(LoginRequiredMixin,DeleteView):
#     model = Lead
#     success_url = reverse_lazy('leads:list')
#     template_name = ''

#     def get_queryset(self):
#         return Lead.objects.filter(created_by=self.request.user,pk=self.kwargs['pk'])
    
#     def delete(self,request,*args,**kwargs):
#         self.object = self.get_object()
#         success_url = self.get_success_url()
#         self.object.delete()
#         return self.redirect_to_response(success_url)

    # def get_object(self):
    #     return get_object_or_404(Lead,created_by=self.request.user,pk=self.kwargs['pk'])
    
    # def delete(self,request,*args,**kwargs):
    #     response = super().delete(request,*args,**kwargs)
    #     messages.success(request,'The lead was deleted')
    #     return response

# @login_required
# def lead_detail(request,pk):
#     lead = get_object_or_404(Lead,created_by=request.user,pk=pk)
#     return render(request,'lead/lead_detail.html',{'lead':lead})

# @login_required
# def leads_list(request):
#     leads = Lead.objects.filter(created_by=request.user,converted_to_client=False)
#     return render(request,'lead/all_leads.html',{'leads':leads})

#@login_required
# def add_lead(request):
#     team = Team.objects.filter(created_by=request.user)[0]
#     if request.method == 'POST':
#         form = lead_form(request.POST)

#         if form.is_valid():
#             team = Team.objects.filter(created_by=request.user)[0]
#             lead = form.save(commit=False)
#             lead.created_by = request.user
#             lead.team = team
#             lead.save()

#             messages.success(request,'The lead was created')
#             return redirect('leads:list')
#     else:
#         form = lead_form()
#     return render(request,'lead/add_lead.html',{'form':form,'team':team})
