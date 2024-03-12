from django.shortcuts import render,redirect,get_object_or_404
from .models import Client,ClientFile
from .forms import client_form,comment_form,file_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from team.models import Team
from django.http import HttpResponse
import csv

@login_required
def client_export(request):
    clients = Client.objects.filter(created_by=request.user)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition':'attachment; filename="clients.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Client','Description','Created_at','Created_by'])
    for client in clients:
        writer.writerow([client.name,client.description,client.created_at,client.created_by])
    return response



    

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)
    return render(request,'clients/clients_list.html',{'clients':clients})

@login_required
def client_add(request):
    if request.method == 'POST':
        form = client_form(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = request.user.userprofile.active_team
            client.save()
            
            messages.success(request,'Client has been added')
            return redirect('clients:list')

    else:
        form = client_form()
    return render(request,'clients/add_client.html',{'form':form,'team':team})

@login_required
def client_detail(request,pk):
    client = get_object_or_404(Client,pk=pk,created_by=request.user)
    form = comment_form()
    fileform = file_form()
    return render(request,'clients/client_detail.html',{'client':client,'form':form,'fileform':fileform})

@login_required
def client_add_file(request,pk):
    client = get_object_or_404(Client,created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = file_form(request.POST,request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = request.user.userprofile.active_team
            file.client_id = pk
            file.created_by = request.user
            file.save()

            messages.success(request,'File added') 
        return redirect('clients:detail',pk=pk)
    return redirect('clients:detail',pk=pk)


@login_required
def client_delete(request,pk):
    client = get_object_or_404(Client,pk=pk,created_by=request.user)
    client.delete()
    messages.success(request,'This client has been deleted')
    return redirect('clients:list')

@login_required
def add_comment(request,pk):
    client = get_object_or_404(Client,pk=pk)

    if request.method == 'POST':
        form = comment_form(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = request.user.userprofile.active_team
            comment.created_by = request.user
            comment.client = client
            comment.save()

            messages.success(request,'Comment added')
            return redirect('clients:detail',pk=pk)
    else:
        form = comment_form()
    return render(request,'clients/client_detail.html',{'form':form,'client':client})


@login_required
def client_edit(request,pk):
    client = get_object_or_404(Client,pk=pk,created_by=request.user)
    if request.method == 'POST':
        form = client_form(request.POST,instance=client)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            messages.success(request,'Client details updated')
            return redirect('clients:list',pk=pk)
    else:
        form = client_form(instance=client)
    return render(request,'clients/client_edit.html',{'form':form})
