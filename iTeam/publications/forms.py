#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-08-20 19:01:23
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-08-21 18:34:43

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.conf import settings


class PublicationForm(forms.Form):

    TYPES = (
        ('P', u'Autre (default)'), # default
        ('N', u'News'),
        ('T', u'Tutoriel'),
    )

    IS_DRAFT = (
        ('1', u'Brouillon'),
        ('0', u'Publier immédiatement'),
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
    subtitle = forms.CharField(
        label='Sous-titre (optionnel)',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Sous-titre (optionnel)'
            }
        ),
        required=False
    )

    image = forms.ImageField(
        required=False
    )

    type = forms.ChoiceField(
        label='Type de la publication',
        widget=forms.RadioSelect,
        choices=TYPES,
        initial='P',
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
        cleaned_data = super(PublicationForm, self).clean()
        img = cleaned_data.get('image')

        if img and img.size > settings.SIZE_MAX_IMG:
            msg = (u'Fichier trop lourd (%d Ko / %d Ko max). Pour ne pas saturer le serveur, merci de réduire la résolution de l\'image.') % (img.size/1024, settings.SIZE_MAX_IMG/1024)
            self._errors['image'] = self.error_class([msg])

            if 'image' in cleaned_data:
                del cleaned_data['image']

        return cleaned_data
