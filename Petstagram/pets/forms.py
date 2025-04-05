from django import forms

from Petstagram.pets.models import Pet


class PetForm(forms.ModelForm):
    personal_photo = forms.ImageField(
        label="Снимка:",
        widget=forms.FileInput,
        required=False
    )
    class Meta:
        model = Pet
        fields = '__all__'
        exclude = ['user', 'slug']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Име на животното...'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'animal_type': forms.TextInput(attrs={'placeholder': 'Вид...'}),
            'specie': forms.TextInput(attrs={'placeholder': 'Порода...'}),
            'color': forms.TextInput(attrs={'placeholder': 'Цвят...'}),
            'distinguishing_marks': forms.TextInput(attrs={'placeholder': 'Отличителни белези...'}),
        }

        labels = {
            'name': 'Име',
            'date_of_birth': 'Роден на',
            'animal_type': 'Вид',
            'specie': 'Порода',
            'color': 'Цвят',
            'distinguishing_marks': 'Белези',
        }


class PetDeleteForm(PetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'