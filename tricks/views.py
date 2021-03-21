from django.shortcuts import render, redirect
from tricks.models import Trick, UserTricks, User, Class
import requests
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned



# Create your views here.
"""
View Methods:
    - sign_in
    - index_all
    - detail
    - index_user

Additional Methods:
    - get_tricks
    - get_classes
"""



def sign_in(request):
    """
    ===============================
    SIGN_IN:
    -------------------------------
        Prompts for username and password.
        Upon successful sign in, takes you to user_tricks.
    ===============================
    """
    get_trick_data()
    # DELETE ME WHEN FINISHED IMPLEMENT SIGN-UP
    # User.objects.all().delete()
    #User.objects.get(username="jafar").delete()
    if len(User.objects.all()) == 0:
        u = User(username="jimbo",password="12345")
        u.save()
        u = User(username="almond16",password="abcde")
        u.save()
        


    context = {
        "error" : "",
        "password" : "",
        "username" : "",
        "confirm_msg" : "",
        "confirm_password" : False,
    }

    if request.method == "POST":
        if request.POST.get("login") == "true":
            try:
                username = request.POST.get("username")
                password = request.POST.get("password")
           
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session["username"] = user.username
                    request.session["user_id"] = user.id
                    return redirect(index_user)
                else:
                    context['error'] = "The Username and Password did not match."
            except ObjectDoesNotExist as e:
                # username does not exist
                context['error'] = "Invalid Username. Did you mean to create new account?"
                # new_user = User(username=username,password=password)
            except MultipleObjectsReturned as e:
                print('That username is already being used')
            except Exception as e:
                print(e)

        elif request.POST.get("create") == "true":
            try:
                username = request.POST.get("username")
                password = request.POST.get("password")
                usernames = User.objects.filter(username=username)
                if len(usernames) != 0:
                    context['error'] = "That username is already being used!"
                
                else:
                    confirm_pass = request.POST.get("confirm_pass")
                    # print(confirm_pass, "here")
                    if confirm_pass != "" and confirm_pass != None :
                        if password == confirm_pass:
                            new_user = User(username=username, password=password)
                            new_user.save()
                            context["error"] = "Accounted created succesfully. \nPlease Sign In."
                        else:
                            context["error"] = "The password did not match. Please try again."
                            context["password"] = password
                            context["username"] = username
                            context["confirm_msg"] = "Please confirm your Password."
                            context["confirm_password"] = True
                    else:
                        context["password"] = password
                        context["username"] = username
                        context["confirm_msg"] = "Please confirm your Password."
                        context["confirm_password"] = True

            except Exception as e:
                print(e)
     
    
    return render(request, 'sign_in.html', context)



def index_user(request):
    """
    ===============================
    INDEX_USER:
    -------------------------------
        Show user's tricks.
            - Edit tricks
            - Generate combo
    ===============================
    """
    # print(request.POST)
    user_id = request.session["user_id"]
    username = request.session["username"]
    user_trick = UserTricks.objects.filter(user_id=user_id)
    
    
    
    ids = []
    for t in user_trick:
        ids.append(t.trick_id)
    user_tricks = Trick.objects.filter(id__in=ids)

    cids = []
    for t in user_tricks:
        cids.append(t.class_id)
    classes = Class.objects.filter(id__in=cids)
    

    context = {
        'username' : username,
        'classes' : classes,
        'tricks' : user_tricks,
    }
    return render(request, 'index_user.html', context)



def index_all(request):
    """
    ===============================
    INDEX_ALL:
    -------------------------------
        Show all tricks with option to save tricks via checkbox
    ===============================
    """    
    
    tricks = Trick.objects.all()

    classes = Class.objects.all()
    classes1 = classes[:1+len(classes)//3]
    # for c in classes1:
    #     print(c.name)
    classes2 = classes[1+len(classes)//3:1+2*len(classes)//3]
    classes3 = classes[1+2*len(classes)//3:]

    context = {
        "classes" : classes,
        "classes1" : classes1,
        "classes2" : classes2,
        "classes3" : classes3,
        "tricks" : tricks,
        "error" : "",
    }

    """
    Retrieves selected tricks and saves to UserTricks database
    for current user.
    """
    user_id = request.session["user_id"]
    if request.method == "POST":
        # print(request.POST)
        try:
            if request.POST.get("submit") == "Save Changes":
                saved_tricks = request.POST.getlist("saved_tricks")
                
                for trick in saved_tricks:
                    user_tricks = UserTricks(user_id=user_id,trick_id=trick)
                    user_tricks.save()
                # print("so far so good")
                    
                return redirect(index_user)
            elif request.POST.get("delete") == "Delete All":
                print("deleting")
                UserTricks.objects.filter(user_id=user_id).delete()
                print("deleted")
        except Exception as e:
            # print("That didn't work")
            context["error"] = "There was an error saving your tricks."
            print(e)
        

    return render(request, 'index_all.html', context)



def detail(request, pk):
    """
    ===============================
    DETAIL:
    ===============================
    """

    trick = Trick.objects.get(pk=pk)
    context = {
        'trick': trick
    }
    return render(request, 'detail.html', context)



def get_trick_data():
    """
    ===============================
    GET_TRICK_DATA:
    -------------------------------
    
        Builds Trick table from club540.com API.

        data : [statusCode, flash, 
                {data : [classes, origins, tricks]}
                        {tricks: }]
    ===============================
    """
    # The following clears Trick and Class tables. Uncomment if needed:
    # Trick.objects.all().delete()
    # Class.objects.all().delete()

    # Build table if no tricks read in.
    tricks = Trick.objects.all()
    if len(tricks) == 0:

        response = requests.get('http://club540.com/api/tricks')
        data = response.json()

        trick_classes = data["data"]["classes"]
        get_classes(trick_classes)

        data = data["data"]["tricks"]
        get_tricks(data)


def get_tricks(data):
    """
    ===============================
    GET_TRICKS:
    -------------------------------
        Builds Trick table from club540.com API.
    ===============================
    """

    for trick in data:
        # print(trick)
        name = trick["name"]
        #print(name)
        description = trick["description"]
        id = trick["id"]
        class_id = trick["classId"]
    
        curr_trick = Trick(id=id, name=name, description=description, class_id=class_id)
        curr_trick.save()


def get_classes(trick_classes):
    """
    ===============================
    GET_CLASSES:
    -------------------------------
        Builds Class table from club540.com API.
    ===============================
    """
    for tclass in trick_classes:
        # print(tclass)
        id = tclass["id"]
        name = tclass["name"]
        description = tclass["description"]

        t_class = Class(id=id, description=description, name=name)
        t_class.save()