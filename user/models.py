from django.db import models
from django.core.validators import RegexValidator


class TblUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=20, validators=[RegexValidator(
        regex='^[A-Za-z]{2,20}$',
        message="Invalid First Name",
        code="invalid_first_name"
    )])
    last_name = models.CharField(max_length=20, validators=[RegexValidator(
        regex='^[A-Za-z\-]{2,20}$',
        message='Invalid Last Name',
        code='invalid_last_name'
    )])
    email = models.EmailField(unique=True, max_length=30, error_messages={ 'unique': "Email already exists."})
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'chat_tbl_user'
