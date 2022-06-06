import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class GuessInfo(models.Model):
    Name = models.CharField(max_length=50, default='')
    Sex = models.CharField(max_length=50, default='Khác')
    DateOfBirth = models.DateField(default=datetime.date.today)
    PhoneNumber = models.CharField(max_length=10, default='')
    Mail = models.EmailField(default='')
    Type = models.CharField(default='Normal', max_length=50)
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    Photo = models.ImageField(null=True, blank=True)


class CinemaInfo(models.Model):
    Address = models.CharField(default='', max_length=50)
    PhoneNumber = models.CharField(max_length=10, default='')
    Mail = models.EmailField(default='')


class FilmData(models.Model):
    Name = models.CharField(default='', max_length=50)
    Type = models.CharField(default='', max_length=50)
    Times = models.IntegerField(default=90)
    Actor = models.CharField(default='', max_length=500)
    Author = models.CharField(default='', max_length=50)
    Premiere = models.DateField(default='')
    Language = models.CharField(default='', max_length=100)
    Rated = models.CharField(default='', max_length=100)
    Photo = models.ImageField(null=True, upload_to="images/")
    Background = models.ImageField(null=True, upload_to="images/")


class Room(models.Model):
    Name = models.CharField(default='', max_length=50)
    Type = models.CharField(default='', max_length=50)
    CinemaInfo = models.ForeignKey(CinemaInfo, on_delete=models.CASCADE, default='')


class TimeDef(models.Model):
    Start = models.TimeField(primary_key=True)


# Suất chiếu:
class ShowTimes(models.Model):
    TimeDef_Start = models.ForeignKey(TimeDef, on_delete=models.CASCADE, default='')
    DateOfShow = models.DateField(default='')
    Film = models.ForeignKey(FilmData, on_delete=models.CASCADE)
    Cost = models.CharField(default='', max_length=50)
    End = models.TimeField(default='')
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Chair(models.Model):
    # Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # IsEmpty = models.BooleanField(default=True)
    Name = models.CharField(default='', max_length=20)
    Type = models.CharField(default='', max_length=50)
    # Django chỉ cho 1 khóa chính


class ChairInRoom(models.Model):
    Room = models.ForeignKey(Room, on_delete=models.CASCADE, default='')
    Chair = models.ForeignKey(Chair, on_delete=models.CASCADE, default='')
    Status=models.IntegerField(default=0)
    Daytemp=models.DateField(default = datetime.date.today)
    showtime = models.IntegerField(default=0)
    class Meta:
        unique_together = (("Room", "Chair","showtime"),)

class TicketDetail(models.Model):
    GuessInfo = models.ForeignKey(GuessInfo, on_delete=models.CASCADE ,default='')
    ShowTimes = models.ForeignKey(ShowTimes, on_delete=models.CASCADE)
    Chair = models.CharField(default='',max_length=30)
    CinemaInfo = models.ForeignKey(CinemaInfo, on_delete=models.CASCADE)
    #class Meta:
     #   unique_together = (("FilmData", "CinemaInfo"),)

class FilmInCinema(models.Model):
    FilmData = models.ForeignKey(FilmData, on_delete=models.CASCADE, default='')
    CinemaInfo = models.ForeignKey(CinemaInfo, on_delete=models.CASCADE, default='')

    class Meta:
        unique_together = (("FilmData", "CinemaInfo"),)


class BillTemp(models.Model):
    GuessInfo = models.ForeignKey(GuessInfo, on_delete=models.CASCADE)

