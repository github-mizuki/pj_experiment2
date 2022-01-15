from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from .models import MainTask, SubTask, Log
from .forms import (
    LogCreateForm, MainTaskCreateForm, LogCreateForm2, LogUpdateForm, MainTaskUpdateForm,
    SubTaskCreateForm, SubTaskUpdateForm
)
from django.urls import reverse_lazy
from datetime import datetime
from django.utils.timezone import make_aware

from django.contrib import messages

# Create your views here.



class HomeView(LoginRequiredMixin, CreateView):
    template_name = os.path.join('task', 'task_home.html')
    form_class = LogCreateForm
    success_url = reverse_lazy('task:task_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = Log.objects.filter(user_id=self.request.user.id).order_by('-create_at')
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        return context
    
    def get_form_kwargs(self):
        kwargs = super(HomeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        messages.info(self.request, "ログを投稿しました。")
        return super(HomeView, self).form_valid(form)


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    template_name = os.path.join('task', 'log_list.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        context['logs'] = Log.objects.filter(user_id=self.request.user.id).order_by('-create_at')
        return context


class LogUpdateView(LoginRequiredMixin, UpdateView):
    template_name = os.path.join('task', 'log_update.html')
    model = Log
    form_class = LogUpdateForm
    success_url = reverse_lazy('task:log_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        return context

    def get_form_kwargs(self):
        kwargs = super(LogUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = post = form.save(commit=False)
        # form.instance.user_id = self.request.user.id
        print(post.maintask)
        if form.instance.maintask == None:
            form.instance.maintask == None
            messages.info(self.request, f"ログ:<{post.matter}>の所属タスクを{post.maintask}に変更しました。")
            return super(LogUpdateView, self).form_valid(form)
        messages.info(self.request, f"ログ:<{post.matter}>の所属タスクを{post.maintask.title}に変更しました。")
        return super(LogUpdateView, self).form_valid(form)


class MaintaskListView(LoginRequiredMixin, ListView):
    template_name = os.path.join('task', 'maintask_list.html')
    model = MainTask

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        return context

class MainTaskCreateView(LoginRequiredMixin, CreateView):
    template_name = os.path.join('task', 'maintask_create.html')
    model = MainTask
    form_class = MainTaskCreateForm
    success_url = reverse_lazy('task:maintask_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        return context

    def form_valid(self, form):
        self.object = post = form.save(commit=False)
        form.instance.user_id = self.request.user.id
        form.instance.create_at = datetime.now()
        messages.info(self.request, f"メインタスク:<{post.title}>を新規作成しました。")
        return super(MainTaskCreateView, self).form_valid(form)

class MainTaskDetailView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('task', 'maintask_detail.html')

    def get_context_data(self, pk, **kwargs):
        object = get_object_or_404(MainTask, pk=pk)
        aware_time = make_aware(datetime.now())
        countdown = object.deadline - aware_time
        form = LogCreateForm2
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        context['object'] = object
        context['subtaskset_complete_count'] = SubTask.objects.filter(maintask_id=object.id, complete=True).count()
        context['logs'] = Log.objects.filter(maintask_id=object.id).order_by('-create_at')
        context['subtasks'] = SubTask.objects.filter(maintask_id=object.id).order_by('-deadline')
        context['form'] = form
        if object.deadline >= aware_time:
            cd_day = int(round(countdown.total_seconds()/86400, 1))
            surplus = int(round(countdown.total_seconds()%86400, 1))
            cd_hour = int(round(surplus/3600, 1))
            surplus = int(round(surplus%3600, 1))
            cd_minutes = int(round(surplus/60, 1))
            if cd_day:
                context['countdown'] = f'残り {cd_day}日 と {cd_hour}時間{cd_minutes}分'
            elif cd_hour:
                context['countdown'] = f'残り {cd_hour}時間{cd_minutes}分'
            else:
                context['countdown'] = f'残り {cd_minutes}分'
        else:
            context['countdown'] = '期限切れ'
        print(object.subtask_set)
        return context

    def post(self, request, pk, *args, **kwargs):
        object = get_object_or_404(MainTask, pk=pk)
        form = LogCreateForm2(request.POST or None)
        if form.is_valid():
            form.instance.user_id = self.request.user.id
            form.instance.maintask_id = object.id
            form.instance.create_at = datetime.now()
            form.save()
            messages.info(self.request, "ログを投稿しました。")
            return redirect('task:maintask_detail', pk=object.id)

class MainTaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = os.path.join('task', 'maintask_update.html')
    model = MainTask
    form_class = MainTaskUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        return context

    def get_success_url(self):
        return reverse_lazy('task:maintask_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = post = form.save(commit=False)
        form.instance.update_at = datetime.now()
        messages.info(self.request, f"メインタスク:<{post.title}>を更新しました。")
        return super(MainTaskUpdateView, self).form_valid(form)


class SubtaskListView(LoginRequiredMixin, ListView):
    template_name = os.path.join('task', 'subtask_list.html')
    model = SubTask

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        context['subtasks'] = SubTask.objects.filter(maintask__user_id=self.request.user.id, maintask__archive=False, complete=False).order_by('deadline')

        return context

class SubTaskCreateView(LoginRequiredMixin, CreateView):
    template_name = os.path.join('task', 'subtask_create.html')
    model = SubTask
    form_class = SubTaskCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(MainTask, pk=self.kwargs['pk'])
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        return context

    def form_valid(self, form):
        self.object = post = form.save(commit=False)
        form.instance.maintask_id = self.kwargs['pk']
        form.instance.create_at = datetime.now()
        messages.info(self.request, f"サブタスク:<{post.title}>を新規作成しました。")
        return super(SubTaskCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('task:maintask_detail', kwargs={'pk': self.object.maintask_id})

class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = os.path.join('task', 'subtask_update.html')
    model = SubTask
    form_class = SubTaskUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        return context

    def form_valid(self, form):
        self.object = post = form.save(commit=False)
        form.instance.complete = self.request.POST['subtask_complete']
        form.instance.update_at = datetime.now()
        messages.info(self.request, f"サブタスク:<{post.title}>を更新しました。")
        return super(SubTaskUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task:maintask_detail', kwargs={'pk': self.object.maintask_id})


class ArchiveListView(LoginRequiredMixin, ListView):
    model = MainTask
    template_name = os.path.join('task', 'archive_list.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=False).order_by('deadline')
        context['archive_tasks'] = MainTask.objects.filter(user_id=self.request.user.id, archive=True).order_by('-archive_at')
        return context

def archive_view(request, pk):
    object = MainTask.objects.get(pk=pk)
    if object.archive:
        object.archive = False
        object.archive_at = None
        object.save()
        messages.info(request, f"<{object.title}>をメインタスクリストに戻しました。")
        return redirect('task:archive_list')
    else:
        object.archive = True
        object.archive_at = datetime.now()
        object.save()
        messages.info(request, f"<{object.title}>をアーカイブリストに移動しました。")
        return redirect('task:maintask_list')