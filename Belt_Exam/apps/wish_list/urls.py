from django.conf.urls import url, include

from . import views

urlpatterns = [

    url(r'^$', views.index, name = "index"),

    url(r'^create_item$', views.create_item, name = "create_item"),
    url(r'^view_item/(?P<item_id>\d+)$', views.view_item, name = "view_item"),
    url(r'^confirm_create_item$', views.confirm_create_item, name = "confirm_create_item"),
    url(r'^wish_for_item/(?P<item_id>\d+)$', views.wish_for_item, name = "wish_for_item"),
    url(r'^remove_wish/(?P<item_id>\d+)$', views.remove_wish, name = "remove_wish")

]


#not sure how to use this yet (?P<item_id>\d+)
#{% url 'wish_list:remove_wish' item_id=1 %}
