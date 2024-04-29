from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from wagtail.models import Page
from django.urls import reverse_lazy
from equipment.models import Profile
from django.shortcuts import get_object_or_404



# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# from wagtail.contrib.search_promotions.models import Query


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'Profile/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class CreateProfilePageView(CreateView):
    model = Profile

    template_name = 'Profile/create_profile.html'
    fields = ['profile_pic', 'user', "name", 'city', 'bio', 'achievements', 'VK','Telegram', 'WhatsApp','mail']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('tasks')