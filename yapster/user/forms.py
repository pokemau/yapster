from django import forms
from django.contrib.auth.models import User
from .models import YapsterUser

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = YapsterUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'postcode', 'country', 'bio', 'profile_image']


    def save(self, commit=True):
        yapster_user = super(ProfileForm, self).save(commit=False)
        user = yapster_user.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if 'profile_image' in self.files:
            yapster_user.profile_image = self.files['profile_image']
        if commit:
            user.save()
            yapster_user.save()
        return yapster_user


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['profile_image'].initial = self.instance.profile_image


