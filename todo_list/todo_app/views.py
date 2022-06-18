# todo_list/todo_app/views.py
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
                                    
from .models import ToDoList, ToDoItem

class ListListView(ListView):    #ListListView class will display a list of the to-do list titles. so you only need to tell it ` the data-model class that you want to fetch and the name pf the template that'll format the list into a displayable form 
    model = ToDoList
    template_name = "todo_app/index.html"

class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

# in your Itemlistview implementation, your specializing ListView a little bit. when you show a list of ToDoItem objects, you dont want to show every ToDoItem in the database
# just those that beling to the current list. todo this lines 16 and 17 override the listview.get_queryset() method by using the models object.filiter() method to restrice the data returned    

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context
# Lines 30 to 37 define ListCreate. This class defines a form containing the sole public ToDoList attribute, its title. The form itself also has a title, which is passed in the context data.        

class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])
#Lines 40 to 63 define the ItemCreate class. This generates a form with four fields. The .get_initial() and .get_context_data() methods are overridden to provide useful information to the template.
# The .get_success_url() method provides the view with a page to display after the new item has been created. In this case, it calls the list view after a successful form submit to display the full 
# to-do list containing the new item.        

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])
# Lines 68 to 84 define ItemUpdate, which is very similar to ItemCreate but supplies a more appropriate title.        

class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context