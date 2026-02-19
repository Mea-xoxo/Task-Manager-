from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.urls import reverse_lazy
from django.contrib import messages


#list tasks of logged-in User
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    login_url = '/login'

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)


#Assign current user when creating a task
class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title","completed"]
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')


    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#only allow users to update their tasks
class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','completed']
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)
    
    def form_valid(self,form):
        messages.success(self.request, "Task updated successfully")
        return super().form_valid(form)

#only allow users to delete their tasks
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")

    def get_queryset(self):
        return Task.objects.filter(user = self.request.user)

    def delete(self,request, *args, **kwargs):
        messages.success(self.request, "Task deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Create your views here.


