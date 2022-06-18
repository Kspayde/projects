# todo_list/todo_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("",
        views.ListListView.as_view(), name="index"),
    # line 6 tells django that if the rest of the url is empty, your listlistview class should be called to handle the request. Notice that the name="index" parameter matches the 
    # target of the {% url "index" %} macro that we saw in line 18 of the base.html template

    path("list/<int:list_id>/",
        views.ItemListView.as_view(), name="list"),
    #Line 10 declares a placeholder as the new route’s first parameter. This placeholder will match a positional parameter in the URL path that the browser returns. The syntax list/<int:list_id>/ 
    # means that this entry will match a URL like list/3/ and pass the named parameter list_id = 3 to the ItemListView instance. If you revisit the ItemListView code in views.py, you’ll notice that 
    # it references this parameter in the form self.kwargs["list_id"].

     # CRUD patterns for ToDoLists
    path("list/add/", views.ListCreate.as_view(), name="list-add"),
    path(
        "list/<int:pk>/delete/", views.ListDelete.as_view(), name="list-delete"
    ),
    # CRUD patterns for ToDoItems
    path(
        "list/<int:list_id>/item/add/",
        views.ItemCreate.as_view(),
        name="item-add",
    ),
    path(
        "list/<int:list_id>/item/<int:pk>/",
        views.ItemUpdate.as_view(),
        name="item-update",
    ),
    path(
        "list/<int:list_id>/item/<int:pk>/delete/",
        views.ItemDelete.as_view(),
        name="item-delete",
    ),
]