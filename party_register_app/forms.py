from django import forms
from .models import Guest


class RegistrationForm(forms.ModelForm):
    """
    A form for registering a new guest, based directly on the Guest model.
    """
    will_attend = forms.BooleanField(
        required=True,
        label="Will you come to the party? (You must select Yes to register)",
        initial=True
    )

    class Meta:
        # 1. Connect the form to our Guest model
        model = Guest
        fields = ['name', 'phone_number', 'will_attend']
        labels = {
            'name': 'Your Full Name',
            'phone_number': 'Your Phone Number (e.g., 555-123-4567)',
        }
        help_texts = {
            'phone_number': 'We will only use this for important event updates.',
        }
