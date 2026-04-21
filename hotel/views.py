from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Room, Booking
from django.contrib import messages
import razorpay
from django.conf import settings



# Create your views here.
client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

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
        
        
        # Store data temporarily in session
        request.session['booking_data'] = {
            'name': name,
            'check_in': check_in,
            'check_out': check_out,
            'room_id': room.id
        }
        
        # Redirect to payment
        return redirect('payment', room_id=room.id)
    return render(request, 'booking.html', {'room': room})

   
# 💳 PAYMENT VIEW
def payment(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    order = client.order.create({
        "amount": room.price * 100,  # in paise
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, 'payment.html', {
        'order': order,
        'room': room,
        'razorpay_key': settings.RAZORPAY_KEY
    })


# ✅ VERIFY PAYMENT & SAVE BOOKING
def payment_success(request):
    if request.method == "POST":
        data = request.session.get('booking_data')

        room = Room.objects.get(id=data['room_id'])

        Booking.objects.create(
            customer_name=data['name'],
            room=room,
            check_in=data['check_in'],
            check_out=data['check_out']
        )

        room.is_available = False
        room.save()

        messages.success(request, "Payment successful & Room booked!")
        return redirect('/')


# ❌ CANCEL BOOKING
def cancel_booking(request, room_id):
    room = Room.objects.get(id=room_id)
    booking = Booking.objects.filter(room=room).first()

    if booking:
        booking.delete()
        room.is_available = True
        room.save()

    return redirect('/')