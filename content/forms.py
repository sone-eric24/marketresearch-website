from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Hidden "honeypot" field: people never see it, spam robots fill it in.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off"}))

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel"}),
            "message": forms.Textarea(attrs={"rows": 6, "aria-describedby": "id_message-hint"}),
        }
        labels = {
            "name": "Your name",
            "email": "Email address",
            "phone": "Phone or WhatsApp (optional)",
            "subject": "What is it about?",
            "message": "How can we help?",
        }
        help_texts = {
            "message": "A few lines about your project, your goals and your timeline are enough.",
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""
