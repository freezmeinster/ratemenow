from django.contrib.auth.models import User

admin = User.objects.create_superuser("admin", "ratemenow@o-leafs.com", "admin")

for i in range(1,11):
    username = "demouser%s" % i
    email = username+"@o-leafs.com"
    user = User.objects.create(
         username = username,
         email = email,
         is_active = True,
         is_staff = True )
    user.set_password(username)
    user.save()
