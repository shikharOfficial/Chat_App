from django.db import models
from django.core.validators import MinLengthValidator
from user.models import TblUser

class Chats(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(TblUser, on_delete=models.CASCADE, related_name='sent_chats')
    recipient = models.ForeignKey(TblUser, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField(validators=[MinLengthValidator(1)])
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        db_table = 'chat_tbl_chat'

    def __str__(self):
        return f'Chat from {self.sender} to {self.recipient} at {self.sent_at}'
