from django.shortcuts import get_object_or_404, redirect, render
from .models import Room, Booking
from django.contrib import messages


def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if not room.is_available:
        messages.error(request, "Room is already booked!")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # ✅ Direct booking (no payment)
        Booking.objects.create(
            customer_name=name,
            room=room,
            check_in=check_in,
            check_out=check_out
        )

        # Update room availability
        room.is_available = False
        room.save()

        messages.success(request, "Room booked successfully!")
        return redirect('home')

    return render(request, 'booking.html', {'room': room})


def cancel_booking(request, room_id):
    room = Room.objects.get(id=room_id)
    booking = Booking.objects.filter(room=room).first()

    if booking:
        booking.delete()
        room.is_available = True
        room.save()

    messages.success(request, "Booking cancelled successfully!")
    return redirect('home')

def booking(request):
    return render(request, 'bookings.html')