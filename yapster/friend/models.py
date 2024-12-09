from django.db import models
from user.models import YapsterUser

class FriendList(models.Model):
    user = models.OneToOneField(YapsterUser, on_delete=models.CASCADE, related_name='friendlist_user')
    friends = models.ManyToManyField(YapsterUser, blank=True, related_name='friends')

    def __str__(self):
        return self.user.user.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self, target_account):
        remover_friends_list = self
        remover_friends_list.remove_friend(target_account)
        friends_list = FriendList.objects.get_or_create(user=target_account)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        return friend in self.friends.all()

class FriendRequest(models.Model):
    sender = models.ForeignKey(YapsterUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(YapsterUser, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.user.username

    def accept(self):
        receiver_friend_list = FriendList.objects.get_or_create(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()


class BlockList(models.Model):
    user = models.OneToOneField(YapsterUser, on_delete=models.CASCADE, related_name='blocklist_user')
    blocked_users = models.ManyToManyField(YapsterUser, blank=True, related_name='blocked_users')

    def __str__(self):
        return self.user.user.username

    def add_to_block_list(self, account):
        if not account in self.blocked_users.all():
            self.blocked_users.add(account)
            self.save()

    def remove_from_block_list(self, account):
        if account in self.blocked_users.all():
            self.blocked_users.remove(account)
            self.save()
