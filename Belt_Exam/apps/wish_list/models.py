from __future__ import unicode_literals
from .. login.models import User #im port the user
from django.db import models

# Create your models here.
# should only need one model and one Manager
class ItemManager(models.Manager):
    def create_item(self, postData, user_id):
        reply_to_veiws = {}
        errors = []
        #some validations for length of name your inputs on this are going to be the logged in user or user_id from session and the postData of name
        if not len(postData["item_name"]):
            errors.append("Please enter item name")
        if self.filter(item_name = postData["item_name"].lower()):
            errors.append("Item already wished for")
        #if there are errors
        if not errors:
            #when creating a item I'll get the item_name from the post data but I need the user_id or user.id is that in session? the wished by is going to be the same, ok it is in seesion so I'm going to pass it from views
            #i think I need to find my user first
            user = User.objects.get(id = user_id)

            print (user.id)
            item = self.create(item_name = postData["item_name"].lower(), created_by=user)
            #item.wished_by.add(user)
            user.users_wished_for.add(item)
            reply_to_veiws["item"] = item
            reply_to_veiws["status"] = True
        else:
            reply_to_veiws["errors"] = errors
            reply_to_veiws["status"] = False

        #some create actions
        return reply_to_veiws
    def add_wish(self, item_id, user_id): #i don't think i need to pass this in up here but not sure
        reply_to_veiws = {}
        item = Item.objects.get(id = item_id)
        user = User.objects.get(id = user_id)
        item.wished_by.add(user)
        #adding a wish is just updating the many to many field

        return reply_to_veiws
    def remove_wish(self, item_id, user_id):
        reply_to_veiws = {}
        user = User.objects.get(id = user_id)
        item = Item.objects.get(id = item_id)

        item.wished_by.remove(user)
        #user.users_wished_for.remove(item)
        #break / update / .save the one to one relationship with user
        return reply_to_veiws



class Item(models.Model):
    item_name = models.CharField(max_length = 45)
    created_by = models.ForeignKey(User, related_name = 'users_created_by') #!!!!! this needs to be one to one relationship to user_id
    wished_by = models.ManyToManyField(User, related_name = 'users_wished_for')#!!!!! this needs to be many to many relationship with user_id
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ItemManager()
