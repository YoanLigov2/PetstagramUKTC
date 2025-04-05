from django import forms

from Petstagram.photos.models import Photo


class PhotoCreateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Описание...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Локация...'}),
        }

        labels = {
            'photo': 'Снимка:',
            'description': 'Описание:',
            'location': 'Локация',
            'tagged_pets': 'Спомени:'
        }


class PhotoEditForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['photo', 'user']