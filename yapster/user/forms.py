from django import forms
from .models import YapsterUser, User

class UpdateUserForm(forms.ModelForm):
    birthdate = forms.DateField(required=False)
    gender = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birthdate', 'gender']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            yapster_user, created = YapsterUser.objects.get_or_create(user=user)
            yapster_user.birthdate = self.cleaned_data['birthdate']
            yapster_user.gender = self.cleaned_data['gender']
            yapster_user.save()
        return user