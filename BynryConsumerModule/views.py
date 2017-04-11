# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
from BynryConsumerModuleapp.models import UserPrivilege, SystemUserProfile, \
    City, UserRole, Branch
import json
import traceback
from datetime import datetime
from consumerapp.views import get_city

# importing mysqldb and system packages
import MySQLdb

# HTTP Response
from django.http import HttpResponse

def dashboard(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        return render(request, 'dashboard.html')

def login(request):
    return render(request, 'login.html')


# redirect to system user's page
def system_user(request):
    print 'views.py|system_user'
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        role_list = []
        branch_list = []
        role_objs = UserRole.objects.filter(is_deleted=False, status='Active')
        total_role_count = UserRole.objects.filter(is_deleted=False).count()
        active_role_count = UserRole.objects.filter(is_deleted=False,
                                                    status='Active').count()
        inactive_role_count = UserRole.objects.filter(is_deleted=False,
                                                      status='Inactive').count()
        branch_obj = Branch.objects.filter(is_deleted=False)
        for branch in branch_obj:
            branch_data = {'branch_id':branch.id, 'branch':branch.branch_name}
            branch_list.append(branch_data)
        for role in role_objs:
            role_data = {'role_id':role.id, 'role':role.role}
            role_list.append(role_data)
        data = {'city_list':get_city(request), 'role_list':role_list, 'branch_list':branch_list,
                'active_role_count':active_role_count,
                'inactive_role_count':inactive_role_count,
                'total_role_count':total_role_count
                }
        return render(request, 'system_user.html', data)


# redirect to administrator's page
def administrator(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        try:
            print 'views.py|administrator'
            privilege_list = UserPrivilege.objects.filter(is_deleted=False)
            data = {'privilege_list':privilege_list}

        except Exception, e:
            print 'views.py|administrator'
        return render(request, 'administrator.html', data)

def complaints(request):
    return render(request, 'complaints.html')

def services(request):
    return render(request, 'services.html')

#vigilance_cases
def vigilance_cases(request):
    return render(request, 'vigilance_cases.html')

def payments(request):
    return render(request, 'payments.html')


# save system user details
def save_system_user_details(request):
    try:
        print 'views.py|save_system_user_details'
        city_obj = City.objects.get(city=request.GET.get('city'))
        role_obj = UserRole.objects.get(role=request.GET.get('role'))
        if request.GET.get('user_status') == 'true':
            user_status = 'Active'
        else:
            user_status = 'Inactive'
        user_obj = SystemUserProfile(
            username=request.GET.get('email'),
            contact_no=request.GET.get('contact_no'),
            address=request.GET.get('address'),
            first_name=request.GET.get('first_name'),
            last_name=request.GET.get('last_name'),
            city=city_obj,
            employee_id=request.GET.get('emp_id'),
            role=role_obj,
            email=request.GET.get('email'),
            status=user_status
            )
        user_obj.save()

        user_obj.set_password(request.GET.get('password'))
        user_obj.save()

        if request.GET.get('branch'):
            branch_obj = Branch.objects.get(id=request.GET.get('branch'))
            user_obj.branch = branch_obj
            user_obj.save()
        data = {'success':'True'}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|save_system_user_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# get system user details
def get_system_user_details(request):
    try:
        print 'views.py|get_system_user_details'
        user_obj = SystemUserProfile.objects.get(id=request.GET.get('user_id'))
        if user_obj.branch:
            branch = user_obj.branch.branch_name
        else:
            branch = ''
        user_data = {'user_id' : user_obj.id,
                     'first_name' : user_obj.first_name,
                     'last_name' : user_obj.last_name,
                     'city' : user_obj.city.city,
                     'role' : user_obj.role.role,
                     'email' : user_obj.email,
                     'user_status' : user_obj.status,
                     'employee_id' : user_obj.employee_id,
                     'contact_no' : user_obj.contact_no,
                     'address' : user_obj.address,
                     'branch':branch
                     }
        data = {'success' : 'true', 'user_data' : user_data}
        print data
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_system_user_details', e
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# update system user details
def update_system_user_details(request):
    try:
        print 'views.py|update_system_user_details'
        user_obj = SystemUserProfile.objects.get(id=request.GET.get('user_id'))
        city_obj = City.objects.get(city=request.GET.get('city'))
        role_obj = UserRole.objects.get(role=request.GET.get('role'))

        if request.GET.get('user_status')=='true':
            user_obj.status = 'Active'
        else:
            user_obj.status = 'Inactive'

        user_obj.username = request.GET.get('email')
        user_obj.contact_no = request.GET.get('contact_no')
        user_obj.address = request.GET.get('address')
        user_obj.first_name = request.GET.get('first_name')
        user_obj.last_name = request.GET.get('last_name')
        user_obj.city = city_obj
        user_obj.employee_id = request.GET.get('emp_id')
        user_obj.role = role_obj
        user_obj.email = request.GET.get('email')
        user_obj.save()

        user_obj.set_password(request.GET.get('password'))
        user_obj.save()

        if request.GET.get('branch'):
            branch = request.GET.get('branch')
            branch_obj = Branch.objects.get(branch_name=branch)
            user_obj.branch = branch_obj
            user_obj.save()
        data = {'success':'True'}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|update_system_user_details', e
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# get head admin list
def head_admin(request):
    final_list = []
    try:
        print 'views.py|head_admin'
        try:
            head_admin_list = SystemUserProfile.objects.all()
            # get head admin data list
            for h in head_admin_list:
                if h.status == 'Active':
                    status = '<span style = "cursor : default;" class = "btn btn-success">Active</span>'
                else:
                    status = '<span style = "cursor : default;" class = "btn btn-danger">Inactive</span>'
                head_admin_data = {'id' : str(h.employee_id),
                                   'name' : str(h.first_name)+' '+str(h.last_name),
                                   'contact' : str(h.contact_no),
                                   'email' : str(h.email),
                                   'role' : str(h.role),
                                   'status' : str(status),
                                   'actions' : '<a class="icon-pencil" title="Edit" onclick="edit_admin_modal('+ str(h.id) +');"></a>',
                              }
                final_list.append(head_admin_data)
            data = {'data' : final_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|head_admin', e
            print 'Exception', e
            data = {'success' : 'false', 'error' : 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def head_supervisor(request):
    final_list = []
    try:
        print 'views.py|head_supervisor'
        try:
            role_obj = UserRole.objects.get(role="H.O.Supervisor")
            head_supervisor_list = SystemUserProfile.objects.filter(role=role_obj)
            # get head admin data list
            for h in head_supervisor_list:
                head_admin_data = {'id' : str(h.id),
                              'name' : str(h.first_name)+' '+str(h.last_name),
                              'contact' : str(h.contact_no),
                              'email' : str(h.email),
                              'status' : str(h.status),
                              'actions' : '<a class="icon-pencil" title="Edit" onclick="edit_supervisor_modal('+ str(h.id) +');"></a>',
                              }
                final_list.append(head_admin_data)
            data = {'data' : final_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|head_supervisor', e
            print 'Exception', e
            data = {'success' : 'false', 'error' : 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def branch_admin(request):
    final_list = []
    try:
        print 'views.py|branch_admin'
        try:
            role_obj = UserRole.objects.get(role="Branch Admin")
            branch_admin_list = SystemUserProfile.objects.filter(role=role_obj)
            # get branch admin data list
            for b in branch_admin_list:
                branch_admin_data = {'id' : str(b.id),
                              'name' : str(b.first_name)+' '+str(b.last_name),
                              'contact' : str(b.contact_no),
                              'email' : str(b.email),
                              'status' : str(b.status),
                              'actions' : '<a class="icon-pencil" title="Edit" onclick="edit_branch_admin_modal('+ str(b.id) +');"></a>',
                              }
                final_list.append(branch_admin_data)
            data = {'data': final_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|branch_admin', e
            print 'Exception', e
            data = {'success': 'false', 'error': 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def branch_supervisor(request):
    final_list = []
    try:
        print 'views.py|branch_supervisor'
        try:
            role_obj = UserRole.objects.get(role="Branch Supervisor")
            branch_supervisor_list = SystemUserProfile.objects.filter(role=role_obj)
            # get branch Supervisor data list
            for b in branch_supervisor_list:
                branch_supervisor_data = {'id' : str(b.id),
                              'name' : str(b.first_name)+' '+str(b.last_name),
                              'contact' : str(b.contact_no),
                              'email' : str(b.email),
                              'status' : str(b.status),
                              'actions' : '<a class="icon-pencil" title="Edit" onclick="edit_branch_supervisor_modal('+ str(b.id) +');"></a>',
                              }
                final_list.append(branch_supervisor_data)
            data = {'data' : final_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|branch_supervisor', e
            print 'Exception', e
            data = {'success' : 'false', 'error' : 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')

def branch_agent(request):
    final_list = []
    try:
        print 'views.py|branch_agent'
        try:
            role_obj = UserRole.objects.get(role="Branch Desk Agent")
            branch_agent_list = SystemUserProfile.objects.filter(role=role_obj)
            # get branch Desk Agent data list
            for b in branch_agent_list:
                branch_agent_data = {'id' : str(b.id),
                              'name' : str(b.first_name)+' '+str(b.last_name),
                              'contact' : str(b.contact_no),
                              'email' : str(b.email),
                              'status' : str(b.status),
                              'actions' : '<a class="icon-pencil" title="Edit" onclick="edit_branch_agent_modal('+ str(b.id) +');"></a>',
                              }
                final_list.append(branch_agent_data)
            data = {'data' : final_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|branch_agent', e
            print 'Exception', e
            data = {'success' : 'false', 'error' : 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')


# save new role
@csrf_exempt
def save_new_role(request):
    try:
        print 'views.py|save_new_role'
        privilege_list = request.POST.get('privilege_list')
        privilege_list = privilege_list.split(',')
        new_role_obj = UserRole(
            role=request.POST.get('roll_name'),
            description=request.POST.get('description'),
            status="Active",
            created_on=datetime.now(),
            updated_on=datetime.now()
        )
        new_role_obj.save()
        for list_obj in privilege_list:
            obj = UserPrivilege.objects.get(privilege=list_obj)
            new_role_obj.privilege.add(obj)
            new_role_obj.save()
        data = {'success':'true', 'message':'Consumer created successfully.'}
    except Exception, e:
        print 'Exception|views.py|save_new_role', e
        data = {
            'success' : 'false',
            'message' : str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


# get role list
def get_role_list(request):
    try:
        print 'views.py|get_role_list'
        data = {}
        final_list = []
        try:
            role_obj_list = UserRole.objects.all()
            for role_obj in role_obj_list:
                role = role_obj.role
                description = role_obj.description
                created_on = role_obj.created_on.strftime("%d-%m-%Y")

                associated_user_obj = SystemUserProfile.objects.filter(role=role_obj.id)  
                users_name_list=''                
                for users in associated_user_obj: 
                    users_name_list = str(users.first_name)+', '+str(users_name_list)

                if role_obj.status == 'Active':
                    status = '<span style = "cursor : default;" class = "btn btn-success">Active</span>'
                else:
                    status = '<span style = "cursor : default;" class = "btn btn-danger">Inactive</span>'
                action = '<a> <i class = "fa fa-pencil" aria-hidden = "true" onclick = "edit_role_modal(' + str(role_obj.id) + ')"></i> </a>'
                role_data = {
                    'role' : role,
                    'description' : description,
                    'created_on' : created_on,
                    'associated_user' : users_name_list,
                    'status' : status,
                    'action' : action
                }
                final_list.append(role_data)
            data = {'success' : 'true', 'data' : final_list}
        except Exception as e:
            print 'Exception|views.py|get_role_list', e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|views.py|get_role_list', e
    except Exception, e:
        print 'Exception|views.py|get_role_list', e
    return HttpResponse(json.dumps(data), content_type='application/json')


# get role details and privileges list
def get_role_details(request):
    try:
        print 'views.py|get_role_details'
        data = {}
        final_list = []
        try:
            i = 11
            plist = []
            # Particular User privileges list
            role_obj = UserRole.objects.get(id=request.GET.get('role_id'))
            privilege_obj = role_obj.privilege.all()             
            for obj_p in privilege_obj:            
                plist.append(obj_p.privilege)
            # All privileges list
            privilege_list = UserPrivilege.objects.all()
            for pri_obj in privilege_list :                    
                if pri_obj.privilege in plist:
                    ss1 = "<div class='col-md-4'><div class='md-checkbox'><input type='checkbox' value='"+pri_obj.privilege+"' id='checkbox1_"+str(i)+"' class='md-check privillagesModel' checked>"
                    ss2 = "<label for='checkbox1_"+str(i)+"'> <span></span> <span class='check privillages'></span>"
                    ss3 = "<span class='box'></span>"+pri_obj.privilege+" </label>  </div> </div>"
                    ss = ss1 + ss2 + ss3
                else:
                    ss1 = "<div class='col-md-4'><div class='md-checkbox'><input type='checkbox' value='"+pri_obj.privilege+"' id='checkbox1_"+str(i)+"' class='md-check privillagesModel'>"
                    ss2 = "<label for='checkbox1_"+str(i)+"'> <span></span> <span class='check privillages'></span>"
                    ss3 = "<span class='box'></span>"+pri_obj.privilege+" </label>  </div> </div>"
                    ss = ss1 + ss2 + ss3
                i = i + 1
                final_list.append(ss)

            user_data = {
                         'role' : role_obj.role, 'role_description' : role_obj.description,
                         'final_list':final_list,'role_id':role_obj.id,'status':role_obj.status
                        }
            data = {'success' : 'true', 'user_data' : user_data}
        except Exception as e:
            print 'Exception|views.py|get_role_details', e
            data = {'success':'false', 'message':'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|views.py|get_role_details', e
    return HttpResponse(json.dumps(data), content_type='application/json')

# to update role details
@csrf_exempt
def update_role_details(request):
    try:
        print 'views.py|update_role_details'
        privilege_list = request.POST.get('privilege_list')
        privilege_list = privilege_list.split(',')

        role_obj = UserRole.objects.get(id=request.POST.get('roleid'))
        role_obj.description = request.POST.get('description')
        if request.POST.get('status') == 'true':
            role_obj.status = 'Active'
        else:
            role_obj.status = 'Inactive'
        role_obj.save()

        role_obj.privilege.clear()
        for list_obj in privilege_list:
            obj = UserPrivilege.objects.get(privilege=list_obj)
            role_obj.privilege.add(obj)
            role_obj.save()

        data = {'success':'True'}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|update_role_details', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


# to get branch wrt city
def get_branch(request):
    try:
        print 'views.py|get_branch'
        branch_list = []
        # filer branch by city
        city_obj = City.objects.get(city=request.GET.get('city'))
        if city_obj:
            branch_obj = Branch.objects.filter(is_deleted=False, city=city_obj)
        else:
            branch_obj = Branch.objects.filter(is_deleted=False)
        # branch result
        for branch in branch_obj:
            branch_data = {
                'branch_id' : branch.id,
                'branch' : branch.branch_name
            }
            branch_list.append(branch_data)
        data = {'success':'true', 'branch_list':branch_list}
    except Exception, e:
        print "Exception|views.py|get_branch", e
        data = {'success':'false', 'branch_list':[]}
    return HttpResponse(json.dumps(data), content_type='application/json')
