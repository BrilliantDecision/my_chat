from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class ChatParticipant(models.Model):
    """Участник чата"""
    user = models.OneToOneField(get_user_model(), related_name='group_user', on_delete=models.CASCADE, null=True)
    status = models.TextField("Статус", max_length=100, default='')
    birthday = models.DateField('День рождения', null=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Additional information of user'
        verbose_name_plural = 'Additional information of user'

    #  Какой пользователь имеет больший id (в базе id первого пользователя меньше id второго)
    @staticmethod
    def _greatest(user_one, user_two):
        if user_two > user_one:
            return user_one, user_two
        elif user_two < user_one:
            return user_two, user_one

    # Получаем список друзей пользователя
    @staticmethod
    def get_friends_list(our_user_id):
        return FriendshipRelations.objects.filter(
            models.Q(user_friend_one=our_user_id) | models.Q(user_friend_two=our_user_id)
        )

    # Получаем отправленные пользователем запросы в друзья, которые еще не приняты
    @staticmethod
    def get_sent_friend_requests(our_user_id):
        return FriendshipRelations.objects.filter(
            models.Q(status=0) & models.Q(user_action=our_user_id)
        )

    # Получаем все отправленные нам запросы в друзья
    @staticmethod
    def get_friend_requests(our_user_id):
        return FriendshipRelations.objects.filter(
            (models.Q(user_friend_one=our_user_id) | models.Q(user_friend_two=our_user_id)) &
            models.Q(status=0)
        ).exclude(user_action=our_user_id)

    # Получаем заблокированных нами пользователей
    @staticmethod
    def get_blocked_friends(our_user_id):
        return FriendshipRelations.objects.filter(
            (models.Q(user_friend_one=our_user_id) | models.Q(user_friend_two=our_user_id)) &
            models.Q(status=3) & models.Q(user_action=our_user_id)
        )

    # Создаем запрос в друзья
    @staticmethod
    def add_friend_request(our_user_id, to_user):
        user_one, user_two = ChatParticipant._greatest(our_user_id, to_user)
        FriendshipRelations.objects.create(user_friend_one=user_one, user_friend_two=user_two,
                                           status=0, user_action=our_user_id)

    # Принимаем запрос в друзья
    @staticmethod
    def accept_friend_request(our_user_id, to_user):
        user_one, user_two = ChatParticipant._greatest(our_user_id, to_user)
        obj = FriendshipRelations.objects.get(
            user_friend_one=user_one, user_friend_two=user_two
        )
        obj.status = 1
        obj.user_action = our_user_id
        obj.save()

    # Откланяем запрос в друзья
    @staticmethod
    def decline_friend_request(our_user_id, to_user):
        user_one, user_two = ChatParticipant._greatest(our_user_id, to_user)
        obj = FriendshipRelations.objects.get(
            user_friend_one=user_one, user_friend_two=user_two
        )
        obj.status = 2
        obj.user_action = our_user_id
        obj.save()

    # Закрываем наш запрос в друзья
    @staticmethod
    def cancel_friend_request(our_user_id, to_user):
        user_one, user_two = ChatParticipant._greatest(our_user_id, to_user)
        FriendshipRelations.objects.get(
            user_friend_one=user_one, user_friend_two=user_two,
            status=0, user_action=our_user_id
        ).delete()

    # Удалить из друзей
    @staticmethod
    def unfriend(our_user_id, to_user):
        user_one, user_two = ChatParticipant._greatest(our_user_id, to_user)
        FriendshipRelations.objects.get(
            user_friend_one=user_one, user_friend_two=user_two,
            status=1, user_action=our_user_id
        ).delete()

    # Блокируем пользователя
    @staticmethod
    def block_user(our_user_id, to_user):
        user_one, user_two = ChatParticipant._greatest(our_user_id, to_user)
        FriendshipRelations.objects.update_or_create(
            user_friend_one=user_one,
            user_friend_two=user_two,
            defaults={'status': 3, 'user_action': our_user_id},
        )

    # Разблокируем пользователя
    @staticmethod
    def unblock_user(our_user_id, to_user):
        user_one, user_two = ChatParticipant._greatest(our_user_id, to_user)
        FriendshipRelations.objects.get(
            user_friend_one=user_one,
            user_friend_two=user_two,
            status=3,
            user_action=our_user_id
        ).delete()

    # Получаем список наших чатов
    @staticmethod
    def get_chats_list(our_user_id):
        return ChatUsers.objects.filter(user=our_user_id)


class FriendshipRelations(models.Model):
    """Друзья пользователя"""
    user_friend_one = models.ForeignKey(get_user_model(), related_name='user_one_friend',
                                        on_delete=models.CASCADE, null=True)
    user_friend_two = models.ForeignKey(get_user_model(), related_name='user_two_friend',
                                        on_delete=models.CASCADE, null=True)
    "0 - запрос на рассмотрении, 1 - запрос принят(друзья), 2 - запрос отклонен, 3 - пользователь заблокирован"
    status = models.IntegerField("Статус отношений", default=0)
    user_action = models.ForeignKey(get_user_model(), related_name='user_action',
                                    on_delete=models.CASCADE, null=True)
    seen = models.BooleanField("Просмотрено", default=False)

    def __str__(self):
        return f'Relations between {self.user_friend_one} and {self.user_friend_two}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_friend_one', 'user_friend_two'],
                name='unique_constraint_friends'
            ),
            models.CheckConstraint(
                check=models.Q(user_friend_two__gt=models.F("user_friend_one")),
                name='user_friend_one > user_friend_two'
            )]


class Chat(models.Model):
    """Чат"""
    name = models.CharField("Название чата", max_length=100)
    admin = models.ForeignKey(get_user_model(), related_name='chat_admin', on_delete=models.CASCADE, null=True)
    create_date = models.DateField("Дата создания", null=True)
    private = models.BooleanField('Приватный чат', default=True)

    def __str__(self):
        return f'Chat {self.name}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    # Получение списка сообщений чата
    def get_messages_sorted_by_date_list(self):
        return Messages.objects.filter(chat=self.id).order_by('date')

    # Получаем список всех пользователей чата
    def get_chat_users_list(self):
        return ChatUsers.objects.filter(chat=self.id)


class ChatUsers(models.Model):
    """Пользователи чата"""
    user = models.ForeignKey(get_user_model(), related_name="chat_user", on_delete=models.CASCADE, null=True)
    chat = models.ForeignKey(Chat, related_name="chat", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Пользователи чатов'
        verbose_name_plural = 'Пользователи чатов'

        models.UniqueConstraint(
            fields=['user', 'chat'],
            name='unique_chat_users'
        )


class Messages(models.Model):
    """Сообщения"""
    user = models.ForeignKey(get_user_model(), related_name="chat_user", on_delete=models.CASCADE, null=True)
    chat = models.ForeignKey(Chat, related_name="chat", on_delete=models.CASCADE, null=True)
    text = models.TextField("Сообщение", max_length=500)
    date = models.DateTimeField("Дата отправки", null=True)

    def __str__(self):
        return f'Message of user {self.user} from chat {self.chat}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
