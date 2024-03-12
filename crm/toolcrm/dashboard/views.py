from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from client.models import Client
from lead.models import Lead
from team.models import Team


@login_required
def dashboard(request):
    team = Team.objects.filter(created_by=request.user)[0]
    clients = Client.objects.filter(team=team).order_by('-created_at')[:5]
    leads = Lead.objects.filter(team=team).order_by('-created_by')[:5]
    return render(request,'dashboard/dashboard.html',{'clients':clients,'leads':leads})
