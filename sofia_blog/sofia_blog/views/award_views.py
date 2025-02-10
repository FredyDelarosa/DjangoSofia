from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.award import Award
from ..forms.award_form import AwardForm

class AwardListView(ListView):
    model = Award
    template_name = "awards/award_list.html"
    context_object_name = "awards"

class AwardDetailView(DetailView):
    model = Award
    template_name = "awards/award_detail.html"
    context_object_name = "award"

class AwardCreateView(LoginRequiredMixin, CreateView):
    model = Award
    form_class = AwardForm
    template_name = "awards/award_form.html"
    success_url = reverse_lazy('award_list')

class AwardUpdateView(LoginRequiredMixin, UpdateView):
    model = Award
    form_class = AwardForm
    template_name = "awards/award_form.html"
    success_url = reverse_lazy('award_list')

class AwardDeleteView(LoginRequiredMixin, DeleteView):
    model = Award
    template_name = "awards/award_confirm_delete.html"
    success_url = reverse_lazy('award_list')
