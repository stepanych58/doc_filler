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
	return HttpResponseRedirect('/todo/');
