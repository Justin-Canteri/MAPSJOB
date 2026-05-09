from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#model for users
class users(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    is_active = models.BooleanField(db_column='is_active')
    created_at = models.DateField(auto_now_add=True)
    user_id = models.OneToOneField ('auth.User',
        db_column='user_id',  # ← le decís qué columna usar en la BD
        null=True,
        on_delete=models.DO_NOTHING,  # DO_NOTHING porque managed = False
        related_name='candidato'
    )
    apellido = models.CharField(max_length=40, db_column='apellido')
    phone = models.CharField(max_length=20, db_column='phone')
    fecha_nacimiento = models.DateField(max_length=20, db_column='fecha_nacimiento')
    direccion = models.TextField(max_length=40, db_column='direccion')
    curriculum = models.TextField(max_length=20, db_column='curriculum')

    class Meta:
        managed = False
        db_table = 'users'

#model for company
class company(models.Model):

    id = models.AutoField(primary_key=True, db_column='id')
    description = models.CharField(max_length=40, db_column='description')
    website = models.CharField(max_length=40, db_column='website')
    phone = models.IntegerField(db_column='phone')
    verified = models.BooleanField(db_column='verified')
    company_id = models.OneToOneField('auth.User',
        db_column='company_id',  # ← le decís qué columna usar en la BD
        null=True,
        on_delete=models.DO_NOTHING,  # DO_NOTHING porque managed = False
        related_name='empresa'
    )
    direccion = models.TextField(max_length=40, db_column='direccion')

    class Meta:
        managed = False
        db_table = 'company'


class jobpost(models.Model):

    id = models.AutoField(primary_key=True, db_column='id')
    company_id = models.ForeignKey(
        'company',
        db_column='company_id',  # ← le decís qué columna usar en la BD
        null=True,
        on_delete=models.DO_NOTHING,  # DO_NOTHING porque managed = False
        related_name='oferta_compania'
    )
    title = models.CharField(max_length=40, db_column='title')
    description = models.CharField(db_column='description')
    salary_range = models.CharField(max_length=40, db_column='salary_range')
    modality = models.CharField(max_length=40, db_column='modality')
    category = models.CharField(max_length=40, db_column='category')
    latitude = models.CharField(max_length=40, db_column='latitude')
    longitude = models.CharField(max_length=40, db_column='longitude')
    address = models.CharField(max_length=40, db_column='address')
    is_active = models.BooleanField(db_column='is_active')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'jobpost'