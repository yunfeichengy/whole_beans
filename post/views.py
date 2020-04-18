from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone

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
    all_products = models.Product.objects.all().order_by('time')
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


@login_required
def myProduct(request):
    my_products = request.user.product_set.all()
    context = {'my_products': my_products}
    return render(request, 'post/myProduct.html', context)


# @login_required
# def modifyListing(request, idToModify):
#     productToModify = models.Product.objects.filter(id=idToModify)
#     if not productToModify:
#         return HttpResponseNotFound('<h1>Page not found</h1>')
#     productToModify = productToModify[0]
#
#     if request.method == 'POST':
#         if 'product' in request.POST:
#             product = models.Product.objects.filter(
#                 id = int(request.POST['product'])
#             )[0]
#             # make changes


# add a dorm in the MYlisting page that allows modification.