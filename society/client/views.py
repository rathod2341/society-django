from django.shortcuts import render , redirect

from django.contrib import messages
from client.models import housingmember
from client.models import complaints
from client.models import notice
from client.models import events
from client.models import house_worker
from client.models import house_worker_type ,  family_members
from client.models import clubhouse_booking , maintanance_payment

def login(request):
    if request.method == "POST":
        name = request.POST['email']
        pwd = request.POST['password']

        c = housingmember.objects.filter(email=name , password=pwd).count()
        if c == 1:
            obj = housingmember.objects.get(email=name , password=pwd)
            request.session['user_id']=obj.member_id
            return redirect("/index/")
        else:
            messages.error(request,"Invalid username or password")
            return render(request,"login.html")
   
    else:
        return render(request,"login.html")

def register(request):
    if request.method == "POST":
        n = request.POST.get ('member_name')
        c = request.POST.get ('contact')
        em= request.POST.get ('email')
        pwd = request.POST.get ('password')
        ir = request.POST.get ('is_rented')
        pf = request.POST.get ('profile_photo')


        housingmember.objects.create(
            member_name = n ,
            contact = c ,
            email = em , 
            password = pwd ,
            otp = 0 ,
            otp_used = 0,
            is_rented = ir,
            is_admin = 0,
            profile_photo = pf




            )
        
        return redirect("/login/")
    else:
     return render(request,"register.html")
    
def table(request):
    if 'user_id' not in request.session:
        return redirect("/login/")
    dt = complaints.objects.all()
    return render(request,"datatable.html",{'dt':dt})

def member_list(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    ml = housingmember.objects.all()
    print(ml)
    return render(request,"member_list.html",{'ml':ml})

def notices(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    n = notice.objects.all().order_by("-notice_date")
    return render(request,"notice.html",{'n':n})

def event(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    ev = events.objects.all().order_by("-event_date")
    return render(request,"events.html",{'ev':ev})

def houseworker(request,name=""):
    if 'user_id' not in request.session:
        return redirect("/login/")

    if name == "":
        hw = house_worker.objects.all()
    else:
        obj = house_worker_type.objects.get(type_name=name)
        hw = house_worker.objects.filter(type_id=obj.type_id)
    return render(request,"house_worker.html",{'hw':hw})

def houseworkertype(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    hwt = house_worker_type.objects.all()
    return render(request,"house_worker_type.html",{'hwt':hwt})     

def add_complain(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    u = request.session['user_id']
    if request.method == "POST":
        complaints.objects.create(
            complaint_title=request.POST["title"],
            descritpion=request.POST["description"],
            member_id_id=u
        ).save()
        return redirect("/complaints/")

    else:
        return render(request,"form.html")   

 
def profile(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    mid = request.session['user_id']
    h = housingmember.objects.get(member_id=mid)
    if request.method == "POST":
        h.member_name = request.POST.get("name")
        h.contact = request.POST.get("contact")
        h.email = request.POST.get("email")
        h.password = request.POST.get("password")
        h.is_rented = request.POST.get("inputis_rented") == "on"    
        
        h.save()
        return redirect("/profile/")

    else:
        
        return render(request,"profile.html",{'housingmember':h})


def logout(request):
    try:
        del request.session['user_id']
        return redirect('/login/')                                                              
    except:
        pass
    

def family_member(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    u = request.session['user_id']
    fm = family_members.objects.filter(member_id=u)
    return render(request,"contact_userlist.html",{'fm':fm})

def delete_family(request,id=0):
    if 'user_id' not in request.session:
        return redirect("/login/")

    obj = family_members.objects.get(family_member_id=id)
    obj.delete()
    return redirect("/family_member/")

def add_family(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    if request.method == "POST":
        u=request.session['user_id']
        family_members.objects.create(
            member_id_id=u,
            name=request.POST['name'],
            contact=request.POST['contact'],
            relation=request.POST['relation']

        ).save()

        return redirect("/family_member/")
    else:

        return render(request,"add_family.html")
    
def index(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    u = request.session['user_id']
    c = complaints.objects.all().count()
    m = housingmember.objects.all().count()
    w = house_worker.objects.all().count()
    f = family_members.objects.filter(member_id=u).count()

    my = complaints.objects.filter(member_id=u)

    return render(request,"index2.html",{'complain':c,'member':m,'house_worker':w,'family':f,'my':my})    

def clubhouse(request):
    u = request.session['user_id']
    clb = clubhouse_booking.objects.filter(member_id=u)
    return render(request,"club_house.html",{'clb':clb})


def clubhousebooking(request):
    if 'user_id' not in request.session:
        return redirect("/login/")

    u = request.session['user_id']
    if request.method == "POST":
        clubhouse_booking.objects.create(
            start_date=request.POST["start_date"],
            end_date=request.POST["end_date"],
            member_id_id=u
        ).save()
        return redirect("/clubhousebooking/")

    else:
        return render(request,"booking_form.html")   
    

def forgot_pwd(request):
    return render(request,"forgot_pwd.html")

from django.core.mail import send_mail
import random
from society import settings


def sendotp(request):

    otp1 = random.randint(1000, 9999)
    e = request.POST['email']

    request.session['temail']=e

    obj = housingmember.objects.filter(email=e).count()

    if obj == 1:

        val = housingmember.objects.filter(email=e).update(otp=otp1 , otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

        print("Mail Send-------------")
        return render(request, 'set_pwd.html')
    


def set_password(request):

    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['pass']
        T_cpass = request.POST['cpass']

        if T_pass == T_cpass:

            e = request.session['temail']
            val = housingmember.objects.filter(email=e,otp = T_otp,otp_used = 0).count()

            if val == 1:
                housingmember.objects.filter(email = e).update(otp_used = 1,password = T_pass)
                return redirect("/login")
            else:
                messages.error(request,"Invalid OTP")
                return render(request,"forgot_password.html")

        else:
            messages.error(request,"New password and Confirm password does not match ")
            return render(request,"set_password.html")

    else:
        return redirect("/forgot_password")

from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def rec(request):
#     return render(request,"reciept.html")

# def maintanance_pay(request):
#      if 'user_id' not in request.session:
#         return redirect("/login/")
#      u = request.session['user_id']
#      mp = maintanance_payment.objects.filter(member_id=u)
#      return render(request,"mp.html",{'mp':mp})

from datetime import datetime
from django.shortcuts import render, redirect
from .models import maintanance_payment

def maintanance_pay(request):
    if 'user_id' not in request.session:
        return redirect('/login/')

    user_id = request.session['user_id']

    # Current month number (1-12)
    current_month = datetime.now().month

    # Month names
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    payment_list = []

    for month in months[:current_month]:
        payment = maintanance_payment.objects.filter(
            member_id_id=user_id,
            month=month
        ).first()

        payment_list.append({
            'month': month,
            'status': 'Paid' if payment else 'Unpaid',
            'amount': payment.amount if payment else "500",
            'payment_date': payment.payment_date if payment else None,
            'payment_mode': payment.payment_mode if payment else "Pending"
        })

    return render(request, 'mp.html', {'payment_list': payment_list})


@csrf_exempt
def rec(request):

    if request.method == "POST":

        id = request.POST.get("user_id")
        member = housingmember.objects.get(
            member_id=id
        )

        month = request.POST.get("month")      # e.g. July
        amount = 500
        payment_mode = 1

        # Check if payment already exists for this month
        if not maintanance_payment.objects.filter(
            member_id=member,
            month=month
        ).exists():

            maintanance_payment.objects.create(
                member_id=member,
                month=month,
                amount=amount,
                payment_mode=payment_mode
            )

        return redirect("/maintanance_payment/")   # Redirect after saving

    return render(request, "reciept.html")