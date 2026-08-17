from django import forms
from .models import Product
from django.contrib.auth.models import User
from .models import Customer
from .models import Review

class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = "__all__"

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')

        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = [

            'phone',

            'address',

            'city',

            'state',

            'pincode'

        ]

class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [

            "rating",

            "comment"

        ]