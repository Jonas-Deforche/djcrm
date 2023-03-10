from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.views import generic
from .forms import LeadModelForm, CustomUserCreationForm, UsernameField
from .models import Lead
from django.contrib.auth.mixins import LoginRequiredMixin


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads}
    return render(request, "leads/lead_list.html", context)


def lead_detail(LoginRequiredMixin, request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        print("receiving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # todo send email
        send_mail(
            subject="a lead has been created",
            message="go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == 'POST':
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        'form': form,
        'lead': lead
    }
    return render(request, "leads/lead_update.html", context)


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

    # def lead_update(request, pk):
    #     lead = Lead.objects.get(id=pk)
    #     form = LeadForm()
    #     if request.method == 'POST':
    #         form = LeadForm(request.POST)
    #         if form.is_valid():
    #             first_name = form.cleaned_data['first_name']
    #             last_name = form.cleaned_data['last_name']
    #             age = form.cleaned_data['age']
    #             lead.first_name = first_name
    #             lead.last_name = last_name
    #             lead.age = age
    #             lead.save()
    #             return redirect("/leads")
    #     context = {
    #         "form": form,
    #         "lead": lead
    #     }

# def lead_create(request):
#    form = LeadForm()
#    if request.method == 'POST':
#        print("receiving a post request")
#        form = LeadForm(request.POST)
#        if form.is_valid():
#            print("form is valid")
#            print(form.cleaned_data)
#            first_name = form.cleaned_data['first_name']
#            last_name = form.cleaned_data['last_name']
#            age = form.cleaned_data['age']
#            agent = Agent.objects.first()
#            Lead.objects.create(
#                first_name=first_name,
#                last_name=last_name,
#                age=age,
#                agent=agent
#            )
#            print("the lead is created")
#            return redirect("/leads")
#    context = {
#        "form": form
#    }
#    return render(request, "leads/lead_create.html", context)
