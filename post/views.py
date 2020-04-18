from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import forms
from . import models

@login_required
def post(request):
    # if GET request, construct this context and return it at end. all the posts that belong to a user
    context = {'posts': request.user.post_set.all()}

    if request.method == 'POST':
        form = forms.PostForm(request.POST)  # instantiate post object
        if form.is_valid():
            new_post = form.save(commit=False)  # create a  model instance. commit=False means I'll save it later
            new_post.owner = request.user
            new_post.save()
        context['form'] = form
    return render(request, 'post/post.html', context)



@login_required
def listAllProduct(request):
    all_products = models.Product.objects.all()
    context = {'all_products': all_products}
    return render(request, 'post/listAllProduct.html', context)


@login_required
def uploadProduct(request):
    context = {'all_products': models.Product.objects.all()}
    if request.method == 'POST':
        form = forms.UploadProductForm(request.POST)
        if form.is_valid():
           newProduct = form.save(commit=False)
           newProduct.owner = request.user
           newProduct.save()
        context['form'] = form
    return render(request, 'post/uploadProduct.html', context)

