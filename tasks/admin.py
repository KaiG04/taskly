from django.contrib import admin
from django.db.models.aggregates import Count

from .models import Task, TaskBoard


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'slug', 'local_id', 'description', 'deadline', 'priority', 'created_by', 'created_at',
              'completed', 'task_board']
    readonly_fields = ['id', 'created_at', 'task_board', 'local_id']
    list_display = ['title', 'slug', 'created_by', 'task_board']
    list_filter = ['completed', 'created_at']
    list_select_related = ['task_board', 'created_by']
    ordering = ('-created_at',)
    search_fields = ['title', 'slug', 'created_by__username', 'task_board__title']
    autocomplete_fields = ['task_board', 'created_by']
    search_help_text = 'Searchable by title, slug, username and task board title.'

class TaskInLine(admin.StackedInline):
    model = Task
    classes = ['collapse']
    exclude = ['id', 'description', 'deadline', 'priority', 'created_by', 'created_at', 'completed']
    extra = 0
    readonly_fields = ['slug', 'local_id']

    def has_add_permission(self, request, obj):
        return False


@admin.register(TaskBoard)
class TaskBoardAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'slug', 'visibility', 'owner', 'created_at', 'last_updated']
    readonly_fields = ['id', 'created_at', 'last_updated']
    list_display = ['title', 'slug', 'visibility', 'owner', 'tasks_count']
    list_filter = ['created_at', 'last_updated']
    list_select_related = ['owner']
    search_fields = ['title', 'created_at']
    inlines = [TaskInLine]

    def tasks_count(self, obj):
        return obj.tasks.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(tasks_count=Count('tasks'))
        return qs
