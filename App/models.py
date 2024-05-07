from django.db import models

# Create your models here.
class login_table(models.Model):
    Username=models.CharField(max_length=100)
    Password=models.CharField(max_length=100)
    Type=models.CharField(max_length=100)

class Branch_table(models.Model):
  LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
  Name=models.CharField(max_length=100)
  Place=models.CharField(max_length=100)
  post=models.CharField(max_length=100)
  Pin=models.IntegerField()
  Phone=models.BigIntegerField()
  latitude=models.FloatField()
  longitude=models.FloatField()
  Email=models.CharField(max_length=100)


class Staff_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    BRANCHID=models.ForeignKey(Branch_table,on_delete=models.CASCADE)
    Fname =models.CharField(max_length=100)
    Lname = models.CharField(max_length=100)
    Gender = models.CharField(max_length=50)
    DOB = models.DateField()
    Phone = models.BigIntegerField()
    Email = models.CharField(max_length=50)
    image = models.FileField()
    Basicpay =models.IntegerField()
    Adharnumber =models.CharField(max_length=20)

class Attendance_table(models.Model):
    STAFFID = models.ForeignKey(Staff_table,on_delete=models.CASCADE)
    Date = models.DateField()
    Attendance = models.CharField(max_length=400)



class Inventory_table(models.Model):
    BRANCHID =models.ForeignKey(Branch_table,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Quantity=models.IntegerField()
    Details = models.CharField(max_length=200)
    Status = models.CharField(max_length=200)
    Date =models.DateTimeField()

class Leaverequest_table(models.Model):
    STAFFID = models.ForeignKey(Staff_table,on_delete=models.CASCADE)
    Reason = models.CharField(max_length=300)
    Date =models.DateTimeField()
    Numofdays=models.CharField(max_length=50)
    Fromdate=models.DateField()
    Status=models.CharField(max_length=200)
class Customer_table(models.Model):
    LOGINID=models.ForeignKey(login_table,on_delete=models.CASCADE)
    Fname=models.CharField(max_length=100)
    Lname=models.CharField(max_length=100)
    Gender=models.CharField(max_length=50)
    Place=models.CharField(max_length=100)
    Post=models.CharField(max_length=100)
    Pin=models.CharField(max_length=20)
    Phone=models.BigIntegerField()
    Email=models.CharField(max_length=50)


class Category_table(models.Model):
    categoryname=models.CharField(max_length=100)



class Cosmeticproduct(models.Model):
    BRANCHID =models.ForeignKey(Branch_table,on_delete=models.CASCADE)
    CATEGORY =models.ForeignKey(Category_table,on_delete=models.CASCADE)
    Product=models.CharField(max_length=300)
    Details=models.CharField(max_length=500)
    Photo=models.FileField()
    Uses=models.CharField(max_length=200)
    Company=models.CharField(max_length=200)
class Cosmeticstock(models.Model):
    COSMETICID=models.ForeignKey(Cosmeticproduct,on_delete=models.CASCADE)
    Quantity=models.CharField(max_length=500)
    Manufacturedate=models.DateField()
    Expiringdate=models.DateField()
    Price=models.IntegerField()


class Facility_table(models.Model):
    BRANCHID = models.ForeignKey(Branch_table, on_delete=models.CASCADE)
    Facility =models.CharField(max_length=500)
    Details =models.CharField(max_length=500)
    Price=models.IntegerField()
    Image=models.FileField()
    Time=models.CharField(max_length=50)

class Offer_table(models.Model):
    FACILITYID=models.ForeignKey(Facility_table,on_delete=models.CASCADE)
    Percentage=models.IntegerField()
    Fromdate=models.DateField()
    Todate=models.DateField()
    Image=models.FileField()


class Booking_table(models.Model):
    CUSTOMERID=models.ForeignKey(Customer_table,on_delete=models.CASCADE)
    Date=models.DateField()
    Time=models.TimeField()
    book_date = models.DateField(null=True)
    slot_time = models.CharField(max_length=30, null=True)
    Status=models.CharField(max_length=300)
    total=models.BigIntegerField()

class Bookingdetails_table(models.Model):
    BOOKINGID=models.ForeignKey(Booking_table,on_delete=models.CASCADE)
    FACILITYID=models.ForeignKey(Facility_table,on_delete=models.CASCADE)
    status=models.CharField(max_length=20)
    offer=models.ForeignKey(Offer_table,on_delete=models.CASCADE,null=True,blank=True)

class Assignwork_table(models.Model):
    STAFFID = models.ForeignKey(Staff_table,on_delete=models.CASCADE)
    BOOKINGID = models.ForeignKey(Booking_table,on_delete=models.CASCADE)
    Datetime =models.DateField()
    Status =models.CharField(max_length=200)

class Rentalproduct_table(models.Model):
    BRANCHID=models.ForeignKey(Branch_table,on_delete=models.CASCADE)
    Product=models.CharField(max_length=300)
    Description=models.CharField(max_length=300)
    Image=models.FileField()
    price=models.IntegerField()
    quantity=models.IntegerField()
    Type=models.CharField(max_length=100)

class Rentalbooking_table(models.Model):
    CUSTOMERID=models.ForeignKey(Customer_table,on_delete=models.CASCADE)
    Date=models.DateField()
    Status=models.CharField(max_length=300)
    Fromdate = models.DateField(blank=True,null=True)
    Todate = models.DateField(blank=True,null=True)
    Total=models.FloatField()


class Rentalbookingdetails_table(models.Model):
    RENTALBOOKING=models.ForeignKey(Rentalbooking_table,on_delete=models.CASCADE)
    RENTALPRODUCTID=models.ForeignKey(Rentalproduct_table,on_delete=models.CASCADE)
    Status=models.CharField(max_length=300)
    quantity=models.BigIntegerField()

class Complaint_table(models.Model):
    CUSTOMERID=models.ForeignKey(Customer_table,on_delete=models.CASCADE)
    Complaint=models.CharField(max_length=500)
    Date=models.DateField()
    Reply=models.CharField(max_length=500)


class Feedbacktobranch_table(models.Model):
    BRANCHID =models.ForeignKey(Branch_table,on_delete=models.CASCADE)
    CUSTOMERID = models.ForeignKey(Customer_table, on_delete=models.CASCADE)
    Feedback=models.CharField(max_length=300)
    Rating=models.CharField(max_length=300)
    Date=models.DateField()

class Feedbacktoapp_table(models.Model):
    CUSTOMERID = models.ForeignKey(Customer_table, on_delete=models.CASCADE)
    Feedback = models.CharField(max_length=300)
    Rating = models.CharField(max_length=300)
    Date = models.DateField()

class payment_table(models.Model):
    oid=models.ForeignKey(Rentalbooking_table,on_delete=models.CASCADE)
    amount=models.BigIntegerField()
    date=models.DateField()













