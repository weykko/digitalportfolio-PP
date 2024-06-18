# from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
# from django.views import View
# from django.views.generic import CreateView, UpdateView, TemplateView
# from django.views.generic.detail import DetailView
# from equipment.models import *
# from django.shortcuts import get_object_or_404, render
# from django.forms import ModelForm
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.shortcuts import redirect, render
# from django.views.generic import TemplateView
# from django.contrib.auth import logout, authenticate, login
# from mysite.forms import PostForm, RegisterForm, ProfileForm
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# from django.db.models import Count
# from django.db.models.functions import Length
# from django import forms
# from django.db.models import Q
# import logging
# # To enable logging of search queries for use with the "Promoted search results" module
# # <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# # uncomment the following line and the lines indicated in the search function
# # (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):
#
# # Create your models here.
#
# @receiver(post_save, sender=Profile)
# def update_user_info(sender, instance, created, **kwargs):
#     if created:
#         instance.user.first_name = instance.firstname
#         instance.user.last_name = instance.lastname
#     else:
#         instance.user.first_name = instance.firstname
#         instance.user.last_name = instance.lastname
#     instance.user.save()
#
# class RegisterView(TemplateView):
#     template_name = "Registration/register.html"
#
#     def check_existing_user(self, form):
#         username = form.cleaned_data.get('username')
#         email = form.cleaned_data.get('email')
#         if User.objects.filter(username=username).exists():
#             messages.error(self.request, "Пользователь с таким логином уже зарегистрирован.")
#             return True
#         if User.objects.filter(email=email).exists():
#             messages.error(self.request, "Пользователь с такой почтой уже зарегистрирован.")
#             return True
#         return False
#
#     def create_new_user(self, form):
#         if not self.check_existing_user(form):
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             User.objects.create_user(username=username, email=email, password=password)
#
#     def dispatch(self, request, *args, **kwargs):
#         form = RegisterForm()
#
#         if request.method == 'POST':
#             form = RegisterForm(request.POST)
#
#             if form.is_valid():
#                 if self.check_existing_user(form):
#                     context = {
#                         'form': form
#                     }
#                     return render(request, self.template_name, context)
#                 else:
#                     self.create_new_user(form)
#                     messages.success(request, "Вы успешно зарегистрировались!")
#                     return redirect("login")
#
#         context = {
#             'form': form
#         }
#         return render(request, self.template_name, context)
#
#
# class LoginView(TemplateView):
#     template_name = "Registration/login.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             return render(request, self.template_name)
#
#         if request.method == 'POST':
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#             if user is None:
#                 messages.error(request, "Неверный логин или пароль")
#                 return render(request, self.template_name)
#
#             login(request, user)
#
#             profile = Profile.objects.filter(user=request.user).first()
#             if not profile:
#                 return redirect("edit_profile", pk=request.user.pk)
#             else:
#                 return redirect("profile", pk=request.user.pk)
#
# class LogoutView(View):
#     def dispatch(self, request, *args, **kwargs):
#         logout(request)
#         return redirect("/")
#
#
# class ProfileView(TemplateView):
#     template_name = "Registration/profile.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         profile = get_object_or_404(Profile, pk=kwargs['pk'])
#         form = PostForm() if request.user.is_authenticated else None
#
#         if request.method == 'POST' and request.user.is_authenticated:
#             form = PostForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.instance.author = request.user
#                 form.save()
#                 return redirect("profile", pk=kwargs['pk'])
#
#         user_posts = Post.objects.filter(author=profile.user) if profile else None
#
#         context = {
#             'profile': profile,
#             'posts': user_posts,
#             'form': form,
#         }
#         return render(request, self.template_name, context)
#
# class EditProfileView(TemplateView):
#     template_name = "Registration/edit_profile.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         form = ProfileForm(instance=self.get_profile(request.user))
#
#         if request.method == 'POST':
#             form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
#             if form.is_valid():
#                 form.instance.user = request.user
#                 form.save()
#
#                 messages.success(request, "Профиль успешно обновлен!")
#                 return redirect("profile", pk = request.user.pk)
#
#         return render(request, self.template_name, {'form': form})
#
#     def get_profile(self, user: User) -> Profile | None:
#         if not Profile.objects.filter(user=user).exists():
#             return None
#
#         return user.profile
#
#
# class CityFilterForm(forms.Form):
#     city = forms.ChoiceField(choices=[], required=False, label="Выберите город")
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         unique_cities = Profile.objects.values_list('city', flat=True).distinct()
#         self.fields['city'].choices = [('', 'Все города')] + [(city, city) for city in unique_cities if city]
#         self.fields['city'].widget.attrs.update({'class': 'custom-select'})
#
# class PostView(TemplateView):
#     timeline_template_name = "PostPage/timeline.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             form = PostForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.instance.author = request.user
#                 form.save()
#                 return redirect("post_view")
#
#         # Начинаем с получения всех постов
#         posts = Post.objects.all()
#         # Получаем параметр сортировки из GET-запроса (по умолчанию сортируем по дате)
#         sort_by = request.GET.get('sort_by', 'datetime')
#         # Фильтрация по наличию фото
#         has_photo = Post.has_photo(Post)
#         if has_photo == 'true':
#             posts = posts.filter(image__isnull=False)
#         elif has_photo == 'false':
#             posts = posts.filter(image__isnull=True)
#
#         # Фильтрация по городу
#         city_filter_form = CityFilterForm(request.GET)
#         if city_filter_form.is_valid() and city_filter_form.cleaned_data['city']:
#             city = city_filter_form.cleaned_data.get('city')
#             posts = posts.filter(author__profile__city=city)
#
#
#         # Сортировка
#         if sort_by == 'date_new':
#             posts = posts.order_by('-datetime')
#         elif sort_by == 'date_old':
#             posts = posts.order_by('datetime')
#         elif sort_by == 'character_count_large':
#             posts = posts.annotate(text_length=Length('text')).order_by('-text_length')
#         elif sort_by == 'character_count':
#             posts = posts.annotate(text_length=Length('text')).order_by('text_length')
#         elif sort_by == 'likes':
#             posts = posts.order_by('-likes')
#         elif sort_by == 'comments':
#             posts = posts.annotate(num_comments=Count('comments')).order_by('-num_comments')
#
#         context = {
#             'city_filter_form': city_filter_form,
#             'posts': posts,
#         }
#         return render(request, self.timeline_template_name, context)
#
#
# class DeletePostView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         post_id = kwargs.get('post_id')
#         try:
#             post = Post.objects.get(id=post_id)
#             if post.author == request.user:
#                 post.delete()
#         except Post.DoesNotExist:
#             pass
#
#         return redirect(request.META.get('HTTP_REFERER', 'post_view'))
#
# @login_required
# def add_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.method == "POST":
#         text = request.POST.get("text")
#         comment = Comment.objects.create(post=post, author=request.user, text=text)
#     return redirect(request.META.get('HTTP_REFERER', 'post_view'))
#
# @login_required
# def delete_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#
#     post_id = comment.post.id
#     comment.delete()
#     return redirect(request.META.get('HTTP_REFERER', 'post_view'))
#
# def like_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user in post.likes.all():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#     return redirect(request.META.get('HTTP_REFERER', 'post_view'))
#
# @method_decorator(login_required, name='dispatch')
# class ProfileFollowingCreateView(View):
#     """
#     Создание подписки для пользователей
#     """
#     model = Profile
#
#     def is_ajax(self):
#         return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'
#
#     def post(self, request, kwargs):
#         user = get_object_or_404(Profile, pk=kwargs['pk'])
#         profile = request.user.profile
#         if profile in user.followers.all():
#             user.followers.remove(profile)
#             message = f'Подписаться на {user}'
#             status = False
#         else:
#             user.followers.add(profile)
#             message = f'Отписаться от {user}'
#             status = True
#         data = {
#             'username': profile.user.username,
#             'get_absolute_url': profile.get_absolute_url(),
#             'slug': profile.slug,
#             'avatar': profile.get_avatar,
#             'message': message,
#             'status': status,
#         }
#         return JsonResponse(data, status=200)
#
#
# def post_list(request):
#     # Получаем параметр сортировки из GET-запроса (по умолчанию сортируем по дате)
#     sort_by = request.GET.get('sort_by', 'datetime')
#
#     if sort_by == 'date':
#         posts = Post.objects.all().order_by('-datetime')
#     elif sort_by == 'character_count':
#         posts = Post.objects.all().annotate(text_length=Length('text')).order_by('text_length')
#     elif sort_by == 'image_first':
#         posts_with_image = Post.objects.filter(image__isnull=False)
#         posts_without_image = Post.objects.filter(image__isnull=True)
#         posts = list(posts_with_image) + list(posts_without_image)
#     elif sort_by == 'likes':
#         posts = Post.objects.all().annotate(like_count=Count('likes')).order_by('-like_count')
#     else:
#         posts = Post.objects.all()
#
#     context = {
#         'posts': posts
#     }
#     return render(request, 'post_list.html', context)
#
# class SupportView(TemplateView):
#     template_name = "Stuff/support.html"
#
# class AboutUs(TemplateView):
#     template_name = "Stuff/aboutus.html"
#
# class Reviews(TemplateView):
#     template_name = "Stuff/reviews.html"
#     #Тут еще что-то будет
#
# class SupportCreators(TemplateView):
#     template_name = "Stuff/supportcreators.html"
#
# class HomeView(TemplateView):
#     template_name = "HomePage/home.html"
#
# def search_profiles(request):
#     query = request.GET.get('q')
#     if query:
#         query_words = query.split()
#         q_objects = Q()
#         for word in query_words:
#             q_objects |= Q(firstnameicontains=word) | Q(lastnameicontains=word)
#
#         results = Profile.objects.filter(q_objects)
#     else:
#         results = Profile.objects.none()
#
#     context = {
#         'results': results,
#     }
#     return render(request, 'Search/search_profiles.html', context)
#
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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import Length
from django import forms
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils.text import slugify
import logging
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
        form = PostForm() if request.user.is_authenticated else None

        if request.method == 'POST' and request.user.is_authenticated:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect("profile", pk=kwargs['pk'])

        user_posts = Post.objects.filter(author=profile.user) if profile else None

        context = {
            'profile': profile,
            'posts': user_posts,
            'form': form,
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


class CityFilterForm(forms.Form):
    city = forms.ChoiceField(choices=[], required=False, label="Выберите город")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_cities = Profile.objects.values_list('city', flat=True).distinct()
        self.fields['city'].choices = [('', 'Все города')] + [(city, city) for city in unique_cities if city]
        self.fields['city'].widget.attrs.update({'class': 'custom-select'})

class PostView(TemplateView):
    timeline_template_name = "PostPage/timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect("post_view")

        # Начинаем с получения всех постов
        posts = Post.objects.all()
        # Получаем параметр сортировки из GET-запроса (по умолчанию сортируем по дате)
        sort_by = request.GET.get('sort_by', 'datetime')
        # Фильтрация по наличию фото
        has_photo = Post.has_photo(Post)
        if has_photo == 'true':
            posts = posts.filter(image__isnull=False)
        elif has_photo == 'false':
            posts = posts.filter(image__isnull=True)

        # Фильтрация по городу
        city_filter_form = CityFilterForm(request.GET)
        if city_filter_form.is_valid() and city_filter_form.cleaned_data['city']:
            city = city_filter_form.cleaned_data.get('city')
            posts = posts.filter(author__profile__city=city)


        # Сортировка
        if sort_by == 'date_new':
            posts = posts.order_by('-datetime')
        elif sort_by == 'date_old':
            posts = posts.order_by('datetime')
        elif sort_by == 'character_count_large':
            posts = posts.annotate(text_length=Length('text')).order_by('-text_length')
        elif sort_by == 'character_count':
            posts = posts.annotate(text_length=Length('text')).order_by('text_length')
        elif sort_by == 'likes':
            posts = posts.order_by('-likes')
        elif sort_by == 'comments':
            posts = posts.annotate(num_comments=Count('comments')).order_by('-num_comments')

        context = {
            'city_filter_form': city_filter_form,
            'posts': posts,
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
            pass

        return redirect(request.META.get('HTTP_REFERER', 'post_view'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get("text")
        comment = Comment.objects.create(post=post, author=request.user, text=text)
    return redirect(request.META.get('HTTP_REFERER', 'post_view'))

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    post_id = comment.post.id
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'post_view'))


@csrf_exempt
@login_required
@transaction.atomic
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        total_likes = post.likes.count()
        return JsonResponse({'liked': liked, 'total_likes': total_likes})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@method_decorator(login_required, name='dispatch')
class ProfileFollowingCreateView(View):
    """
    Создание подписки для пользователей
    """
    model = Profile

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, kwargs):
        user = get_object_or_404(Profile, pk=kwargs['pk'])
        profile = request.user.profile
        if profile in user.followers.all():
            user.followers.remove(profile)
            message = f'Подписаться на {user}'
            status = False
        else:
            user.followers.add(profile)
            message = f'Отписаться от {user}'
            status = True
        data = {
            'username': profile.user.username,
            'get_absolute_url': profile.get_absolute_url(),
            'slug': profile.slug,
            'avatar': profile.get_avatar,
            'message': message,
            'status': status,
        }
        return JsonResponse(data, status=200)


def post_list(request):
    # Получаем параметр сортировки из GET-запроса (по умолчанию сортируем по дате)
    sort_by = request.GET.get('sort_by', 'datetime')

    if sort_by == 'date':
        posts = Post.objects.all().order_by('-datetime')
    elif sort_by == 'character_count':
        posts = Post.objects.all().annotate(text_length=Length('text')).order_by('text_length')
    elif sort_by == 'image_first':
        posts_with_image = Post.objects.filter(image__isnull=False)
        posts_without_image = Post.objects.filter(image__isnull=True)
        posts = list(posts_with_image) + list(posts_without_image)
    elif sort_by == 'likes':
        posts = Post.objects.all().annotate(like_count=Count('likes')).order_by('-like_count')
    else:
        posts = Post.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'post_list.html', context)


def search_profiles(request):
    query = request.GET.get('q')
    if query:
        query_words = query.split()
        q_objects = Q()
        for word in query_words:
            q_objects |= Q(firstname__icontains=word) | Q(lastname__icontains=word)

        results = Profile.objects.filter(q_objects)
    else:
        results = Profile.objects.none()

    context = {
        'results': results,
    }
    return render(request, 'Search/search_profiles.html', context)

class SupportView(TemplateView):
    template_name = "Stuff/support.html"

class AboutUs(TemplateView):
    template_name = "Stuff/aboutus.html"

class Reviews(TemplateView):
    template_name = "Stuff/reviews.html"
    #Тут еще что-то будет

class SupportCreators(TemplateView):
    template_name = "Stuff/supportcreators.html"

class HomeView(TemplateView):
    template_name = "HomePage/home.html"


