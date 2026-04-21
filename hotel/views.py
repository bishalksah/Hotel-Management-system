from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Room, Booking
from django.contrib import messages



# Create your views here.

def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if not room.is_available:
        messages.error(request, "Room is already booked!")
        return redirect('/')

    if request.method == 'POST':
        name = request.POST.get('name')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        Booking.objects.create(
            customer_name=name,
            room=room,
            check_in=check_in,
            check_out=check_out
        )
        room.is_available = False
        room.save()

        # ✅ Success message
        messages.success(request, "Room booked successfully!")

        
        
        
        return redirect('/')
    return render(request, 'booking.html', {'room': room})