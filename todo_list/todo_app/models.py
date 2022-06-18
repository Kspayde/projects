# todo_list_app/models.py

from django.utils import timezone

from django.db import models
from django.urls import reverse

def one_week_hence():
    return timezone.now() + timezone.timedelta(days =7)   # used for setting todoitel default due dates

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self): # 14-15 and 27-30 .get_absolute_url() method is implemented... a django convention for data models. it returns the url for the particular data item. allows you to reference the url conventiently and robustly in code the return statement of both implementations of .get_absolute_url() uses reverse() to avoid hard-codig the url and its parameters.
        return reverse("list", args=[self.id])   #lines 12 - 21 declare title fields that are each limited to 100 characters, cammot have two toDolist with the same title

    def __str__(self): #17-18 32-33 declaires __str__() methods for each model class. startd way of creating readable representation of an object, not necessary to write but can help with debugging 
        return self.title

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)   # lines 23-24 provide useful defaults for their date fields django will automatically set .created_date to the current date and first time a todoitem object is saved while                      
    due_date = models.DateTimeField(default=one_week_hence)  # .due_date uses one_week_hence() to set a default due date one week in the future of course, the app will allow the user to change the due date if this default value doesn't suit them
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)  #line 25 declares ToDoItem.todo_List, so each ToDoItem must have exactly one ToDoList in which it belongs. In the DB its one-too-many relationship. The on_delete keyword is the same line ensures that if a todo is deleted than all items associated to-do items will be deleted also 

    def get_absolute_url(self):   # 14-15 and 26-29 .get_absolute_url() method is implemented... a django convention for data models. it returns the url for the particular data item. allows you to reference the url conventiently and robustly in code the return statement of both implementations of .get_absolute_url() uses reverse() to avoid hard-codig the url and its parameters.
        return reverse(
             "item-update", args=[str(self.todo_list.id), str(self.id)]
        )        

    def __str__(self): #17-18 32-33 declaires __str__() methods for each model class. startd way of creating readable representation of an object, not necessary to write but can help with debugging
        return f"{self.title}: due {self.due_date}"

    class Meta:  # defines the nested meta class, which allows you to get some useful options. here your using it to set a default odering for ToDoItem records. 
        ordering = ["due_date"]    #lines 11 -36 are extended djangos django.db.models.model superclass we just need to define the data fields in each model
# model superclass defines an id field which is automatically unique for each object and serves as its identifier. 
#djando.db.models submodile also has classes for all the field types we might need to define and allows us to set up useful default behavior.    