from django.forms import ModelForm
from .models import *


class UploadProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'inventoryCount', 'image']
