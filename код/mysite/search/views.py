from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from django.views.generic.detail import DetailView
from equipment.models import *
from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login
from mysite.forms import PostForm, RegisterForm, ProfileForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.mixins import LoginRequiredMixin
# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# Create your models here.

@receiver(post_save, sender=Profile)
def update_user_info(sender, instance, created, **kwargs):
    if created:
        instance.user.first_name = instance.firstname
        instance.user.last_name = instance.lastname
    else:
        instance.user.first_name = instance.firstname
        instance.user.last_name = instance.lastname
    instance.user.save()

class RegisterView(TemplateView):
    template_name = "Registration/register.html"

    def check_existing_user(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(self.request, "Пользователь с таким логином уже зарегистрирован.")
            return True
        if User.objects.filter(email=email).exists():
            messages.error(self.request, "Пользователь с такой почтой уже зарегистрирован.")
            return True
        return False

    def create_new_user(self, form):
        if not self.check_existing_user(form):
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()

        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                if self.check_existing_user(form):
                    context = {
                        'form': form
                    }
                    return render(request, self.template_name, context)
                else:
                    self.create_new_user(form)
                    messages.success(request, "Вы успешно зарегистрировались!")
                    return redirect("login")

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

'''class RegisterView(TemplateView):
    template_name = "Registration/register.html"
    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()

        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                self.create_new_user(form)
                messages.success(request, "Вы успешно зарегистрировались!")
                return redirect("login")

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


    def create_new_user(self, form: RegisterForm):
        User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data.get("email"),
            password=form.cleaned_data['password'],

        )'''

class LoginView(TemplateView):
    template_name = "Registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return render(request, self.template_name)

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Неверный логин или пароль")
                return render(request, self.template_name)

            login(request, user)

            profile = Profile.objects.filter(user=request.user).first()
            if not profile:
                return redirect("edit_profile", pk=request.user.pk)
            else:
                return redirect("profile", pk=request.user.pk)

class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")

class ProfileView(TemplateView):
    template_name = "Registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])

        context = {
            'profile': profile
        }

        return render(request, self.template_name, context)

class EditProfileView(TemplateView):
    template_name = "Registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()

                messages.success(request, "Профиль успешно обновлен!")
                return redirect("profile", pk = request.user.pk)

        return render(request, self.template_name, {'form': form})

    def get_profile(self, user: User) -> Profile | None:
        if not Profile.objects.filter(user=user).exists():
            return None

        return user.profile

class HomeView(TemplateView):
    template_name = "HomePage/home.html"

'''class PostView(TemplateView):

    timeline_template_name = "PostPage/timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect("post_view")

        if 'delete_post_id' in request.POST:
            post_id_to_delete = request.POST.get('delete_post_id')
            post_to_delete = Post.objects.filter(author=request.user, id=post_id_to_delete)
            if post_to_delete.exists():
                post_to_delete.delete()

        context = {
            'posts': Post.objects.all()
        }
        return render(request, self.timeline_template_name, context)'''

class PostView(TemplateView):

    timeline_template_name = "PostPage/timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()

                return redirect("post_view")

        context = {
            'posts': Post.objects.all()
        }
        return render(request, self.timeline_template_name, context)

class DeletePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
            if post.author == request.user:
                post.delete()
        except Post.DoesNotExist:
            # Handle the case when the post does not exist
            pass

        return redirect('post_view')  # Redirect to the post list view after deletion

class PostCommentView(View):
    def dispatch(self, request, *args, **kwargs):
        post_id = request.GET.get("post_id")
        comment = request.GET.get("comment")

        if comment and post_id:
            post = Post.objects.get(pk=post_id)

            comment = Comment(text=comment, post=post, author=request.user.profile)
            comment.save()

            return render(request, "mysite/templates/blocks/comment.html", {'comment': comment})

        return HttpResponse(status=400)





class SupportView(TemplateView):
    template_name = "Stuff/support.html"

class AboutUs(TemplateView):
    template_name = "Stuff/aboutus.html"

class Reviews(TemplateView):
    template_name = "Stuff/reviews.html"
    #Тут еще что-то будет

class SupportCreators(TemplateView):
    template_name = "Stuff/supportcreators.html"


'''class ShowProfilePageView(DetailView):
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
    form_class = ProfileForm'''

