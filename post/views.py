from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone
from django.urls import reverse

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
def home(request):
    all_products = models.Product.objects.all().order_by('-time')
    context = {'all_products': all_products}

    if request.method == 'POST':
        addCart_productId = int(request.POST['addCartProductId'])
        product_toAddToCart = models.Product.objects.filter(id=addCart_productId)
        if not product_toAddToCart:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        product_toAddToCart = product_toAddToCart[0]
        stockCount = product_toAddToCart.inventoryCount

        context['addCartName'] = product_toAddToCart.name
        addCart_quantity = int(request.POST['quantityToAddToCart'])

        if stockCount < addCart_quantity:  # check the amount user wants to add to cart is less than total stock
            context['stockFailure'] = True
            return render(request, 'post/home.html', context)

        context['addCardQuantity'] = addCart_quantity

        # create orederItem
        item = models.OrderItem(
            quantity=addCart_quantity,
            product=product_toAddToCart
        )
        item.save()

        order = models.Order.objects.filter(owner=request.user)
        if not order:  # owner is empty create an order and associate to the user
            order = models.Order.objects.create(owner=request.user)
            order.items.add(item)
        else:
            order = order[0]
            order.items.add(item)

    return render(request, 'post/home.html', context)


@login_required
def uploadProduct(request):
    context = {'all_products': models.Product.objects.all().order_by('-time')}
    if request.method == 'POST':
        form = forms.UploadProductForm(request.POST, request.FILES)
        if form.is_valid():
           newProduct = form.save(commit=False)
           newProduct.owner = request.user
           newProduct.save()
        context['form'] = form
    return render(request, 'post/uploadProduct.html', context)


@login_required
def listAllMyCart(request):
    context = {}
    order = models.Order.objects.filter(owner=request.user)
    if not order:
        return HttpResponseNotFound('<h1>Please add to Cart first</h1>')
    order = order[0]
    cart_items = order.get_cart_items()
    context['cartItems'] = cart_items
    context['cartSum'] = order.get_cart_total()

    if request.method == 'POST':
        context['shipAddressReturn'] = escape(request.POST['shipAddress'] + 'change')
        # check if all items are in stock
        flag = False
        for item in cart_items:
            if item.quantity > item.product.inventoryCount:
                flag = True

        if flag:  # there was at least 1 item where the quantity in cart was > than stock
            context['stockNotEnough'] = True
            return render(request, 'post/myCart.html', context)
        else:  # all stock is safe. modify product database
            for item in cart_items:
                # modify inventory count of each product
                item.product.inventoryCount -= item.quantity
                item.product.save()

                # add to history of this user
                history = models.History.objects.create(
                    owner=request.user,
                    productName=item.product.name,
                    productDescription=item.product.description,
                    productPrice=item.product.price,
                    quantity=item.quantity
                )

                item.delete()  # delete from itemOrder table


        context['purchaseSuccessful'] = True
        return render(request, 'post/home.html', context)

    return render(request, 'post/myCart.html', context)


@login_required
def myListings(request):
    my_products = request.user.product_set.all().order_by('-time')
    context = {'my_products': my_products}

    if request.method == 'POST':
        if 'productID' in request.POST:
            pID = int(request.POST['productID'])
            productToModify = models.Product.objects.filter(id=pID)
            if not productToModify:
                return HttpResponseNotFound('<h1>Page not found</h1>')
            productToModify = productToModify[0]
            # modify
            productToModify.name = escape(request.POST['productName'])
            productToModify.description = escape(request.POST['productDescription'])
            productToModify.inventoryCount = int(request.POST['productStock'])
            productToModify.price = float(request.POST['productPrice'])
            productToModify.save()

            context['updateSuccess'] = True

        if 'productIDDelete' in request.POST:
            pID = int(request.POST['productIDDelete'])
            productToModify = models.Product.objects.filter(id=pID)
            if not productToModify:
                return HttpResponseNotFound('<h1>Page not found</h1>')

            productToModify = productToModify[0]
            productToModify.delete()

            context['deleteSuccess'] = True

    return render(request, 'post/myListings.html', context)


@login_required
def displayHistory(request):
    context = {}
    history = request.user.history_set.all()
    if not history:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    history = history.order_by('-time')
    context['history'] = history

    return render(request, 'post/purchaseHistory.html', context)


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