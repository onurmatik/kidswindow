from django.contrib import admin
from .models import Meeting, MeetingParticipant, MeetingPoll


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['game', 'is_public', 'host', 'time']
    list_editable = ['is_public']
    list_filter = ['game', 'time', 'is_public']
    search_fields = ['host__username', 'game__name']
    autocomplete_fields = ['game', 'host', 'participants']


@admin.register(MeetingParticipant)
class MeetingParticipantAdmin(admin.ModelAdmin):
    list_display = ['participant', 'meeting', 'meeting_time', 'tutor', 'joined']
    autocomplete_fields = ['meeting', 'participant']

    def meeting_time(self, obj):
        return obj.meeting.time
    meeting_time.admin_order_field = 'meeting__time'


@admin.register(MeetingPoll)
class MeetingFeedbackAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'user', 'rate', 'notes', 'time']
