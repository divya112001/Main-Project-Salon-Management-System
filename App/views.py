from datetime import datetime
from .encode_faces import enf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from App.models import *


def mainhome(request):
    from App.encode_faces import enf
    obb = Staff_table.objects.all()
    result = []
    for i in obb:
        row = [i.id, "media/" + str(i.image)]
        result.append(row)
    enf(result)
    return render(request,'Admin/adminindex.html')
def login(request):
    return render(request,'Admin/login_index.html')

def logout(request):
    auth.logout(request)
    return render(request,'Admin/login_index.html')

@login_required(login_url='/')
def map(request):
    return render(request,'Admin/map.html')
    # return render(request,'Admin/login_index.html')
def logincode(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    try:
        ob=login_table.objects.get(Username=username, Password=password)
        # if ob.Username!=username or ob.Password!=password:
        #     return HttpResponse('''<script>alert("Invalid username or password..!");window.location='/'</script>''')
        if ob.Type == "admin":
            obb=auth.authenticate(username="admin",password="admin")
            if obb is not None:
                auth.login(request,obb)
            request.session['lid'] = ob.id
            return redirect('/adminshome')
        elif ob.Type == "Branch":
            obb = auth.authenticate(username="admin", password="admin")
            if obb is not None:
                auth.login(request,obb)


            x=Branch_table.objects.filter(LOGIN=ob.id)
            if len(x)>0:
                request.session['lid'] = ob.id
                request.session['branchName'] = x[0].Name
                print(request.session['branchName'])

                return  redirect('/branchhome')
            else:
                return HttpResponse('''<script>alert("User does not Exist..!");window.location='/'</script>''')


        else:
            return HttpResponse('''<script>alert("Invalid username or password..!");window.location='/'</script>''')
    except Exception as e :
        print(e)
        return HttpResponse('''<script>alert("Invalid username or password..!");window.location='/'</script>''')
@login_required(login_url='/')
def adminshome(request):
    return render(request,'Admin/adminhomeindex1.html')
@login_required(login_url='/')
def adminhome(request):
    return render(request, 'Admin/adminindex.html')
@login_required(login_url='/')
def addbranches(request):
    return render(request,'Admin/addbranches.html')
@login_required(login_url='/')
def addbranch_post(request):
    Branch=request.POST['textfield']
    Place=request.POST['textfield2']
    Post=request.POST['textfield3']
    pin=request.POST['textfield4']
    Phone=request.POST['textfield5']
    Email=request.POST['textfield6']
    Username=request.POST['textfield8']
    Password=request.POST['textfield9']



    un=login_table.objects.filter(Username=Username,Password=Password)
    if len(un)>0:
        return HttpResponse('''<script>alert('username already existing');window.location='/login'</script>''')
    else:
        obj=login_table()
        obj.Username=Username
        obj.Password=Password
        obj.Type='Branch'
        obj.save()

        ob=Branch_table()
        ob.Name =Branch
        ob.Place=Place
        ob.post=Post
        ob.Pin=pin
        ob.Phone=Phone
        ob.Email=Email
        ob.LOGIN=obj
        ob.latitude=0
        ob.longitude=0
        ob.save()
        request.session['bid']=ob.id
        return redirect('map')




@login_required(login_url='/')
def map1(request):
    return render(request,"Admin/map.html")

@login_required(login_url='/')
def mapcode(request):
    latitude=request.POST['lat']
    longitude=request.POST['lon']
    ob=Branch_table.objects.get(id=request.session['bid'])
    ob.latitude=latitude
    ob.longitude=longitude
    ob.save()

    return HttpResponse('''<script>window.location='/managebranch'</script>''')

@login_required(login_url='/')
def managebranch(request):
    ob=Branch_table.objects.all().order_by('-id')
    return render(request,'Admin/managebranches.html',{'val':ob})

@login_required(login_url='/')
def deletebranch(request,id):
    ob=login_table.objects.get(id=id)
    ob.delete()
    # return HttpResponse('''<script>alert("Deleted");window.location='/managebranch'</script>''')
    return redirect('/managebranch')
@login_required(login_url='/')
def editbranch(request,id):
    request.session['bid']=id
    ob=Branch_table.objects.get(id=id)
    return render(request,"Admin/editbranches.html",{'val':ob})
@login_required(login_url='/')
def editbranch_post(request):
    Branch=request.POST['textfield']
    Place=request.POST['textfield2']
    Post=request.POST['textfield3']
    pin=request.POST['textfield4']
    Phone=request.POST['textfield5']
    Email=request.POST['textfield6']



    ob=Branch_table.objects.get(id=request.session['bid'])
    ob.Name =Branch
    ob.Place=Place
    ob.post=Post
    ob.Pin=pin
    ob.Phone=Phone
    ob.Email=Email
    ob.save()
    # return HttpResponse('''<script>alert("updated");window.location='/managebranch'</script>''')
    return redirect('/managebranch')
@login_required(login_url='/')
def admin_add_category(request):
    return render(request,'Admin/add_category.html')
@login_required(login_url='/')
def addcateogory_post(request):
    Category=request.POST["textfield"]
    ob=Category_table()
    ob.categoryname=Category
    ob.save()
    return redirect('/admin_view_category')

@login_required(login_url='/')
def admin_view_category(request):
    ob=Category_table.objects.all().order_by('-id')
    return render(request,'Admin/View_category.html',{'val':ob})
@login_required(login_url='/')
def deletecategory(request,id):
    ob = Category_table.objects.get(id=id)
    ob.delete()
    return redirect('/admin_view_category')
@login_required(login_url='/')
def searchcategory(request):
    name=request.POST["textfield"]
    ob=Category_table.objects.filter(categoryname__istartswith=name)
    print(name,"---",ob)
    return render(request,'Admin/View_category.html',{'val':ob})


@login_required(login_url='/')
def searchbranch(request):
    name=request.POST['textfield']
    ob=Branch_table.objects.filter(Name__istartswith=name)
    return render(request,'Admin/managebranches.html',{'val':ob})
@login_required(login_url='/')
def sendreply(request,id):
    ob=Complaint_table.objects.get(id=id)
    request.session['ridd']=ob.id
    return render(request,'Admin/sendreply.html')

@login_required(login_url='/')
def addreply(request):
    a=request.POST['textarea']
    ob=Complaint_table.objects.get(id=request.session['ridd'])
    ob.Reply=a
    ob.Date=datetime.now()
    ob.save()
    return redirect('/viewcomplaints')

@login_required(login_url='/')
def viewcomplaints(request):
    ob=Complaint_table.objects.all()
    return render(request,'Admin/viewcomplaints.html',{'val':ob})
def viewcomplaintssrch(request):
    date=request.POST['textfield']
    ob=Complaint_table.objects.filter(Date=date)
    return render(request,'Admin/viewcomplaints.html',{'val':ob ,"a":date})


def feedbacksearch(request):
    date=request.POST['textfield']
    ob=Feedbacktobranch_table.objects.filter(Date=date)
    return render(request,'Admin/viewcomplaints.html',{'val':ob ,"a":date})



@login_required(login_url='/')
def viewcosmeticproduct(request):
    ob=Cosmeticproduct.objects.all()
    return render(request,'Admin/viewcosmeticproduct.html',{"val":ob})
@login_required(login_url='/')


def viewfeedback(request):
    ob=Feedbacktobranch_table.objects.all()
    return render(request,'Admin/viewfeedback.html',{"val":ob})

@login_required(login_url='/')


def viewfeedbacksrch(request):
    nm=request.POST['textfield']
    ob=Feedbacktobranch_table.objects.filter(BRANCHID__Name__icontains=nm)
    return render(request,'Admin/viewfeedback.html',{"val":ob,"a":nm})




@login_required(login_url='/')
def viewproductrequest(request):

    return render(request,'Admin/viewproductrequest.html')



@login_required(login_url='/')
def viewstaffattendance(request):
    # ob=Attendance_table.objects.all()
    b=Branch_table.objects.all()
    return render(request,'Admin/viewstaffattendance.html',{'branch':b})


@login_required(login_url='/')
def viewstaff_post(request):
    # date=request.POST["textfield"]
    bid=request.POST["branch"]
    year = int(request.POST["year"])
    month = int(request.POST["month"])
    b = Branch_table.objects.get(id=bid)

    # ob=Attendance_table.objects.filter(Date__exact=date,STAFFID__BRANCHID=bid)
    # return render(request,'Admin/viewstaffattendance.html',{'val':ob,'branch':b})
    staffid=[]
    staffname=[]
    br=Staff_table.objects.filter(BRANCHID=bid)
    for i in br:
        staffid.append(i.id)
        staffname.append(i.Fname)
    # dates = get_dates(year, month)
    # days = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'saturday']
    days = staffid
    # hours = ['1', '2', '3', '4', '5', '6']
    hours = get_dates(year, month)
    day_date=[]
    l=len(hours)

    for i in range(1,l+1):
        day_date.append(i)

    day_date.append("Percentage")
    print(l, "====================", day_date)
    timetablee = []
    for i in days:
        print("mmmmm")
        subj = []
        for j in hours:
            # qry4 = "SELECT timetable.* ,subject.* FROM timetable, SUBJECT WHERE `timetable`.`subject_id`=`subject`.`subject_id` and day='" + i + "' and hour='" + j + "' and `subject`.`course_id`='" + course + "'and `subject`.`semester`='" + sem + "'"
            # occ = timetable.objects.filter(SUBJECT__sem=sem, SUBJECT__COURSE__id=crsid, day=i, hour=j)
            # print("----", sem, crsid, i, j)
            # print(timetable.objects.filter(SUBJECT__sem=sem, SUBJECT__COURSE__id=crsid, day=i, hour=j))
            # print(occ, "===================================================")
            occ=Attendance_table.objects.filter(STAFFID=i,Date__exact=j)
            if len(occ) > 0:
                subj.append("P")
            else:
                subj.append("A")
        total=len(subj)
        present=subj.count("P")

        persc=str((present/total)*100)+"%"
        subj.append(persc)


        # timetablee.append(i)
        timetablee.append(subj)
        print(subj)

    print(timetablee)

    obcourse = Branch_table.objects.all()
    print("-",year)
    return render(request, 'Admin/viewstaffattendance.html', {"timetab": zip(timetablee, staffname), "day": day_date, 'branch': obcourse,"date":day_date,"branchname":b.Name,"y":year,"m":month,"b":b})


@login_required(login_url='/')
def viewstaffsalary(request):
    obb=Staff_table.objects.all()
    ob=Branch_table.objects.all()
    return render(request,'Admin/viewstaffsalary.html',{'val':ob,'next':obb})

@login_required(login_url='/')
def viewstaffsalarysearch(request):
    ob=Branch_table.objects.all()
    branch=request.POST['branch']
    obb=Staff_table.objects.filter(BRANCHID=branch)
    return render(request,'Admin/viewstaffsalary.html',{'val':ob,'next':obb})



@login_required(login_url='/')
def admin_monthlyreports(request):
    ok=Branch_table.objects.all()
    return render(request, 'Admin/monthly_report.html',{"k":ok})
@login_required(login_url='/')
def admin_monthlyreports_post(request):
    year=request.POST["year"]
    month=request.POST["month"]
    bid=request.POST['b']
    product=Rentalproduct_table.objects.filter(BRANCHID__LOGIN=bid)

    print(year,month,"=================")

    rentallist=[]
    rent_Total=0
    for i in product:
        amt=0
        x=Rentalbookingdetails_table.objects.filter(RENTALPRODUCTID=i.id,RENTALBOOKING__Date__month=int(month),RENTALBOOKING__Date__year=int(year))
        print(x,"-----------------------")
        for ij in x:
            amt=amt+(int(ij.quantity)*int(ij.RENTALPRODUCTID.price))
        rent_Total=rent_Total+amt

        rentalrow={"pname":i.Product,"image":i.Image.url,"ExactPrice":i.price,"totalabooking":str(len(x)),"TotalAmount":amt}
        if len(x)>0:
            rentallist.append(rentalrow)

    facilitylist = []
    facility_Total = 0
    facility=Facility_table.objects.filter(BRANCHID__LOGIN=bid)
    for f in facility:


        # for i in product:
            amt1 = 0
            x1 = Bookingdetails_table.objects.filter(FACILITYID=f.id, BOOKINGID__Date__month=int(month),
                                                     BOOKINGID__Date__year=int(year))
            print(x, "-----------------------")
            for fa in x1:
                amt1 = amt1 + fa.FACILITYID.Price
            facility_Total = facility_Total + amt1

            facilityrow = {"pname": f.Facility, "image": f.Image.url, "ExactPrice": f.Price, "totalabooking": str(len(x1)),
                         "TotalAmount": amt1}
    if len(x) > 0:
            facilitylist.append(facilityrow)
    ok = Branch_table.objects.all()
    return render(request, 'Admin/monthly_report.html',{"rental":rentallist,"rent_Total":rent_Total,"facility":facilitylist,"facility_Total":facility_Total,"k":ok})






#____________________________________


@login_required(login_url='/')
def addcosmetics(request):
    ob=Category_table.objects.all()
    return render(request,'Branch/addcosmetics.html',{'cat':ob})
@login_required(login_url='/')
def addcosmetic_post(request):
    Product=request.POST["textfield"]
    Details=request.POST["textfield3"]
    Photo=request.FILES["file"]
    Uses=request.POST["textfield4"]
    Company=request.POST["textfield5"]
    catid=request.POST["catt"]
    fs = FileSystemStorage()
    fsave = fs.save(Photo.name, Photo)

    ob=Cosmeticproduct()
    ob.Product=Product
    ob.Details=Details
    ob.CATEGORY_id=catid
    ob.Uses=Uses
    ob.Company=Company
    ob.Photo=fsave
    ob.BRANCHID = Branch_table.objects.get(LOGIN=request.session["lid"])
    ob.save()
    return redirect('/viewcosmetics')
@login_required(login_url='/')
def viewcosmetics(request):
    ob = Cosmeticproduct.objects.filter(BRANCHID__LOGIN__id=request.session["lid"]).order_by('-id')
    cat=Category_table.objects.all()
    return render(request, 'Branch/managecosmetics.html', {"data":ob,'cat':cat})
@login_required(login_url='/')
def searchviewcosmetics(request):
    fa=request.POST['textfield']
    ob = Cosmeticproduct.objects.filter(BRANCHID__LOGIN__id=request.session["lid"],CATEGORY=fa).order_by('-id')

    cat = Category_table.objects.all()
    return render(request, 'Branch/managecosmetics.html', {"data": ob,'cat':cat})
def deletecosmetics(request,id):
    ob=Cosmeticproduct.objects.get(id=id)
    ob.delete()
    return redirect('/viewcosmetics')
@login_required(login_url='/')
def editcosmetic(request,id):
    request.session['bid']=id
    ob=Cosmeticproduct.objects.get(id=id)
    return render(request,"Branch/editcosmetics.html",{'val':ob})
@login_required(login_url='/')
def editcosmetic_post(request):
    Product=request.POST["textfield"]
    Details=request.POST["textfield3"]
    Uses=request.POST["textfield4"]
    Company=request.POST["textfield5"]

    ob=Cosmeticproduct.objects.get(id=request.session['bid'])
    ob.Product=Product
    ob.Details=Details
    ob.Uses=Uses
    ob.Company=Company
    if 'file' in request.FILES:
        Image=request.FILES["file"]
        fs=FileSystemStorage()
        fsave=fs.save(Image.name,Image)
        ob.Photo=fsave
    ob.save()
    return redirect('/viewcosmetics')
@login_required(login_url='/')
def facilitysearch(request):
    name = request.POST['textfield']
    ob = Facility_table.objects.filter(Name__istartswith=name)
    return render(request, 'Admin/ viewmanagefacility.html', {'val': ob})

@login_required(login_url='/')
def updatestock(request,id):
    ob=Cosmeticstock.objects.filter(COSMETICID=id)
    ob2 = Cosmeticproduct.objects.get(id=id)
    d=datetime.now().strftime("%Y-%m-%d")

    return render(request, 'Branch/updatestock.html',{'cosid':id,"stock":ob,"pr":ob2,"d":d})
@login_required(login_url='/')
def updatestock_post(request):
    Quantity=request.POST["textfield1"]
    cosid=request.POST["cosid"]
    Manufacturingdate=request.POST["textfield3"]
    Expiringdate=request.POST["textfield4"]
    Price=request.POST["textfield5"]
    ob=Cosmeticstock()
    ob.Quantity=Quantity
    ob.Manufacturedate=Manufacturingdate
    ob.Expiringdate=Expiringdate
    ob.COSMETICID_id=cosid
    ob.Price=Price
    ob.save()
    return redirect('/updatestock/'+cosid)
@login_required(login_url='/')
def deletestock(request,id,cosid):
    ob=Cosmeticstock.objects.get(id=id)
    ob.delete()
    return redirect('/updatestock/'+cosid)

@login_required(login_url='/')
def addinventory(request):
    return render(request,'Branch/addinventory.html')
@login_required(login_url='/')
def  addinventory_post(request):
    Name=request.POST["textfield"]
    Quantity=request.POST["textfield2"]
    Details=request.POST["textarea"]
    ob=Inventory_table()
    ob.Name=Name
    ob.Quantity=Quantity
    ob.Details=Details
    ob.Date=datetime.today()
    ob.BRANCHID = Branch_table.objects.get(LOGIN=request.session["lid"])
    ob.save()
    return redirect('/viewmanageinventory')
@login_required(login_url='/')
def viewmanageinventory(request):
    ob=Inventory_table.objects.filter(BRANCHID__LOGIN__id=request.session["lid"]).order_by('-id')
    return render(request, 'Branch/viewmanageinventory.html',{'val':ob})
@login_required(login_url='/')
def editinventory(request,id):
    request.session['inventoryid'] = id
    ob = Inventory_table.objects.get(id=id)
    return render(request, "Branch/editinventory.html", {'data': ob})
@login_required(login_url='/')
def editinventory_post(request):
    Name=request.POST["textfield"]
    Quantity=request.POST["textfield2"]
    Details=request.POST["textarea"]

    ob=Inventory_table.objects.get(id=request.session['inventoryid'])
    ob.Name=Name
    ob.Quantity=Quantity
    ob.Details=Details
    ob.save()
    return HttpResponse('''<script>alert("updated");window.location='/viewmanageinventory'</script>''')


@login_required(login_url='/')
def deleteinventory(request,id):
    ob=Inventory_table.objects.get(id=id)
    ob.delete()
    return redirect('/viewmanageinventory')
@login_required(login_url='/')
def deleteoffer(request,id):
    ob=Offer_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted");window.location='/viewmanageoffer'</script>''')




@login_required(login_url='/')
def searchviewmanageinventory(request):
    fa=request.POST['textfield']
    ob=Inventory_table.objects.filter(BRANCHID__LOGIN__id=request.session["lid"],Name__icontains=fa)
    return render(request, 'Branch/viewmanageinventory.html',{'val':ob})
@login_required(login_url='/')
def addoffer(request):

    print("loginid==",request.session["lid"])
    ob=Facility_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])
    d=datetime.now().strftime("%Y-%m-%d")
    return render(request,'Branch/addoffer.html',{"fac":ob,"d":d})
@login_required(login_url='/')
def addoffer_post(request):
    Facility=request.POST["textfiled"]
    Percentage=request.POST["textfiled2"]
    Fromdate=request.POST["textfiled3"]
    Todate=request.POST["textfiled4"]

    ob=Offer_table()
    ob.FACILITYID_id=Facility
    ob.Percentage=Percentage
    ob.Fromdate=Fromdate
    ob.Todate=Todate

    ob.save()
    return redirect('/viewmanageoffer')
@login_required(login_url='/')
def viewmanageoffer(request):

    print(request.session["lid"],"==============")
    ob=Offer_table.objects.filter(FACILITYID__BRANCHID__LOGIN=request.session["lid"]).order_by('-id')
    obfac = Facility_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])

    return render(request, 'Branch/viewmanageoffer.html',{'val':ob,'faci':obfac})
@login_required(login_url='/')
def viewmanageoffer_search(request):
    facid=request.POST["select"]

    print(request.session["lid"],"==============")
    ob=Offer_table.objects.filter(FACILITYID__BRANCHID__LOGIN=request.session["lid"],FACILITYID=facid)

    obfac = Facility_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])

    return render(request, 'Branch/viewmanageoffer.html',{'val':ob,'faci':obfac})

@login_required(login_url='/')
def addrental(request):
    return render(request,'Branch/addrental.html')
@login_required(login_url='/')
def addrental_post(request):
    Product=request.POST["textfield"]
    Description=request.POST["textfield2"]
    Image=request.FILES["file"]
    Price=request.POST["textfield3"]
    qu=request.POST["textfield4"]

    ob=Rentalproduct_table()
    ob.Product=Product
    ob.Description=Description
    fs = FileSystemStorage()
    fsave = fs.save(Image.name, Image)
    ob.Image=fsave
    ob.Description=Description
    ob.price=Price
    ob.quantity=qu
    ob.BRANCHID = Branch_table.objects.get(LOGIN=request.session["lid"])
    ob.save()
    return redirect('/viewrentalproducts')
@login_required(login_url='/')
def viewrentalproducts(request):
        ob=Rentalproduct_table.objects.filter(BRANCHID__LOGIN__id=request.session["lid"]).order_by('-id')
        return render(request, 'Branch/viewrentalproducts.html', {'val':ob})


@login_required(login_url='/')
def monthlyreports(request):
        return render(request, 'Branch/monthly_report.html')
@login_required(login_url='/')
def monthlyreports_post(request):
    year=request.POST["year"]
    month=request.POST["month"]

    product=Rentalproduct_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])

    print(year,month,"=================")

    rentallist=[]
    rent_Total=0
    for i in product:
        amt=0
        x=Rentalbookingdetails_table.objects.filter(RENTALPRODUCTID=i.id,RENTALBOOKING__Date__month=int(month),RENTALBOOKING__Date__year=int(year))
        print(x,"-----------------------")
        for ij in x:
            amt=amt+(int(ij.quantity)*int(ij.RENTALPRODUCTID.price))
        rent_Total=rent_Total+amt

        rentalrow={"pname":i.Product,"image":i.Image.url,"ExactPrice":i.price,"totalabooking":str(len(x)),"TotalAmount":amt}
        if(len(x))>0:
            rentallist.append(rentalrow)

    facilitylist = []
    facility_Total = 0
    facility=Facility_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])
    for f in facility:


        # for i in product:
            amt1 = 0
            x1 = Bookingdetails_table.objects.filter(FACILITYID=f.id, BOOKINGID__Date__month=int(month),
                                                     BOOKINGID__Date__year=int(year))
            print(x1, "-----------------------")
            for fa in x1:
                amt1 = amt1 + fa.FACILITYID.Price
            facility_Total = facility_Total + amt1

            facilityrow = {"pname": f.Facility, "image": f.Image.url, "ExactPrice": f.Price, "totalabooking": str(len(x1)),
                         "TotalAmount": amt1}
            if len(x1)>0:
                facilitylist.append(facilityrow)
    curdate=datetime.now()
    return render(request, 'Branch/monthly_report.html',{"rental":rentallist,"rent_Total":rent_Total,"facility":facilitylist,"facility_Total":facility_Total,"curdate":curdate})




@login_required(login_url='/')
def deleterental(request,id):
    ob=Rentalproduct_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted");window.location='/viewrentalproducts'</script>''')
@login_required(login_url='/')
def editrental(request,id):
    request.session['rid']=id
    ob=Rentalproduct_table.objects.get(id=id)
    return render(request,'Branch/editrental.html',{'val':ob })
@login_required(login_url='/')
def editrental_post(request):
    try:
        Product=request.POST["textfield"]
        Description=request.POST["textfield2"]
        Image=request.FILES["file"]
        Price=request.POST["textfield3"]
        qu=request.POST["textfield4"]

        ob = Rentalproduct_table.objects.get(id=request.session['rid'])
        ob.Product = Product
        ob.Description = Description
        fs = FileSystemStorage()
        fsave = fs.save(Image.name, Image)
        ob.Image = fsave
        ob.Description = Description
        ob.price =Price
        ob.quantity =qu
        ob.BRANCHID = Branch_table.objects.get(LOGIN=request.session["lid"])
        ob.save()
        return HttpResponse('''<script>alert("Updated");window.location='/viewrentalproducts'</script>''')
    except:
        Product = request.POST["textfield"]
        Description = request.POST["textfield2"]
        Price = request.POST["textfield3"]
        qu = request.POST["textfield4"]
        ob = Rentalproduct_table.objects.get(id=request.session['rid'])
        ob.Product = Product
        ob.Description = Description
        ob.price = Price
        ob.quantity = qu
        ob.BRANCHID = Branch_table.objects.get(LOGIN=request.session["lid"])
        ob.save()
        return HttpResponse('''<script>alert("Updated");window.location='/viewrentalproducts'</script>''')

@login_required(login_url='/')
def addstaff(request):
    return render(request,'Branch/addstaff.html')
@login_required(login_url='/')
def viewmanagestaff(request):
    ob=Staff_table.objects.filter(BRANCHID__LOGIN=request.session['lid'])
    return render(request, 'Branch/viewmanagestaff.html',{'val':ob})
@login_required(login_url='/')
def addstaff_post(request):
    Name=request.POST["textfield"]
    Gender=request.POST["radiobutton"]
    DOB=request.POST["textfield2"]
    Phone=request.POST["textfield3"]
    Image=request.FILES["file"]
    Adharnumber=request.POST["textfield5"]
    Email=request.POST["textfield6"]
    Basicpay=request.POST["textfield7"]
    uname=request.POST["textfield8"]
    passw=request.POST["textfield9"]

    print(uname,"----")


    obb=login_table.objects.filter(Username=uname)
    if len(obb)>0:
        return HttpResponse('''<script>alert("user name already exist");window.location='/viewmanagestaff'</script>''')


    else:
        fs = FileSystemStorage()
        fsave = fs.save(Image.name, Image)
        ob2=login_table()
        ob2.Username=uname
        ob2.Password=passw
        ob2.Type="staff"
        ob2.save()

        from App.encode_faces import enf
        obb = Staff_table.objects.all()
        result = []
        for i in obb:
            row = [i.id, "media/" + str(i.image)]
            result.append(row)
        enf(result)

        ob=Staff_table()
        ob.Fname=Name
        ob.Gender=Gender
        ob.LOGIN_id=ob.id
        ob.DOB=DOB
        ob.Phone=Phone
        ob.Email=Email
        ob.image=fsave
        ob.Adharnumber=Adharnumber
        ob.Basicpay=Basicpay
        ob.LOGIN_id=ob2.id
        ob.BRANCHID=Branch_table.objects.get(LOGIN=request.session["lid"])
        ob.Image = fsave
        ob.save()




        return redirect('/viewmanagestaff')
@login_required(login_url='/')
def deletestff(request,id):
    ob = login_table.objects.get(id=id)
    ob.delete()
    return redirect('/viewmanagestaff')
@login_required(login_url='/')
def searchstaff(request):
    name = request.POST["textfield"]
    ob = Staff_table.objects.filter(Fname__contains=name)
    print(name, "---", ob)
    return render(request, 'Branch/viewmanagestaff.html', {'val': ob})
@login_required(login_url='/')
def editstaff(request,id):
    request.session['staffid'] = id
    ob = Staff_table.objects.get(id=id)
    return render(request, 'Branch/editstaff.html', {'val': ob})
@login_required(login_url='/')
def editstaff_post(request):
    Name=request.POST["textfield"]
    Gender=request.POST["radiobutton"]
    DOB=request.POST["textfield2"]
    Phone=request.POST["textfield3"]

    Adharnumber=request.POST["textfield5"]
    Email=request.POST["textfield6"]
    Basicpay=request.POST["textfield7"]
    if 'file' in request.FILES:
        Image = request.FILES["file"]
        fs = FileSystemStorage()
        fsave = fs.save(Image.name, Image)
        ob=Staff_table.objects.get(id=request.session['staffid'])
        ob.Fname=Name
        ob.Gender=Gender
        ob.DOB=DOB
        ob.Phone=Phone
        ob.image=fsave
        ob.Adharnumber=Adharnumber
        ob.Email=Email
        ob.Basicpay=Basicpay
        ob.save()
    else:
        ob = Staff_table.objects.get(id=request.session['staffid'])
        ob.Fname = Name
        ob.Gender = Gender
        ob.DOB = DOB
        ob.Phone = Phone
        ob.Adharnumber = Adharnumber
        ob.Email = Email
        ob.Basicpay = Basicpay
        ob.save()
    return redirect('/viewmanagestaff')





@login_required(login_url='/')
def assignworkstaff(request,id):
    ob=Assignwork_table.objects.filter(STAFFID__BRANCHID__LOGIN=request.session["lid"],Status="assigned")
    stafflist=[]
    for i in ob:
        if i.STAFFID.id in stafflist:
            pass
        else:
            stafflist.append(i.STAFFID.id)

    ob=Staff_table.objects.exclude(id__in=stafflist).filter(BRANCHID__LOGIN=request.session["lid"])
    request.session["bookid"]=id
    return render(request, 'Branch/assignworkstaff.html',{'val':ob})

@login_required(login_url='/')
def assign_post(request):
    bid=request.POST["select"]
    # Facility=request.POST["textfield2"]
    # Date=request.POST["textfield3"]
    # Status=request.POST["textfield4"]

    Booking_table.objects.filter(id=request.session["bookid"]).update(Status="Assigned")

    ob=Assignwork_table()
    ob.STAFFID_id=bid
    ob.BOOKINGID_id=request.session["bookid"]
    ob.Datetime=datetime.now()
    ob.Status="assigned"
    ob.save()
    return redirect('/viewaccapprovebooking')

@login_required(login_url='/')
def adssign(request):
     return render(request,'Branch/Assignwork.html')

@login_required(login_url='/')
def adssigned(request):

    ob=Bookingdetails_table.objects.filter(FACILITYID__BRANCHID__LOGIN__id=request.session['lid'])
    fid=[]
    for i in ob:
        if i.BOOKINGID.id in fid:
            pass
        else:
            fid.append(i.BOOKINGID.id)

    ob2=Assignwork_table.objects.filter(BOOKINGID__id__in=fid,BOOKINGID__Status="Assigned")

    return render(request,'Branch/work.html',{"val":ob2})


@login_required(login_url='/')
def moredetailssearch(request):
    date = request.POST['textfield']
    # ob = Booking_table.objects.filter(date__isexact=date).order_by('-id')
    ob = Bookingdetails_table.objects.filter(FACILITYID__BRANCHID__LOGIN__id=request.session['lid'])
    fid = []
    for i in ob:
        if i.BOOKINGID.id in fid:
            pass
        else:
            fid.append(i.BOOKINGID.id)

    ob2 = Assignwork_table.objects.filter(BOOKINGID__id__in=fid, BOOKINGID__Status="Assigned",BOOKINGID__book_date__exact=date)

    return render(request, 'Branch/work.html', {"val": ob2})


@login_required(login_url='/')
def branchhome(request):
        return render(request, 'Branch/branchindex1.html')


@login_required(login_url='/')
def rental_booking(request):
    # ob=Rentalbooking_table.objects.filter(BRANCHID__LOGINID=request.session['lid'])
    #
    # print(ob)



    ob = Rentalbookingdetails_table.objects.filter(RENTALPRODUCTID__BRANCHID__LOGIN__id=request.session['lid']).order_by('-id')
    fid = []
    for i in ob:
        if i.RENTALBOOKING.id in fid:
            pass
        else:
            fid.append(i.RENTALBOOKING.id)

    # ob2 = Rentalbooking_table.objects.filter(~Q(Status="cart"),id__in=fid)
    ob2 = Rentalbooking_table.objects.filter(Status="paid",id__in=fid)


    return render(request, 'Branch/rental_bookings.html',{'val':ob2})

@login_required(login_url='/')
def rental_booking_more(request,id):
    request.session["rental_book_id"]=id
    ob=Rentalbookingdetails_table.objects.filter(RENTALBOOKING=id)

    print(ob)

    data = []
    for i in ob:
        row = {"id": i.id, "product": i.RENTALPRODUCTID.Product, "desc": i.RENTALPRODUCTID.Description,
               "img": str(i.RENTALPRODUCTID.Image.url), "price": str(i.RENTALPRODUCTID.price * i.quantity),
               "qty": i.quantity,"Statis":i.Status}
        data.append(row)


    return render(request, 'Branch/Rental_booking_more.html',{"val":data})



@login_required(login_url='/')
def rental_returned_more(request,id):
    request.session["rental_book_id"]=id
    ob=Rentalbookingdetails_table.objects.filter(RENTALBOOKING=id)

    print(ob)

    data = []
    for i in ob:
        row = {"id": i.id, "product": i.RENTALPRODUCTID.Product, "desc": i.RENTALPRODUCTID.Description,
               "img": str(i.RENTALPRODUCTID.Image.url), "price": str(i.RENTALPRODUCTID.price * i.quantity),
               "qty": i.quantity,"Statis":i.Status}
        data.append(row)


    return render(request, 'Branch/retured_rental_more.html',{"val":data})



@login_required(login_url='/')
def rental_booking_return(request,id):
    ob=Rentalbookingdetails_table.objects.filter(~Q(Status="return"),RENTALBOOKING=request.session["rental_book_id"]).order_by('-id')
    if len(ob)>1:
        x=Rentalbookingdetails_table.objects.get(id=id)
        x.Status="return"
        x.save()

    elif len(ob)==1:
        x = Rentalbookingdetails_table.objects.get(id=id)
        x.Status = "return"
        x.save()

        x1=Rentalbooking_table.objects.get(id=request.session["rental_book_id"])
        x1.Status="return"
        x1.save()

    # ob=Rentalbookingdetails_table.objects.filter(RENTALBOOKING=id)
    # return render(request, 'Branch/Rental_booking_more.html',{"val":ob})
    return rental_booking_more(request,request.session["rental_book_id"])

@login_required(login_url='/')
def view_returned_rental(request):
    ob = Rentalbookingdetails_table.objects.filter(
        RENTALPRODUCTID__BRANCHID__LOGIN__id=request.session['lid']).order_by('-id')
    fid = []
    for i in ob:
        if i.RENTALBOOKING.id in fid:
            pass
        else:
            fid.append(i.RENTALBOOKING.id)

    # ob2 = Rentalbooking_table.objects.filter(~Q(Status="cart"),id__in=fid)
    ob2 = Rentalbooking_table.objects.filter(Status="return", id__in=fid)

    # return render(request, 'Branch/rental_bookings.html', {'val': ob2})

    return render(request,'Branch/view_returened_rental.html',{'val':ob2})


@login_required(login_url='/')
def managecosmetics(request):
        return render(request, 'Branch/managecosmetics.html')
@login_required(login_url='/')
def addstaffattendance(request):
        return render(request, 'Branch/addstaffattendance.html')
@login_required(login_url='/')
def managestaffattendance(request):
    # ob=Attendance_table.objects.all()

    return render(request, 'Branch/managestaffattendance.html')
@login_required(login_url='/')
def managestaffattendance_post(request):
    date=request.POST["textfield"]

    st = Staff_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])
    data=[]
    for i in st:
        i2 = Attendance_table.objects.filter(STAFFID=i, Date__exact=date,)
        if len(i2)>0:
            row = {"id": i2[0].id, "fname":  i2[0].STAFFID.Fname, "lname": i2[0].STAFFID.Lname, "gender": i2[0].STAFFID.Gender, "dob": i2[0].STAFFID.DOB,
                   "phone": i2[0].STAFFID.Phone, "email": i2[0].STAFFID.Email, "image": i2[0].STAFFID.image, "pay": i2[0].STAFFID.Basicpay, "adhar": i2[0].STAFFID.Adharnumber,"attendance":"present"}
        else:
            row = {"id": i.id, "fname": i.Fname, "lname": i.Lname,
                   "gender": i.Gender, "dob": i.DOB,
                   "phone": i.Phone, "email": i.Email, "image": i.image,
                   "pay": i.Basicpay, "adhar": i.Adharnumber, "attendance": "absnet"}

        data.append(row)
    return render(request, 'Branch/managestaffattendance.html',{"data":data})


@login_required(login_url='/')
def deleteattendance(request,id):
    ob=Attendance_table.objects.get(id=id)
    ob.delete()

    return redirect('/managestaffattendance')


@login_required(login_url='/')
def salarycalculation(request):
    return render(request,'Branch/salarycalculation.html')
@login_required(login_url='/')
def generatebill(request):
    return render(request,'Branch/generatebill.html')
@login_required(login_url='/')
def viewfeedbacks(request):
    ob=Feedbacktobranch_table.objects.filter(BRANCHID__LOGIN=request.session["lid"]).order_by('-id')
    return render(request, 'Branch/viewfeedback.html',{"val":ob})



@login_required(login_url='/')
def viewapprovebooking(request):
    # obb=Facility_table.objects.filter(BRANCHID__LOGIN__id=request.session['lid'])


    ob=Bookingdetails_table.objects.filter(FACILITYID__BRANCHID__LOGIN__id=request.session['lid']).order_by('-id')
    fid=[]
    for i in ob:
        if i.BOOKINGID.id in fid:
            pass
        else:
            fid.append(i.BOOKINGID.id)

    ob2=Booking_table.objects.filter(id__in=fid,Status="booked")



    return render(request, 'Branch/viewapprovebooking.html',{"val":ob2})
@login_required(login_url='/')
def viewaccapprovebooking(request):
    ob = Bookingdetails_table.objects.filter(FACILITYID__BRANCHID__LOGIN__id=request.session['lid']).order_by('-id')
    fid = []
    for i in ob:
        if i.BOOKINGID.id in fid:
            pass
        else:
            fid.append(i.BOOKINGID.id)

    ob2 = Booking_table.objects.filter(id__in=fid, Status="accpted")

    return render(request, 'Branch/viewacceptedbooking.html',{"val":ob2})


@login_required(login_url='/')
def acceptbookings(request,id):
    ob = Booking_table.objects.get(id=id)
    ob.Status="accpted"
    ob.save()
    return redirect('/viewapprovebooking')
    # return redirect('/viewaccapprovebooking')
@login_required(login_url='/')
def rejectbookings(request,id):
    ob = Booking_table.objects.get(id=id)
    ob.Status="rejected"
    ob.save()
    return redirect('/viewapprovebooking')
    # return redirect('/viewaccapprovebooking')
@login_required(login_url='/')
def moredetails_one(request,id):
    ob = Bookingdetails_table.objects.filter(BOOKINGID=id)
    return render(request, 'Branch/moredetails_one.html',{"val":ob})

@login_required(login_url='/')
def moredetails(request,id):
    ob = Bookingdetails_table.objects.filter(BOOKINGID=id)
    return render(request, 'Branch/moredetails.html',{"val":ob})


def acceptfacility(request,id):
    ob=Bookingdetails_table.objects.get(id=id)
    ob.status='accept'
    ob.save()
    return HttpResponse('''<script>alert("Accepted");window.location='/viewapprovebooking'</script>''')
def rejecttfacility(request,id):
    ob=Bookingdetails_table.objects.get(id=id)
    ob.status='reject'
    ob.save()
    return HttpResponse('''<script>alert("Rejected");window.location='/viewapprovebooking'</script>''')



@login_required(login_url='/')
def cosmeticsearch(request):
    Name = request.POST['textfield']
    ob = Cosmeticproduct.objects.filter(Product=Name)
    return render(request, 'Admin/viewcosmeticproduct.html', {"val": ob})



# def search_blind(request):
#     Name=request.POST['textfield']
#     ob=Blindspot_table.objects.filter(Name__contains=Name)







@login_required(login_url='/')
def addfacility(request):
    return render(request,'Branch/addfacility.html')
@login_required(login_url='/')
def addfacility_post(request):
    facilty=request.POST["textfield"]
    details=request.POST["textarea"]
    price=request.POST["textfield2"]
    image=request.FILES["file"]
    Time=request.POST["textfield3"]

    fs=FileSystemStorage()
    fsave=fs.save(image.name,image)


    ob=Facility_table()
    ob.Facility=facilty
    ob.Details=details
    ob.Price=price
    ob.Image=fsave
    ob.Time=Time
    ob.BRANCHID=Branch_table.objects.get(LOGIN=request.session["lid"])
    ob.save()
    return redirect('/viewmanagefacility')

@login_required(login_url='/')
def viewmanagefacility(request):
    ob=Facility_table.objects.filter(BRANCHID__LOGIN__id=request.session["lid"]).order_by('-id')
    return render(request, 'Branch/viewmanagefacility.html',{"data":ob})
@login_required(login_url='/')
def searchviewmanagefacility(request):
    fa=request.POST['textfield']
    ob=Facility_table.objects.filter(Facility__istartswith=fa,BRANCHID__LOGIN__id=request.session["lid"]).order_by('-id')
    return render(request, 'Branch/viewmanagefacility.html',{"data":ob})

@login_required(login_url='/')
def deletetfacility(request,id):
    ob=Facility_table.objects.get(id=id)
    ob.delete()
    return redirect('/viewmanagefacility')
@login_required(login_url='/')
def editfacility(request,id):
    request.session['facilityid'] = id
    ob = Facility_table.objects.get(id=id)
    return render(request, "Branch/editfacility.html", {'data': ob})
@login_required(login_url='/')
def editfacility_post(request):
    Facility=request.POST["textfield"]
    Details=request.POST["textarea"]
    Price=request.POST["textfield2"]


    if 'file' in request.FILES:
        Image=request.FILES["file"]
        fs=FileSystemStorage()
        fsave=fs.save(Image.name,Image)

        ob = Facility_table.objects.get(id=request.session['facilityid'])
        ob.Facility=Facility
        ob.Details=Details
        ob.Price=Price
        ob.Image=fsave
        ob.save()
    else:
        ob = Facility_table.objects.get(id=request.session['facilityid'])
        ob.Facility = Facility
        ob.Details = Details
        ob.Price = Price

        ob.save()

    return redirect('/viewmanagefacility')



@login_required(login_url='/')
def viewleavedetails(request):
    staff=Staff_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])
    ob=Leaverequest_table.objects.filter(STAFFID__BRANCHID__LOGIN=request.session["lid"]).order_by('-id')
    return render(request, 'Branch/viewleavedetails.html',{'val':ob,"staff":staff})
@login_required(login_url='/')
def acceptleave(request,id):
    ob = Leaverequest_table.objects.get(id=id)
    ob.Status="accepted"
    ob.save()
    return redirect('/viewleavedetails')
@login_required(login_url='/')
def reject_leave(request,id):
    ob = Leaverequest_table.objects.get(id=id)
    ob.Status="rejected"
    ob.save()
    return redirect('/viewleavedetails')


def searchleaverqst(request):
    bt=request.POST["bt"]
    print("00000000000",bt)
    if bt=="Search":
        sid=request.POST['select']
        ob=Leaverequest_table.objects.filter(STAFFID=sid).order_by('-id')
        staff = Staff_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])
        return render(request, 'Branch/viewleavedetails.html', {'val': ob, "staff": staff})
    elif bt=="go":
        fdate=request.POST['f1']
        tdate=request.POST['f2']

        print(fdate,tdate)
        ob=Leaverequest_table.objects.filter(Fromdate__range=(fdate,tdate)).order_by('-id')
        staff = Staff_table.objects.filter(BRANCHID__LOGIN=request.session["lid"])
        return render(request, 'Branch/viewleavedetails.html', {'val': ob, "staff": staff})


@login_required(login_url='/')
def Viewcustomers(request):
    # ob = Customer_table.objects.all()

    br=Branch_table.objects.all()

    return render(request, 'Admin/Viewcustomers.html',{"branch":br})
@login_required(login_url='/')
def searchcustomer(request):
    name=request.POST['branch']
    obb=Branch_table.objects.all()
    ob=Bookingdetails_table.objects.filter(FACILITYID__BRANCHID=name)
    orderlis=[]
    for i in ob:
        if i.BOOKINGID.id in orderlis:
            pass
        else:
            orderlis.append(i.BOOKINGID.id)

    cu=Booking_table.objects.filter(id__in=orderlis)

    return render(request,'Admin/Viewcustomers.html',{'val':cu,"branch":obb})


def insertAttendance(request):
    sid = request.GET["staffid"]
    # type = request.GET["type"]

    # print("---------",sid,type)
    import datetime

    ob=Attendance_table.objects.filter(STAFFID=sid,Date=datetime.datetime.now().date())
    print(ob,len(ob),"+++++++/++++")
    if len(ob)==0:
        ins=Attendance_table()
        ins.STAFFID_id=sid
        ins.Date=datetime.datetime.now()
        ins.Attendance="1"
        ins.save()
    else:
        pass

    return HttpResponse("ok")



#______________________________ANDROID SERVE
import json

def and_logincode(request):
    print(request.POST)
    un = request.POST['uname']
    pwd = request.POST['pswd']
    print(un, pwd)
    try:
        users = login_table.objects.get(Username=un,Password=pwd)
        print(users.Type,"ooooooooooooooooooooooo")

        if users is None:
            data = {"task": "invalid"}
        else:
            print(users.Type)
            print("in user function")
            data = {"task": "valid", "id": users.id,"type":users.Type}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)
    except Exception as e:
        print("----",e)
        data = {"task": "invalid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)

def and_staffviewassignedwork(request):
    lid=request.POST["lid"]
    ob=Assignwork_table.objects.filter(STAFFID__LOGIN__id=lid)
    data=[]
    for i in ob:
        row={"id":i.id,"ass_date":i.Datetime,"st":i.Status,"slot":i.BOOKINGID.Status,
             "cname":i.BOOKINGID.CUSTOMERID.Fname+" "+i.BOOKINGID.CUSTOMERID.Fname,"phone":i.BOOKINGID.CUSTOMERID.Phone}
        data.append(row)
    r=json.dumps(data)
    return HttpResponse(r)






#------------------------------------------cust
def and_viewbranches(request):

    ob=Branch_table.objects.all()
    data=[]
    for i in ob:
        row={"name":i.Name,"place":i.Place,"post":i.post,"pin":i.Pin,"phone":i.Phone,"lat":i.latitude,"long":i.longitude,"email":i.Email,"id":i.id}
        data.append(row)
    r = json.dumps(data)
    print("))))))))))))))))))))))))",r)
    return HttpResponse(r)



def and_viewfacilities(request):
    bid=request.POST["bid"]
    print(bid)
    ob=Facility_table.objects.filter(BRANCHID=bid)
    data=[]
    for i in ob:
        row={"facility":i.Facility,"details":i.Details,"price":i.Price,"img":i.Image.url,"time":str(i.Time),"id":i.id}
        data.append(row)

    r=json.dumps(data)
    print(r)
    return HttpResponse(r)

def and_viewfacilities_search(request):
    bid=request.POST["bid"]
    fname=request.POST["name"]
    ob=Facility_table.objects.filter(BRANCHID=bid,Facility__istartswith=fname)
    data=[]
    for i in ob:
        row={"facility":i.Facility,"details":i.Details,"price":i.Price,"img":i.Image.url,"time":str(i.Time),"id":i.id}
        data.append(row)

    r=json.dumps(data)
    print(r)
    return HttpResponse(r)


def and_viewrental(request):
    bid=request.POST["bid"]
    ob=Rentalproduct_table.objects.filter(BRANCHID=bid).order_by('-id')
    data=[]
    for i in ob:
        row={"product":i.Product,"description":i.Description,"image":str(i.Image.url),"price":i.price,"type":i.Type,"id":i.id,"quantity":i.quantity}
        data.append(row)

    r=json.dumps(data)
    print(r)
    return HttpResponse(r)

def and_viewrentalsearch(request):
    bid=request.POST["bid"]
    pname=request.POST["pname"]
    ob = Rentalproduct_table.objects.filter(BRANCHID=bid, Product__istartswith=pname)
    data=[]
    for i in ob:
        row={"product":i.Product,"description":i.Description,"image":str(i.Image.url),"price":i.price,"id":i.id}
        data.append(row)

    r=json.dumps(data)
    print(r)
    return HttpResponse(r)

from datetime import datetime, timedelta

def generate_time_slots(start_time, end_time, slot_duration):
    current_time = start_time
    slot=[]
    while current_time < end_time:
        slot.append(str(current_time).split(" ")[1][:5]+" to "+str(current_time+slot_duration).split(" ")[1][:6])
        current_time += slot_duration
    return (slot)



def registration(request):
    fname=request.POST["Fname"]
    lname=request.POST["Lname"]
    place=request.POST["place"]
    phone=request.POST["phone_number"]
    gender=request.POST["gender"]
    post=request.POST["post"]
    pin=request.POST["pin"]
    email=request.POST["email_id"]
    username=request.POST["username"]
    password=request.POST["password"]
    try:
        ob=login_table()
        ob.Username=username
        ob.Password=password
        ob.Type='user'
        ob.save()

        obb=Customer_table()
        obb.Fname=fname
        obb.Lname=lname
        obb.Gender=gender
        obb.Place=place
        obb.Post=post
        obb.Pin=pin
        obb.Phone=phone
        obb.Email=email
        obb.LOGINID=ob
        obb.save()
        return JsonResponse({"task":"ok"})
    except Exception as e:
        print(e)
def and_view_sloat(request):
    date=request.POST['date']
    pid=request.POST['facility']
    ob=Facility_table.objects.get(id=pid)

    time=ob.Time
    # sloatlist=[]

    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    slot_duration = timedelta(minutes=int(time))
    slt=generate_time_slots(start_time,end_time,slot_duration)

    # date_object = datetime.strptime(date, "%Y-%m-%d")


    data=[]
    for i in slt:
        r={"slot":i}
        print(i,pid)
        obb=Bookingdetails_table.objects.filter(FACILITYID__id=pid,Slot__exact=str(i),BOOKINGID__Date=date)
        print(obb)
        print("----"+i,len(obb),date)
        if len(obb)>0:
            r['s']="0"
        else:
            r['s']="1"
        data.append(r)
    print(data)
    return JsonResponse(data,safe=False)

def add_to_cart(request):
        import datetime
        print(request.POST, "=================================")
        pro_id = request.POST['facilityid']
        # slot = request.POST['slot']
        lid = request.POST['lid']
        # book_date=request.POST["booking_date"]

        print(pro_id, "PPPPPPPPPPPPPPPPPPPPPPP")
        # print(slot, "qqqqqqqqqqqqqqqqqqqqqqq")
        print(lid, "lllllllllllllllllllllllll")

        ob = Facility_table.objects.get(id=pro_id)
        tt = int(ob.Price)

        # obe1 = Bookingdetails_table()
        # obe1.BOOKINGID = obe
        # obe1.FACILITYID_id = pro_id
        # obe1.status = "pending"
        OBCKECK=Bookingdetails_table.objects.filter(FACILITYID__id = pro_id,BOOKINGID__CUSTOMERID__LOGINID__id=lid, BOOKINGID__Status='cart')
        if len(OBCKECK)>0:
            data = {"task": "valid"}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
        q = Booking_table.objects.filter(CUSTOMERID__LOGINID__id=lid, Status='cart')
        if len(q) == 0:

            obe = Booking_table()
            obe.Status = 'cart'
            obe.Date = datetime.datetime.now().strftime("%Y-%m-%d")
            obe.Time = datetime.datetime.now().strftime("%H:%M")
            obe.total=tt

            obe.CUSTOMERID = Customer_table.objects.get(LOGINID__id=lid)
            obe.save()
            obf = Offer_table.objects.filter(FACILITYID=pro_id, Fromdate__lte=datetime.datetime.today(),
                                             Todate__gte=datetime.datetime.today())
            print(obf, "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            obe1 = Bookingdetails_table()
            obe1.BOOKINGID = obe
            obe1.FACILITYID_id = pro_id
            obe1.status = "pending"
            if len(obf) > 0:
                obe1.offer_id = obf[0].id
                tt = tt - (tt * float(obf[0].Percentage) / 100)
                obe.total = tt
                print("ooooooooooooooooooooooooo")
                obe.save()
            else:
                obe1.offer_id = ""

            obe1.save()
            data = {"task": "valid"}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
        else:
            total = int(ob.Price) + int(tt)
            print(total, "KKKKKKKKKKKKKKKK")

            obr = Booking_table.objects.get(id=q[0].id)
            # obr. total= total
            obr.Status = 'cart'
            obr.save()
            obr1 = Bookingdetails_table()
            obr1.BOOKINGID = obr
            obr1.FACILITYID = ob
            obr1.status = "pending"
            # obr1.Slot = slot
            obf = Offer_table.objects.filter(FACILITYID__id=ob.id, Fromdate__lte=datetime.datetime.today(),
                                             Todate__gte=datetime.datetime.today())
            print(obf, "+++++++++++=============")
            if len(obf) > 0:
                obr1.offer_id = obf[0].id
                tt = tt - (tt * float(obf[0].Percentage) / 100)
                total = int(obr.total) + int(tt)
                obr.total = total

                obr.save()
            else:

                total = int(obr.total) + int(tt)
                print(total, "===========+++++++++++")
                obr.total = total

                obr.save()
            obr1.save()
            data = {"task": "valid", "tt": str(tt)}

            r = json.dumps(data)
            print(r)
            return HttpResponse(r)

        data = {"task": "valid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)

def view_cart(request):
    lid = request.POST["lid"]
    print(request.POST)
    ob = Bookingdetails_table.objects.filter(BOOKINGID__CUSTOMERID__LOGINID__id=lid,BOOKINGID__Status="cart")
    data = []
    for i in ob:
        try:



            row = {"facility": i.FACILITYID.Facility, "facilityimage": str(i.FACILITYID.Image.url), "slot":str(i.FACILITYID.Price)  ,
                   "offer": i.offer.Percentage, "id": i.id}
            data.append(row)
        except:
            row = {"facility": i.FACILITYID.Facility, "facilityimage": str(i.FACILITYID.Image.url), "slot":str(i.FACILITYID.Price),
                   "offer": "No Offer", "id": i.id}
            data.append(row)
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)
def delete_cart(request):
    bild=request.POST["bild"]
    ob=Bookingdetails_table.objects.get(id=bild).delete()
    data = {"task": "valid"}

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)

def Purchase_cart(request):
    lid=request.POST["lid"]
    bookdate=request.POST["bookdate"]
    slottime=request.POST["slottime"]

    ob=Booking_table.objects.filter(Status='cart',CUSTOMERID__LOGINID=lid)

    if len(ob)>0:
        xx=Booking_table.objects.filter(book_date__exact=bookdate,slot_time=slottime)

        print(xx,"---------------")
        if len(xx)>3:
            data = {"task": "exist"}

            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
        else:

            obb=Booking_table.objects.get(id=ob[0].id)
            obb.book_date=bookdate
            obb.slot_time=slottime
            obb.Status="booked"
            obb.save()
            data = {"task": "valid"}

            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
    else:
        data = {"task": "invalid"}

        r = json.dumps(data)
        print(r)
        return HttpResponse(r)


def and_staffrequestsend(request):
    Reason=request.POST["rsn"]
    Fromdate=request.POST["frmd"]
    Noofdays=request.POST["nody"]
    stafflid=request.POST["lid"]

    print(stafflid)
    ob =Leaverequest_table()
    ob.Reason=Reason
    ob.Fromdate=Fromdate
    ob.Numofdays=Noofdays
    ob.STAFFID=Staff_table.objects.get(LOGIN=stafflid)
    ob.Date=datetime.today()
    ob.Status="pending"
    ob.save()
    data = {"task": "valid"}

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)
def and_view_leavereqsr(request):

    lid=request.POST["lid"]
    ob = Leaverequest_table.objects.filter(STAFFID__LOGIN__id=lid)
    print(ob)
    data = []
    for i in ob:
        row = {"reason": i.Reason, "fromdaste":str(i.Fromdate), "noofdays":i.Numofdays, "id": i.id}
        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)
def delete_leave(request):
    rlid=request.POST["leid"]
    ob=Leaverequest_table.objects.get(id=rlid).delete()
    data = {"task": "valid"}

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)
def and_viewbookings(request):
    lid=request.POST["lid"]
    print(lid)
    ob=Booking_table.objects.filter(CUSTOMERID__LOGINID=lid)


    data = []
    for i in ob:
        print("mmmm",i.id)

        if i.Status=="Assigned":
            xx=Assignwork_table.objects.get(BOOKINGID=i.id)

            row = {"id": i.id, "date": str(i.Date), "time":str(i.Time),"bookdate": str(i.book_date),  "slot": i.slot_time,"status":i.Status,"total":i.total,"assignstaff":xx.STAFFID.Fname}
        else:
            row = {"id": i.id, "date": str(i.Date), "time": str(i.Time), "bookdate": str(i.book_date),
                   "slot": i.slot_time, "status": i.Status, "total": i.total, "assignstaff": "No"}

        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def and_viewbooking_more(request):
    bid=request.POST['bid']
    ob=Bookingdetails_table.objects.filter(BOOKINGID=bid)
    data=[]
    for i in ob:
        row = {"facility": i.FACILITYID.Facility, "details": i.FACILITYID.Details, "price": i.FACILITYID.Price, "time": str(i.FACILITYID.Time),"image":str(i.FACILITYID.Image.url),"id":i.id}

        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def and_view_attendance_and_slary(request):
    # Example usage
    year = int(request.POST["year"])
    month = request.POST["month"]  # March
    lid = request.POST["lid"]  # March
    totalworking = request.POST["totalworking"]  # March
    mon=0
    if month=="January":
        mon=1
    elif month=="February":
        mon=2
    elif month == "March":
        mon = 3
    elif month == "April":
        mon = 4
    elif month == "May":
        mon = 5
    elif month == "June":
        mon = 6
    elif month == "July":
        mon = 7
    elif month == "August":
        mon = 8
    elif month == "September":
        mon = 9
    elif month == "October":
        mon = 10
    elif month == "November":
        mon = 11
    else :
        mon = 12

    year =year
    month = mon
    dates = get_dates(year, month)
    print("Dates in March 2024:")
    data=[]
    atten=[]
    for date in dates:
        print(date)

        ob=Attendance_table.objects.filter(STAFFID__LOGIN=lid,Date__exact=date)
        if len(ob)>0:
            atten.append("P")
            row={"Date":date,"Attendance":"present"}
        else:
            st=datetime.strptime(date, "%Y-%m-%d")
            if st > datetime.today():
                atten.append("W")
                row = {"Date": date, "Attendance": "Waiting"}
            else:
                atten.append("A")
                row = {"Date": date, "Attendance": "absent"}
        data.append(row)

    # total = len(atten)
    total = int(totalworking)
    present = atten.count("P")
    sa=Staff_table.objects.get(LOGIN=lid)

    basicpay=sa.Basicpay
    persc = round((present / total) * 100)
    amnt = round((persc * basicpay) / 100)

    print("total",total)
    print("attt",atten)
    print("=============",basicpay)
    print("=============",persc)
    print("=============",amnt,"%")
    # subj.append(persc)
    x={"salary":str(amnt)+".00","totalworking":totalworking,"Present":present,"percen":str(persc)+"%"}

    r = json.dumps(x)
    # print(r)
    return HttpResponse(r)

def and_view_attendance(request):
    # Example usage
    year = int(request.POST["year"])
    month = request.POST["month"]  # March
    lid = request.POST["lid"]  # March
    mon=0
    if month=="January":
        mon=1
    elif month=="February":
        mon=2
    elif month == "March":
        mon = 3
    elif month == "April":
        mon = 4
    elif month == "May":
        mon = 5
    elif month == "June":
        mon = 6
    elif month == "July":
        mon = 7
    elif month == "August":
        mon = 8
    elif month == "September":
        mon = 9
    elif month == "October":
        mon = 10
    elif month == "November":
        mon = 11
    else :
        mon = 12

    year =year
    month = mon
    dates = get_dates(year, month)
    print("Dates in March 2024:")
    data=[]
    for date in dates:
        print(date)

        ob=Attendance_table.objects.filter(STAFFID__LOGIN=lid,Date__exact=date)
        if len(ob)>0:
            row={"Date":date,"Attendance":"present"}
        else:
            st=datetime.strptime(date, "%Y-%m-%d")
            if st > datetime.today():
                row = {"Date": date, "Attendance": "Waiting"}
            else:
                row = {"Date": date, "Attendance": "absent"}
        data.append(row)


    r = json.dumps(data)
    print(r)
    return HttpResponse(r)
import calendar

def get_dates(year, month):
    _, num_days = calendar.monthrange(year, month)
    dates = [f"{year}-{month:02d}-{day:02d}" for day in range(1, num_days + 1)]
    return dates




def and_view_works(request):
    lid=request.POST["lid"]

    ob=Assignwork_table.objects.filter(STAFFID__LOGIN=lid)
    data = []
    for i in ob:
        row ={"bookdate":str(i.BOOKINGID.book_date),"slottime":str(i.BOOKINGID.slot_time),"sts":i.Status,"total":i.BOOKINGID.total,"id":i.id,"bid":i.BOOKINGID.id}

        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)

def and_update_work(request):
    assid=request.POST["assid"]
    ob=Assignwork_table.objects.get(id=assid)

    Booking_table.objects.filter(id=ob.BOOKINGID.id).update(Status="completed")

    ob.Status="completed"
    ob.save()

    data={"task":"valid"}
    r=json.dumps(data)
    return HttpResponse(r)
def Rental_add_to_cart(request):
    print(request.POST,"=================================")
    pro_id = request.POST['pro_id']
    qty = request.POST['qty']
    lid = request.POST['lid']
    print(pro_id, "PPPPPPPPPPPPPPPPPPPPPPP")
    # print(qty, "qqqqqqqqqqqqqqqqqqqqqqq")
    print(lid, "lllllllllllllllllllllllll")

    ob = Rentalproduct_table.objects.get(id=pro_id)
    tt = int(ob.price) * int(qty)
    print(tt,"price=====================tt========")
    stock = ob.quantity
    print(stock, "SSSSSSSSSSSSSSSSSSSSSSSSS")
    nstk = int(stock) - int(qty)
    print(nstk, "OOOOOOOOOOOOOOOOOOOO")
    if int(stock) >= int(qty):
        up = Rentalproduct_table.objects.get(id=pro_id)
        up.quantity = nstk
        up.save()
        q = Rentalbooking_table.objects.filter(CUSTOMERID__LOGINID__id=lid, Status='cart')
        if len(q) == 0:

            obe = Rentalbooking_table()
            obe.Total = tt
            obe.Status = 'cart'
            # obe.Date = datetime.datetime.now().strftime("%Y-%m-%d")
            obe.Date = datetime.now().date()

            obe.CUSTOMERID = Customer_table.objects.get(LOGINID__id=lid)
            obe.save()
            # obf = Offer.objects.filter(PRODUCT__id=up.id, fromdate__lte=datetime.datetime.today(),
            #                            todate__gte=datetime.datetime.today())
            # print(obf,"IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            obe1 = Rentalbookingdetails_table()
            obe1.RENTALBOOKING = obe
            obe1.Status = 'order'
            obe1.RENTALPRODUCTID = ob
            obe1.quantity=qty
            # if len(obf)>0:
            #     obe1.OFFER = obf[0].offer
            #     tt=tt-(tt*float(obf[0].offer)/100)
            #     obe.total = tt
            #     print("ooooooooooooooooooooooooo")
            #     obe.save()
            # else:
            #     obe1.OFFER = '0'

            obe1.save()
            data = {"task": "valid"}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
        else:
            total = int(q[0].Total) + int(tt)
            print(total, "KKKKKKKKKKKKKKKK")

            obr = Rentalbooking_table.objects.get(id=q[0].id)
            obr. Total= total
            obr.Status = 'cart'
            obr.save()

            obr1 = Rentalbookingdetails_table()
            obr1.quantity = qty
            obr1.RENTALBOOKING = obr
            obr1.RENTALPRODUCTID = ob
            obr1.Status='cart'
            # obf = Offer.objects.filter(PRODUCT__id=up.id, fromdate__lte=datetime.datetime.today(),
            #                            todate__gte=datetime.datetime.today())
            # print(obf,"+++++++++++=============")
            # if len(obf) > 0:
            #     obr1.OFFER = obf[0].offer
            #     tt = tt - (tt * float(obf[0].offer) / 100)
            #     total = int(obr.total) + int(tt)
            #     obr.total = total
            #
            #     obr.save()
            # else:
            #     obr1.OFFER = '0'
            #     total = int(obr.total) + int(tt)
            #     print(total,"===========+++++++++++")
            #     obr.total = total
            #
            #     obr.save()
            obr1.save()
            data = {"task": "valid","tt":str(tt)}

            r = json.dumps(data)
            print(r)
            return HttpResponse(r)

        data = {"task": "valid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)
    else:
        data = {"task": "out of stock"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)



def view_rental_cart(request):
   lid=request.POST["lid"]
   print(lid)
   ob=Rentalbookingdetails_table.objects.filter(RENTALBOOKING__CUSTOMERID__LOGINID=lid,RENTALBOOKING__Status="cart")
   print(ob)
   data = []

   for i in ob:
       row = { "product": i.RENTALPRODUCTID.Product,"desc":i.RENTALPRODUCTID.Description, "image": str(i.RENTALPRODUCTID.Image.url),"price":str(int(i.RENTALPRODUCTID.price)*int(i.quantity)),"type":i.RENTALPRODUCTID.Type,"id":i.id,"quantity":i.quantity}
       data.append(row)

   r = json.dumps(data)
   print(r)
   return HttpResponse(r)

def view_order_data(request):
    lid=request.POST["lid"]
    od=Rentalbooking_table.objects.get(CUSTOMERID__LOGINID=lid,Status="Cart")
    data = {"task": "valid","oid":od.id}

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def delete_rental(request):
    rlid=request.POST["bild"]
    ob=Rentalbookingdetails_table.objects.get(id=rlid)

    ob2=Rentalbooking_table.objects.get(id=ob.RENTALBOOKING.id)

    ob2.Total=ob2.Total-(ob.quantity*ob.RENTALPRODUCTID.price)
    ob2.save()

    ob.delete()




    data = {"task": "valid"}

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)
def paymentfinish(request):
    oid=request.POST["bid"]
    # lid=request.POST["lid"]
    amount=request.POST["amt"]

    ob1=Rentalbooking_table.objects.filter(id=oid).update(Status="paid")
    ob2=Rentalbookingdetails_table.objects.filter(RENTALPRODUCTID=oid).update(Status="paid")


    ob=payment_table()
    ob.oid_id=oid
    ob.amount=amount
    ob.date=datetime.now().date()
    ob.save()
    data = {"task": "success"}

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)






def sendfeedback(request):
    Feedback=request.POST['feedback']
    Rating=request.POST['rating']
    uid = request.POST["lid"]

    complaint_obj = Feedbacktoapp_table()
    complaint_obj.CUSTOMERID = Customer_table.objects.get(LOGINID__id=uid)
    complaint_obj.Feedback = Feedback
    complaint_obj.Rating = Rating
    complaint_obj.Date=datetime.today()
    complaint_obj.save()
    data = {'task': 'success'}
    r = json.dumps(data)
    return HttpResponse(r)
def sendfeedbackbrnch(request):
    Feedback=request.POST['feedback']
    Rating=request.POST['rating']
    uid = request.POST["lid"]
    bid = request.POST["branchid"]

    complaint_obj = Feedbacktobranch_table()
    complaint_obj.CUSTOMERID = Customer_table.objects.get(LOGINID__id=uid)
    complaint_obj.BRANCHID = Branch_table.objects.get(id=bid)
    complaint_obj.Feedback = Feedback
    complaint_obj.Rating = Rating
    complaint_obj.Date=datetime.today()
    complaint_obj.save()
    data = {'task': 'success'}
    r = json.dumps(data)
    return HttpResponse(r)

def and_view_feedback(request):
    ob = Feedbacktoapp_table.objects.all()
    print(ob)
    data = []
    for i in ob:
        row = {"name":i.CUSTOMERID.Fname+i.CUSTOMERID.Lname,"feedback": i.Feedback, "rating":i.Rating, "date":str(i.Date)}
        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def view_reply(request):
    Lid=request.POST['lid']
    ob = Complaint_table.objects.filter(CUSTOMERID__LOGINID__id=Lid)
    data = []
    for i in ob:
        row = {"complaints": i.Complaint,"date": str(i.Date), "reply": i.Reply}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)



def send_complaints(request):
    complaint=request.POST['complaint']
    id=request.POST['lid']
    comp_ob = Complaint_table()
    comp_ob.Complaint=complaint
    comp_ob.Date= datetime.now()
    comp_ob.Reply='pending'
    comp_ob.CUSTOMERID=Customer_table.objects.get(LOGINID=id)
    comp_ob.save()
    data = {"task": "success"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)



def and_view_offer(request):

    ob = Offer_table.objects.all()
    print(ob)
    data = []
    for i in ob:
        row = {"facility":i.FACILITYID.Facility,"offer": i.Percentage, "fromdate":str(i.Fromdate), "todate":str(i.Todate)}
        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)



def viewhistory1(request):
    lid=request.POST['lid']
    ob = Rentalbookingdetails_table.objects.filter(RENTALBOOKING__CUSTOMERID__LOGINID__id=lid)
    a=[]
    for i in ob:
        a.append(i.id)
    obb=Rentalbookingdetails_table.objects.filter(RENTALBOOKING_id__in=a)
    p_ob= payment_table.objects.get(oid__id=ob.id)
    print(p_ob,'%%%%%%%%%%%%')
    data = []

    for i in obb:
        row = {"product":i.RENTALPRODUCTID.Product,"description": i.RENTALPRODUCTID.Description, "image":str(i.RENTALPRODUCTID.Image.url), "price":i.RENTALPRODUCTID.price,"date":str(i.RENTALBOOKING.Date),"fromdate":str(i.RENTALBOOKING.Fromdate),"todate":str(i.RENTALBOOKING.Todate),"payment": p_ob.amount }
        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)



def viewhistory(request):
    uid=request.POST['lid']
    ob=Rentalbookingdetails_table.objects.filter(RENTALBOOKING__CUSTOMERID__LOGINID__id=uid).exclude(RENTALBOOKING__Status='cart')
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    total=0
    tt=0
    for i in ob:
        # obf = Offer.objects.filter(PRODUCT__id=i.PRODUCT.id, fromdate__lte=datetime.datetime.today(),
        #                            todate__gte=datetime.datetime.today())
        # print(obf, "+++++++++++=============")
        # tt1=int(i.quantity) * int(i.PRODUCT.price)
        # if len(obf) > 0:
        #     i.OFFER = obf[0].offer
        #     tt1 = tt1- (tt1 * float(obf[0].offer) / 100)
        #     print(tt1,")000000000000000")
        #     total = (int(i.quantity) * int(i.PRODUCT.price)) - int(tt1)
        # else:
        #     i.OFFER = '0'
        #     total = int(i.quantity) * int(i.PRODUCT.price)
        data = {"product":i.RENTALPRODUCTID.Product,"description": i.RENTALPRODUCTID.Description, "image":str(i.RENTALPRODUCTID.Image.url), "price":i.RENTALPRODUCTID.price,"date":str(i.RENTALBOOKING.Date),"fromdate":str(i.RENTALBOOKING.Fromdate),"todate":str(i.RENTALBOOKING.Todate) }

        # data={'shop':i.PRODUCT.SHOP.shopname,'product':i.PRODUCT.name,'status':i.status,'date': str(i.ORDERDETAILS.date),'total':total}
        mdata.append(data)
        print(mdata)
    r=json.dumps(mdata)
    return HttpResponse(r)



def delete_pet(request):
    pet=request.POST['id']
    print("$$$$$$$$$",pet)
    ob=Booking_table.objects.get(id=pet)
    ob.delete()
    data = {'task': 'valid'}
    r = json.dumps(data)
    return HttpResponse(r)




def add_to_cart1(request):
        print(request.POST, "=================================")
        pro_id = request.POST['pro_id']
        qty = request.POST['quantity']
        lid = request.POST['lid']
        print(pro_id, "PPPPPPPPPPPPPPPPPPPPPPP")
        print(qty, "qqqqqqqqqqqqqqqqqqqqqqq")
        print(lid, "lllllllllllllllllllllllll")

        ob = Rentalproduct_table.objects.get(id=pro_id)
        tt = int(ob.price) * int(qty)
        print(tt, "price=====================tt========")
        stock = ob.quantity
        print(stock, "SSSSSSSSSSSSSSSSSSSSSSSSS")
        nstk = int(stock) - int(qty)
        print(nstk, "OOOOOOOOOOOOOOOOOOOO")
        if stock >= qty:
            up = Rentalproduct_table.objects.get(id=pro_id)
            up.stock = nstk
            up.save()

            q = Rentalbooking_table.objects.filter(CUSTOMERID__LOGINID__id=lid, Status='cart')
            if len(q) == 0:

                obe = Rentalbooking_table()
                obe.Total = tt
                obe.Status = 'cart'
                obe.Date = datetime.now().strftime("%Y-%m-%d")

                obe.CUSTOMERID = Customer_table.objects.get(LOGINID__id=lid)
                obe.save()
                # obf = Offer.objects.filter(PRODUCT__id=up.id, fromdate__lte=datetime.datetime.today(),
                #                            todate__gte=datetime.datetime.today())
                obe1 = Rentalbookingdetails_table()
                obe1.RENTALBOOKING = obe
                obe1.Status = 'order'
                obe1.RENTALPRODUCTID = up
                # if len(obf) > 0:
                #     obe1.OFFER = obf[0].offer
                #     tt = tt - (tt * float(obf[0].offer) / 100)
                #     obe.total = tt
                #
                #     obe.save()
                # else:
                #     obe1.OFFER = '0'

                obe1.save()
                data = {"task": "valid"}
                r = json.dumps(data)
                print(r)
                return HttpResponse(r)



            else:
                total = int(ob.price) + int(tt)
                print(total, "KKKKKKKKKKKKKKKK")

                obr = Rentalbooking_table.objects.get(id=q[0].id)
                # obr. total= total
                # obr.status = 'cart'
                # obr.save()
                obr1 = Rentalbookingdetails_table()
                obr1.RENTALBOOKING = obr
                obr1.RENTALPRODUCTID = up
                # obf = Offer.objects.filter(PRODUCT__id=up.id, fromdate__lte=datetime.datetime.today(),
                #                            todate__gte=datetime.datetime.today())
                # print(obf, "+++++++++++=============")
                # if len(obf) > 0:
                #     obr1.OFFER = obf[0].offer
                #     tt = tt - (tt * float(obf[0].offer) / 100)
                #     total = int(obr.total) + int(tt)
                #     obr.total = total
                #
                #     obr.save()
                # else:
                #     obr1.OFFER = '0'
                #     total = int(obr.total) + int(tt)
                #     print(total, "===========+++++++++++")
                #     obr.total = total
                #
                #     obr.save()
                obr1.save()
                data = {"task": "valid"}

                r = json.dumps(data)
                print(r)
                return HttpResponse(r)

            data = {"task": "valid"}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)



        else:
            data = {"task": "out of stock"}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
def  and_view_rental_booking(request):
    lid=request.POST["lid"]
    ob=Rentalbooking_table.objects.filter(CUSTOMERID__LOGINID=lid).order_by('-id')
    data =[]
    for i in ob:
        row = {"date":str( i.Date), "status": i.Status,
               "frmdate":str(i.Fromdate), "todate":str(i.Todate) ,
               "total": str(i.Total),"id":i.id}
        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def and_rental_booking_more(request):
    bid=request.POST["bid"]
    ob=Rentalbookingdetails_table.objects.filter(RENTALBOOKING=bid)
    data=[]
    for i in ob:
        row = {"id":i.id,"product":i.RENTALPRODUCTID.Product,"desc": i.RENTALPRODUCTID.Description,"img":str(i.RENTALPRODUCTID.Image.url), "price":str(i.RENTALPRODUCTID.price*i.quantity) ,
               "qty": i.quantity}
        data.append(row)

    r = json.dumps(data)
    print(r)
    return HttpResponse(r)




