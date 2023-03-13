from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent


# Create your views here.
class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        return Agent.objects.all()


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = none

    def get_success_url(self):
        return reverse("agents:agents-list")
