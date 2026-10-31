from django.db import models
    # Create your models here.
class housingmember(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    otp = models.IntegerField()
    otp_used = models.IntegerField()
    is_rented = models.BooleanField(default=False)
    is_admin = models.IntegerField(default=0)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    class Meta:
        db_table = "Housing_Member"

    def __str__(self):
        return f"{self.member_id} - {self.member_name}"

class family_members(models.Model):
    family_member_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(housingmember,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=10)
    relation = models.CharField(max_length=15)

    class Meta:
        db_table = "Family_Member"

    def __str__(self):
        return f"{self.family_member_id} - {self.name}"

class notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    notice_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Notice"

    def __str__(self):
        return f"{self.notice_id} - {self.title}"

class events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    event_date = models.DateField(auto_now_add=True)
    event_time = models.TimeField(auto_now_add=True)
    cover_image =models.ImageField(upload_to='cover_image/', blank=True, null=True)

    class Meta:
        db_table = "Events"

    def __str__(self):
        return f"{self.event_id} - {self.event_name}"

class complaints(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    complaint_title = models.CharField(max_length=30)
    descritpion = models.CharField(max_length=150)
    member_id = models.ForeignKey(housingmember,on_delete=models.CASCADE)
    status = models.CharField(max_length=10,default="Pending")

    class Meta:
        db_table = "Complaints"

    def __str__(self):
        return f"{self.complaint_id} - {self.complaint_title}"


class clubhouse_booking(models.Model):
    clubhouse_booking_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(housingmember,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    basic_charges = models.IntegerField()
    total_amount = models.IntegerField()
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=10,default="Pending")

    class Meta:
        db_table = "Club_house_booking"

    def __str__(self):
        return f"{self.clubhouse_booking_id} - {self.start_date}"


class house_worker_type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=30)
    descripition = models.CharField(max_length=150)

    class Meta:
        db_table = "House_worker_type"

    def __str__(self):
        return f"{self.type_id} - {self.type_name}"



class house_worker(models.Model):
    worker_id = models.AutoField(primary_key=True)
    worker_name = models.CharField(max_length=15)
    contact_no = models.CharField(max_length=10)
    in_time = models.TimeField()
    out_time = models.TimeField()
    type_id = models.ForeignKey(house_worker_type,on_delete=models.CASCADE)
    basic_charges = models.CharField(max_length=20)

    class Meta:
        db_table = "House_worker"

    def __str__(self):
        return f"{self.worker_id} - {self.worker_name}"



class maintanance_payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(housingmember,on_delete=models.CASCADE)
    month = models.CharField(max_length=10)
    amount = models.IntegerField()
    payment_mode = models.IntegerField()
    payment_date = models.DateField(auto_now_add=True)


    class Meta:
        db_table = "Maintanance_payment"
    
    def __str__(self):
        return f"{self.payment_id} - {self.month}"



