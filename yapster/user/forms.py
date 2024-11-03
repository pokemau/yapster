from django import forms
from django.contrib.auth import get_user_model
from .models import YapsterUser

User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    postcode = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=100, required=False)
    birthdate = forms.DateField(required=False)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_image = forms.ImageField(required=False)
    cover_photo = forms.ImageField(required=False)

    class Meta:
        model = YapsterUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'postcode', 'country',
                  'birthdate', 'gender', 'profile_image', 'cover_photo', 'bio']

    def save(self, commit=True):
        yapster_user = super().save(commit=False)

        user = yapster_user.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
       # yapster_user.email = self.cleaned_data['email']
        yapster_user.bio = self.cleaned_data['bio']
        if commit:
            user.save()
            yapster_user.save()
        return yapster_user
