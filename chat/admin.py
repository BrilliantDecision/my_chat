from django.contrib import admin
from .models import ChatParticipant, Chat, ChatUsers, Messages, FriendshipRelations


@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'birthday')
    list_display_links = ('user', )


@admin.register(FriendshipRelations)
class FriendshipRelationsAdmin(admin.ModelAdmin):
    list_display = ('user_friend_one', 'user_friend_two', 'status', 'user_action', 'seen')
    list_display_links = ('user_friend_one', 'user_friend_two')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date')
    list_display_links = ('name',)


@admin.register(ChatUsers)
class ChatUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat')
    list_display_links = ('user', 'chat')


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat', 'date')
    list_display_links = ('user', 'chat')
