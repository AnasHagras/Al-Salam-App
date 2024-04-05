from users.models import User

try:
    admin = User.objects.create_superuser("123456789", "1")
except:
    admin = User.objects.get(phone_number="123456789")

try:
    customer = User.objects.create_user("987654321", "1")
    print("Customer created")
except:
    customer = User.objects.get(phone_number="987654321")
