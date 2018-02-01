from datetime import date
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=64)
    num_seats = models.IntegerField()
    has_beamer = models.BooleanField(default=True)

    #atrybut bookings powstał nam z related_name w Booking :)
    def is_currently_booked(self):
        bookings_today = self.bookings.filter(date=date.today())
        return len(bookings_today) != 0

class Booking(models.Model):
    room = models.ForeignKey(Room, related_name='bookings')
    date = models.DateField() # wartość domyślna tylko dla ułatwienia
    comment = models.TextField(default='', blank=True)

    #zapewniamy, że na dany dzień jest tylko jedna rezerwacja
    class Meta:
        unique_together = ("room", "date")


#Room.objects.get(id=1).is_currently_booked()

"""
Zabukowanie sali w shellu

Room.objects.get(id=1).is_currently_booked()
Out[2]: False

In [3]: Booking.objects.create(room_id=1)
Out[3]: <Booking: Booking object>

In [4]: Room.objects.get(id=1).is_currently_booked()
Out[4]: True
"""