from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin
from .models import NewsletterSubscriber

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


admin.site.register(Comment)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_subscribed')
    search_fields = ('email',)
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=subscribers.csv'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Date Subscribed'])

        for subscriber in queryset:
            writer.writerow([subscriber.name, subscriber.email, subscriber.date_subscribed])

        return response

    export_as_csv.short_description = "Export Selected to CSV"
