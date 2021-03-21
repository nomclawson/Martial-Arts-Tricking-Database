from django.db import models

# Create your models here.


"""
TRICK table:
"""
class Trick(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    class_id = models.IntegerField()

"""
USERTRICKS table: 
    Contains the id of the user along with all of the ids of
    the tricks that user can perform / has saved.
"""
class UserTricks(models.Model):
    user_id = models.IntegerField()
    trick_id = models.IntegerField()

"""
USER table:
    No security on username or password, just a lookup 
"""
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

"""
Class table:
    Classification of tricks (variations, setups, beginner, etc.)
"""
class Class(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()