from django.db import models

# Create your models here.

class Room(models.Model):
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=50)
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number}"


class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

   
def save(self, *args, **kwargs):
        self.room.is_available = False
        self.room.save()
        super().save(*args, **kwargs)

