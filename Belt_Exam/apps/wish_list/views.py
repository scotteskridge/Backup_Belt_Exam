from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from . models import Item, User


# Create your views here.
def index(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:login")
    other_items = Item.objects.all().exclude(wished_by = request.session['user_id']) #well i need to exclude my items but running out of time
    my_items = Item.objects.filter(wished_by = request.session['user_id'])
    post = request.POST
    current_user = User.objects.get(id = request.session["user_id"])
    context = {
        "other_items" : other_items,
        "my_items" : my_items,
        "user" : current_user
    }

    return render(request, "wish_list/index.html", context)

def create_item(request):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:login")
    #this is just the page to fill out the form, confirm_create_item makes the item

    return render(request, "wish_list/create_item.html")

def confirm_create_item(request):
    ## you need to pass the postData and the user_id
    responce_from_model = Item.objects.create_item(request.POST, request.session["user_id"])
    if responce_from_model["status"]:
        messages.error(request, "You added an item")
        return redirect("wish_list:index")
    else:
        for error in responce_from_model["errors"]:
            messages.error(request, error)
        return redirect("wish_list:create_item")

    print("8"*80)
    print("did i make an item?")
    print (responce_from_model["item"])

    return redirect("wish_list:index")

def view_item(request, item_id):
    if not "user_id" in request.session:
        messages.error(request, "Must be logged in to continue")
        return redirect("login:login")
    current_user = User.objects.get(id = request.session["user_id"])
    current_item = Item.objects.get(id = item_id)
    wishers = User.objects.filter(users_wished_for__id = item_id)
    context = {
        "user" : current_user,
        "item" : current_item,
        "wishers" : wishers
    }


    return render(request, "wish_list/view_item.html", context)


def wish_for_item(request, item_id):
    responce_from_model = Item.objects.add_wish(item_id, request.session["user_id"])


    return redirect("wish_list:index")

def remove_wish(request, item_id):
    responce_from_model = Item.objects.remove_wish(item_id, request.session["user_id"])

    return redirect("wish_list:index")
