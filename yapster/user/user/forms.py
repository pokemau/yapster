from django import forms
from .models import YapsterUser

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], widget=forms.RadioSelect)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = YapsterUser
        fields = ['first_name', 'last_name', 'email', 'birthdate', 'gender', 'bio']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            yapster_user, created = YapsterUser.objects.get_or_create(user=user)
            yapster_user.birthdate = self.cleaned_data['birthdate']
            yapster_user.gender = self.cleaned_data['gender']
            yapster_user.bio = self.cleaned_data['bio']
            yapster_user.save()

            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        return user