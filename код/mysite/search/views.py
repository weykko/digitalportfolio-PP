from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from equipment.models import *
from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm

# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'Profile/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(**kwargs)

        # Get the page user based on the pk from the URL
        page_user = get_object_or_404(Profile, pk=self.kwargs['pk'])

        context['page_user'] = page_user
        return context

class CreateProfilePageView(CreateView):
    model = Profile

    template_name = 'Profile/create_profile.html'
    fields = ['profile_pic', 'user', "firstname", "lastname", 'city', 'bio', 'achievements', 'VK','Telegram', 'WhatsApp']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'user',"firstname", "lastname", 'city', 'bio', 'achievements', 'VK','Telegram', 'WhatsApp']

class EditProfilePageView(UpdateView):
    model = Profile
    template_name = 'Profile/edit_profile_page.html'
    form_class = ProfileForm


class HomeView(TemplateView):
    template_name = "HomePage/index.html"

class PostView(TemplateView):
    #template_name = "HomePage/index.html"
    timeline_template_name = "PostPage/timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        context = {
            'posts': Post.objects.all()
        }
        return render(request, self.timeline_template_name, context)


class PostCommentView(View):
    def dispatch(self, request, *args, **kwargs):
        post_id = request.GET.get("post_id")
        comment = request.GET.get("comment")

        if comment and post_id:
            post = Post.objects.get(pk=post_id)

            comment = Comment(text=comment, post=post, author=request.user)
            comment.save()

            return render(request, "blocks/comment.html", {'comment': comment})

        return HttpResponse(status=400)