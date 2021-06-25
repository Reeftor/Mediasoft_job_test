from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ('title', 'image')


class ImageEditForm(forms.ModelForm):
    image = forms.FileField()

    class Meta:
        model = Image
        fields = ('title', 'image')
