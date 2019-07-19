from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TodoItem

# Create your views here.
def todoView(request):
	all_items = TodoItem.objects.all();
	return render(request, 'todo.html', {'all_items': all_items,})

def addTodo(request):
	new_item = TodoItem(content=request.POST['content'])
	new_item.save()
	checked_item = request.POST['chxn']
	if checked_item is not None:
		new_item2 = TodoItem(content=checked_item)
		new_item2.save()
	
	
	return HttpResponseRedirect('/todo/');

def deleteTodo(request, todo_id):
	item_to_delete = TodoItem.objects.get(id= todo_id);
	item_to_delete.delete()
	return HttpResponseRedirect('/todo/');


