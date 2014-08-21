
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.conf import settings


class EventForm(forms.Form):

    TYPES = (
        ('F', u'Formation'),
        ('C', u'Conference'),
        ('B', u'Bar'),
        ('J', u'Journee portes ouvertes'),
        ('A', u'AG'),
        ('O', u'Autre'), # other
    )

    IS_DRAFT = (
        ('1', u'Brouillon'),
        ('0', u'Publier immediatement'),
    )

    title = forms.CharField(
        label='Titre',
        widget=forms.TextInput(
            attrs={
                'autofocus': '',
                'placeholder': 'Titre'
            }
        )
    )
    place = forms.CharField(
        label='Lieu',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Lieu'
            }
        ),
        required=False
    )
    date_start = forms.DateTimeField(
        label='Date de debut',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Date de debut aaaa-mm-jj hh:mm'
            }
        )
    )

    image = forms.ImageField(
        required=False
    )

    type = forms.ChoiceField(
        label='Type de l\'evenement',
        widget=forms.RadioSelect,
        choices=TYPES,
        initial='O',
        required=False,
    )

    is_draft = forms.ChoiceField(
        label='Status de la publication',
        widget=forms.RadioSelect,
        choices=IS_DRAFT,
        initial='1',
        required=False,
    )

    text = forms.CharField(
        label='Texte',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Texte',
                'rows': '30'
            }
        )
    )


    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        img = cleaned_data.get('image')

        if img and img.size > settings.SIZE_MAX_IMG:
            msg = (u'Fichier trop lourd (%d Ko / %d Ko max). Pour ne pas saturer le serveur, merci de reduire la resolution de l\'image.') % (img.size/1024, settings.SIZE_MAX_IMG/1024)
            self._errors['image'] = self.error_class([msg])

            if 'image' in cleaned_data:
                del cleaned_data['image']

        return cleaned_data
