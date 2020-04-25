from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone
from django.urls import reverse

from . import forms
from . import models


@login_required
def home(request):
    # get all listings by all users
    all_products = models.Product.objects.all().order_by('-time')
    context = {'all_products': all_products}

    # adding item to my cart
    if request.method == 'POST' \
            and 'addCartProductId' in request.POST \
            and 'addCardQuantity' in request.POST:

        addCart_productId = int(request.POST['addCartProductId'])
        addCart_quantity = int(request.POST['quantityToAddToCart'])

        product_toAddToCart = models.Product.objects.filter(id=addCart_productId)
        if not product_toAddToCart:  # product doesnt exits
            return HttpResponseNotFound('<h1>Page not found</h1>')

        product_toAddToCart = product_toAddToCart[0]
        stockCount = product_toAddToCart.inventoryCount
        context['addCartName'] = product_toAddToCart.name

        # check the amount user wants to add to cart is less than total stock
        if stockCount < addCart_quantity:
            context['stockFailure'] = True
            return render(request, 'post/home.html', context)

        context['addCardQuantity'] = addCart_quantity

        # create orederItem.
        item = models.OrderItem(
            quantity=addCart_quantity,
            product=product_toAddToCart
        )
        item.save()

        # add orderItem to Order (ie add to Cart)
        # first check if user has an Order associated to him
        order = models.Order.objects.filter(owner=request.user)
        if not order:
            # no association. first time adding to cart. create cart and add item
            order = models.Order.objects.create(owner=request.user)
            order.items.add(item)
        else:
            # add item
            order = order[0]
            order.items.add(item)

    return render(request, 'post/home.html', context)


@login_required
def uploadProduct(request):
    # list all products below
    context = {'all_products': models.Product.objects.all().order_by('-time')}

    # upload an item using forms. All fields are required
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
    # get cart of current user
    order = models.Order.objects.filter(owner=request.user)
    if not order:
        # means that user has never added to  cart
        return render(request, 'post/myCart.html', context)

    order = order[0]
    cart_items = order.get_cart_items()  # list of orderItems associated to Order
    context['cartItems'] = cart_items
    context['cartSum'] = order.get_cart_total()

    # scaling for STRIPE API
    context['paySum'] = order.get_cart_total() * 100

    # form for checkout/purchasing
    if request.method == 'POST' and 'shipAddress' in request.POST:
        addr = escape(request.POST['shipAddress'])
        context['shipAddressReturn'] = addr + 'change'

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
                    quantity=item.quantity,
                    address=addr
                )

                item.delete()  # delete from itemOrder table

        context['purchaseSuccessful'] = True

        # direct to paypal-like purchasing page
        return render(request, 'payments/confirmation.html', context)

    else:
        return render(request, 'post/myCart.html', context)


@login_required
def myListings(request):
    my_products = request.user.product_set.all().order_by('-time')
    context = {'my_products': my_products}

    if request.method == 'POST':
        # modify listing
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

        # delete listing
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
        return render(request, 'post/purchaseHistory.html', context)
    else:
        history = history.order_by('-time')
        context['history'] = history

    return render(request, 'post/purchaseHistory.html', context)

