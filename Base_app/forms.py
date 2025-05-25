from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User  


from .models import BookTable,Feedback

class BookTableForm(ModelForm):
    class Meta:
        model = BookTable
        fields = "__all__"

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ("__all__")

    def clean_Rating(self):
        rating = self.cleaned_data.get("Rating")
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
class SignupForm(ModelForm):
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
       
        