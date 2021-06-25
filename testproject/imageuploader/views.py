from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView, RedirectView
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from .forms import ImageForm, ImageEditForm
from .models import Image


class LoginView(TemplateView):
    template_name = "imageuploader/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.user = user
                uid = user.id
                u = User.objects.get(id=uid)
                if u.is_superuser:
                    return redirect(reverse("adminprofile"))
                else:
                    return redirect(reverse("profile"))
            else:
                try:
                    user_is_active = User.objects.get(username=username).is_active
                except Exception:
                    context['error'] = "Incorrect username or password"
                    return render(request, self.template_name, context)
                if not user_is_active:
                    context['error'] = "Your account is blocked"
                    return render(request, self.template_name, context)

                return render(request, self.template_name, context)

        return render(request, self.template_name, context)


class RegistrationView(TemplateView):
    template_name = "imageuploader/signup.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.user.is_superuser:
            admin_password = request.user.password
            context['superuser'] = request.user.is_superuser

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if request.user.is_superuser:
                keyword = request.POST.get('keyword')

            if password == password2:
                try:
                    db_user = str(User.objects.get(username=username))
                except Exception:
                    db_user = hash(username)

                if username == db_user:
                    context['error'] = "User already exists!"
                    return render(request, self.template_name, context)
                else:
                    if request.user.is_superuser:
                        if check_password(keyword, admin_password):
                            User.objects.create_superuser(username=username, password=password)
                            return redirect(reverse("adminprofile"))
                    User.objects.create_user(username=username, password=password)
                    return redirect(reverse("login"))

        return render(request, self.template_name, context)


class ProfileView(TemplateView):
    template_name = "imageuploader/profile.html"

    def dispatch(self, request, *args, **kwargs):

        context = {}
        username = request.user.username
        uid = request.user.id
        user_images = Image.objects.filter(user_id=uid).order_by('-id')
        context['uid'] = uid
        context['username'] = username
        context['user_images'] = user_images

        try:
            u = User.objects.get(id=uid)
            if u.is_superuser:
                return redirect(reverse("adminprofile"))
        except Exception:
            if not request.user.is_authenticated:
                return redirect(reverse("login"))
            return redirect(reverse("profile"))

        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                context['form'] = form

                for file in request.FILES.getlist('image'):
                    instance = Image(
                        user=User.objects.get(id=uid),
                        image=file,
                        title=str(form.instance)
                    )
                    instance.save()
                return render(request, self.template_name, context)
        else:
            form = ImageForm()
            context['form'] = form

        return render(request, self.template_name, context)


class ImageClickCounterRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        image = get_object_or_404(Image, pk=pk)
        image.update_views(pk)
        return image.image_url


class AdminProfileView(TemplateView):
    template_name = "imageuploader/adminprofile.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        uid = request.user.id
        username = request.user.username
        context['uid'] = uid
        context['username'] = username

        try:
            u = User.objects.get(id=uid)
            if not u.is_superuser:
                return redirect(reverse("profile"))
        except Exception:
            return redirect(reverse("profile"))

        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        all_users = User.objects.all().filter(is_superuser=False)

        context['all_users'] = all_users

        return render(request, self.template_name, context)


class UserpageAdminView(TemplateView):
    template_name = "imageuploader/userpageadmin.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        pk = kwargs['pk']
        user = User.objects.get(id=pk)
        context['user'] = user
        user_images = Image.objects.filter(user_id=pk).order_by('-id')
        context['user_images'] = user_images

        return render(request, self.template_name, context)


class AdminPostEditView(TemplateView):
    template_name = "imageuploader/admineditpost.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        image_id = kwargs['image_id']
        context['image_id'] = image_id
        context['image'] = Image.objects.get(id=image_id)
        if request.method == 'POST':
            form = ImageEditForm(request.POST, request.FILES)
            if form.is_valid():
                context['form'] = form

                image = Image.objects.get(id=image_id)
                context['image'] = image
                image.image = request.FILES.get('image')
                image.title = str(form.instance)
                image.view_count = 0
                image.save()

                return render(request, self.template_name, context)
        else:
            form = ImageForm()
            context['form'] = form

        return render(request, self.template_name, context)


def user_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        return redirect(reverse("login"))


def redirect_ref(request):
    user = request.user
    if user.is_superuser:
        return redirect(reverse("adminprofile"))
    else:
        return redirect(reverse("profile"))


def delete_user(request, user_id):
    user = request.user
    if user.is_superuser:
        User.objects.get(id=user_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def block_user(request, user_id):
    user = request.user
    u = User.objects.get(id=user_id)
    if user.is_superuser:
        if u.is_active:
            u.is_active = False
            u.save()
        else:
            u.is_active = True
            u.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_image(request, image_id):
    user = request.user
    uid = user.id

    if user.is_authenticated:
        try:
            if user.is_superuser:
                Image.objects.get(id=image_id).delete()
            else:
                Image.objects.get(id=image_id, user_id=uid).delete()
        except Exception:
            ...

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(reverse("login"))
