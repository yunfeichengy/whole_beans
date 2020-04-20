from django.forms import ModelForm
from .models import *


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # only title and content should be entered by user

class UploadProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'inventoryCount']
