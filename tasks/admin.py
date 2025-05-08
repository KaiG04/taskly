from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.text import slugify

from .models import Task, TaskBoard


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'slug', 'local_id', 'description', 'deadline', 'priority', 'created_by', 'created_at',
              'task_board', 'completed', 'reminder_notification']
    readonly_fields = ['id', 'slug', 'created_at', 'created_by', 'task_board', 'local_id']
    list_display = ['title', 'slug', 'created_by', 'task_board']
    list_filter = ['completed', 'created_at']
    list_select_related = ['task_board', 'created_by']
    ordering = ('-created_at',)
    search_fields = ['title', 'slug', 'created_by__username', 'task_board__title']
    autocomplete_fields = ['task_board', 'created_by']
    search_help_text = 'Searchable by title, slug, username and task board title.'


class TaskInLine(admin.TabularInline):
    model = Task
    classes = ['collapse']
    fields = ['title', 'local_id', 'deadline', 'priority', 'created_by',
              'completed', 'reminder_notification']
    extra = 0
    readonly_fields = ['id', 'slug', 'created_at', 'created_by', 'local_id']
    show_change_link = True




@admin.register(TaskBoard)
class TaskBoardAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'slug', 'visibility', 'owner', 'created_at', 'last_updated', 'tasks_count', 'guests']
    readonly_fields = ['id', 'slug', 'owner', 'created_at', 'last_updated', 'tasks_count']
    list_display = ['title', 'slug', 'visibility', 'owner', 'tasks_count']
    list_filter = ['created_at', 'last_updated']
    list_select_related = ['owner']
    search_fields = ['title', 'created_at']
    autocomplete_fields = ['owner']
    inlines = [TaskInLine]

    def tasks_count(self, obj):
        return obj.tasks.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('tasks').annotate(tasks_count=Count('tasks'))
        return qs
