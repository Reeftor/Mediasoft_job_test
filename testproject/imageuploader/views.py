from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView, RedirectView
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import ImageForm
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
                return redirect(reverse("profile"))
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)


class RegistrationView(TemplateView):
    template_name = "imageuploader/signup.html"

    def dispatch(self, request, *args, **kwargs):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                User.objects.create_user(username=username, password=password)
                return redirect(reverse("login"))

        return render(request, self.template_name)


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

        if not request.user.is_authenticated:
            return redirect(reverse("login"))

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


def user_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        return redirect(reverse("login"))


def delete_image(request, image_id):
    user = request.user
    uid = user.id

    if user.is_authenticated:
        Image.objects.get(id=image_id, user_id=uid).delete()
        return redirect(reverse("profile"))

    return redirect(reverse("login"))
