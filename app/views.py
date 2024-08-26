from django.shortcuts import render,redirect
from . forms import ProfileForm,ExtendedForm,ExtendedUpdateForm,ProfileUpdateForm,ConsentDocumentForm
from django.contrib.auth.models import User
from . models import ConsentDocument,ConsentStatus,Profile
from django.contrib import messages
import datetime
from django.utils import timezone
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('log')
    else:
        return render(request,'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('log')
    else:
        if request.method =='POST':
            email = request.POST['email']
            form = ExtendedForm(request.POST)
            user_profile = ProfileForm(request.POST,request.FILES)
            if form.is_valid() and user_profile.is_valid():
                try:
                    user = form.save()
                    profile = user_profile.save(commit=False)
                    profile.user = user
                    profile.save()
                    return redirect('/')
                except:
                    messages.info(request,'invalid mail')
                    return redirect('signup')
            else:
                messages.info(request,'invalid details')
                return redirect('signup')
        else:
            form = ExtendedForm()
            user_profile = ProfileForm()
            return render(request,'register.html',{'form':form,'form1':user_profile})
    
def log(request):
    if request.user.is_authenticated:
        status= ConsentStatus.objects.filter(user=request.user)
        alldoccount= ConsentDocument.objects.count()
        lastdoc=ConsentDocument.objects.latest('id')
        lastdocuserscnt= ConsentStatus.objects.filter(document=lastdoc).count()
        pending_count,signed_count,declined_count=0,0,0
        for i in status:
            if i.status=='pending':
                pending_count+=1
            elif i.status=='signed':
                signed_count+=1
            else:
                declined_count+=1
        pending_count=alldoccount-(signed_count+declined_count)
        return render(request,'profile.html',{'signed_count':signed_count,'declined_count':declined_count,'pending_count':pending_count,'alldoccount':alldoccount,'lastdoc':lastdoc,'lastdocuserscnt':lastdocuserscnt})
    else:
        return redirect('/')

def feedback(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/')

def profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ExtendedUpdateForm(request.POST,instance=request.user)
            profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
            if form.is_valid() and profile_form.is_valid():
                form.save()
                profile_form.save()
                return redirect('log')
            else:
                return redirect('profile')
        else:
            form = ExtendedUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=request.user.profile)
            return render(request,'profile_update.html',{'form':form,'form1':profile_form})
    else:
        return redirect('/')

def createdoc(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ConsentDocumentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('log')
            else:
                return redirect('createdoc')
        else:
            form = ConsentDocumentForm()
            return render(request,'createdoc.html',{'form':form})
    else:
        return redirect('/')
    
def alldoc(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            src_doc = request.POST['srh']
            src_words=src_doc.split()
            result = []
            all_doc=ConsentDocument.objects.all()
            for i in all_doc:
                title_words = i.title.split()
                count=0
                for word in title_words:
                    for src_word in src_words:
                        if src_word.lower() in word.lower() or word.lower() in src_word.lower():
                            count+=1
                result.append([i,count])
            print(*result,sep='\n')
            result =[i[0] for i in sorted(result,key=lambda x:x[1],reverse=True) if i[1]>0]
            str1 = 'showing results for "{}"'.format(src_doc)
            return render(request,'alldoc.html',{'document':result,'str1':str1,'src_doc':src_doc})
        else:
            document = ConsentDocument.objects.all()
            count = ConsentDocument.objects.count()
            document = [i for i in document]
            document = sorted(document,key=lambda x:x.id,reverse=True)
            return render(request,'alldoc.html',{'document':document,'count':count})
    else:
        return redirect('/')
    

def editdoc(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            document = ConsentDocument.objects.get(id=id)
            form = ConsentDocumentForm(request.POST,instance=document)
            if form.is_valid():
                form.save()
                return redirect('log')
            else:
                return redirect('createdoc')
        else:
            form = ConsentDocumentForm()
            return render(request,'createdoc.html',{'form':form})
    else:
        return redirect('/')

def allparticipents(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            src_name = request.POST['srh']
            name = Profile.objects.filter(acc_type='participent')
            users = User.objects.all()
            name = [i for i in users if i.id in [j.user.id for j in name]]
            result=[]
            for i in name:
                if src_name.lower() in i.first_name.lower()+i.last_name.lower():
                    result.append(i)
            finallist =sorted(result,key=lambda x:x.first_name)
            str1 = 'showing results for "{}"'.format(src_name)
            return render(request,'allparticipents.html',{'name':finallist,'str1':str1,'count':len(name),'src_name':src_name})
        else:
            name = Profile.objects.filter(acc_type='participent')
            users = User.objects.all()
            name = [i for i in users if i.id in [j.user.id for j in name]]
            return render(request,'allparticipents.html',{'name':name,'count':len(name)})
    else:
        return redirect('/')

def pendingdoc(request):
     if request.user.is_authenticated:
        documentID = ConsentDocument.objects.all()
        statusID = ConsentStatus.objects.filter(user=request.user)
        document1= sorted([i for i in documentID if i.id not in [j.document.id for j in statusID]],key=lambda x:x.id,reverse=True)
        return render(request,'alldoc.html',{'document':document1,'count':len(document1)})
     else:
        return redirect('/')
     
def signeddoc(request):
    if request.user.is_authenticated:
        documentID = ConsentDocument.objects.all()
        statusID = ConsentStatus.objects.filter(user=request.user.id,status='signed')
        document1=[j for j in documentID if j.id in [i.document.id for i in statusID]]
        return render(request,'alldoc.html',{'document':document1,'count':len(document1)})
    else:
        return redirect('/')

def declineddoc(request):
    if request.user.is_authenticated:
        documentID = ConsentDocument.objects.all()
        statusID = ConsentStatus.objects.filter(user=request.user.id,status='declined')
        document1=[j for j in documentID if j.id in [i.document.id for i in statusID]]
        return render(request,'alldoc.html',{'document':document1,'count':len(document1)})
    else:
        return redirect('/')
    
def draftdoc(request):
    if request.user.is_authenticated:
        documentID = ConsentDocument.objects.all()
        statusID = ConsentStatus.objects.filter(user=request.user.id,status='pending')
        document1=[j for j in documentID if j.id in [i.document.id for i in statusID]]
        return render(request,'alldoc.html',{'document':document1,'count':len(document1)})
    else:
        return redirect('/')

def viewdetails(request,id):
    if request.user.is_authenticated:
        document = ConsentDocument.objects.get(id=id)
        name = User.objects.all()
        status = ConsentStatus.objects.filter(document=document,user=request.user)
        allreactedusers = ConsentStatus.objects.filter(document=document)
        participentname = Profile.objects.filter(acc_type='participent')
        allusers = User.objects.all()
        allnames = [i for i in allusers if i.id in [j.user.id for j in participentname]]
        signed_users,declined_users,pending_users=[],[],[]
        for i in allreactedusers:
            if i.status == 'signed':
                signed_users.append(i)
            elif i.status == 'declined':
                declined_users.append(i)
        for i in allnames:
            if i not in [j.user for j in signed_users] and i.id not in [j.user for j in declined_users]:
                pending_users.append(i)
        difference=0
        if status:
            difference = timezone.make_aware(datetime.datetime.now()).replace(tzinfo=None) - status[0].signed_at.replace(tzinfo=None)
            difference= difference.days
            status=status[0]
        return render(request,'viewdetails.html',{'document':document,'name':name,'statusID':status,'datediff':difference,'signed_users':signed_users,'declined_users':declined_users,'pending_users':pending_users})
    else:
        return redirect('/')

def sign(request,id):
    if request.user.is_authenticated:
        documentID = ConsentDocument.objects.get(id=id)
        userID = request.user
        check = ConsentStatus.objects.filter(document=documentID,user=userID).update(status='signed')
        if not check:
            status = ConsentStatus.objects.create(user=userID,document=documentID,status='signed',signed_at=datetime.datetime.now(),comments='')
            status.save()
        statusID = ConsentStatus.objects.filter(document=documentID,user=userID)
        return render(request,'viewdetails.html',{'document':documentID,'name':userID,'statusID':statusID[0]})
    else:
        return redirect('/')

def decline(request,id):
    if request.user.is_authenticated:
        documentID = ConsentDocument.objects.get(id=id)
        userID = request.user
        check = ConsentStatus.objects.filter(document=documentID,user=userID).update(status='declined')
        if not check:
            status = ConsentStatus.objects.create(user=userID,document=documentID,status='declined',signed_at=datetime.datetime.now(),comments='')
            status.save()
        statusID = ConsentStatus.objects.filter(document=documentID,user=userID)
        return render(request,'viewdetails.html',{'document':documentID,'name':userID,'statusID':statusID[0]})
    else:
        return redirect('/')
    
def revoke(request,id):
    if request.user.is_authenticated:
        documentID = ConsentDocument.objects.get(id=id)
        userID = request.user
        ConsentStatus.objects.filter(document=documentID,user=userID).delete()
        return render(request,'viewdetails.html',{'document':documentID,'name':userID,'status':''})
    else:
        return redirect('/')

def draft(request,id):
    if request.user.is_authenticated:
        documentID = ConsentDocument.objects.get(id=id)
        userID = request.user
        status = ConsentStatus.objects.create(user=userID,document=documentID,status='pending',signed_at=datetime.datetime.now(),comments='')
        status.save()
        return render(request,'viewdetails.html',{'document':documentID,'name':userID,'statusID':status})
    else:
        return redirect('/')
    
def viewparticipent(request,id):
    if request.user.is_authenticated:
        userDetails = User.objects.get(id=id)
        allDocuments = ConsentDocument.objects.all()
        allConsent = ConsentStatus.objects.filter(user=userDetails)
        signed_doc,declined_doc,pending_doc=[],[],[]
        for i in allConsent:
            if i.status=='signed':
                signed_doc.append(i)
            elif i.status=='declined':
                declined_doc.append(i)
        for i in allDocuments:
            if i not in [j.document for j in signed_doc] and i not in [j.document for j in declined_doc]:
                pending_doc.append(i)
        return render(request,'viewparticipent.html',{'userDetails':userDetails,'signed_doc':signed_doc,'declined_doc':declined_doc,'pending_doc':pending_doc})
    else:
        return redirect('/')