from django import forms
from .models import Reviews

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ["rating", "content"]
        widgets = {
            "rating": forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={"class": "form-select"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
        labels = {
            "rating": "Оцінка (від 1 до 5)",
            "content": "Текст відгуку",
        }