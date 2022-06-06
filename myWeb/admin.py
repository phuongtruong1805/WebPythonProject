from django.contrib import admin
from .models import GuessInfo,\
    CinemaInfo, FilmData,\
    Room, ShowTimes, Chair,\
    TicketDetail, FilmInCinema,\
    TimeDef, ChairInRoom
# Register your models here.
admin.site.register(GuessInfo)
admin.site.register(CinemaInfo)
admin.site.register(FilmData)
admin.site.register(Room)
admin.site.register(ShowTimes)
admin.site.register(Chair)
admin.site.register(TicketDetail)
admin.site.register(FilmInCinema)
admin.site.register(TimeDef)
admin.site.register(ChairInRoom)