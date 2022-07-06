from rest_framework.permissions import BasePermission

import base.constants as cts
from users.models import User
from .models import Client, Contract, Event

# from .models import Client

# |	Role	  |                          	E.P.                        	|	Permissions	|
# |---------|---------------------------------------------------------|-------------|
# |	Sales	  |	4.POST /api/v1/clients/                            	    |	C	          |
# |	Sales	  |	6.PUT /api/v1/clients/{id}/	                            |	U own	      |
# |	Sales	  |	9.POST /api/v1/clients/{id}/contracts/	                |	C own	      |
# |	Sales	  |	11.PUT /api/v1/clients/{id}/contracts/{id}	            |	U own	      |
# |	Sales	  |	14.POST /api/v1/clients/{id}/contracts/{id}/events/	    |	C own	      |
# |	Sales	  |	3.GET /api/v1/clients/  5.GET /api/v1/clients/{id}/   8.GET /api/v1/clients/{id}/contracts/   10.GET /api/v1/clients/{id}/contracts/{id}   13.GET /api/v1/clients/{id}/contracts/{id}/events/   15.GET /api/v1/clients/{id}/contracts/{id}/events/{id}	                   |	  R	       |
# |	Support	  |	3.GET /api/v1/clients/ 5.GET /api/v1/clients/{id}/ 8.GET /api/v1/clients/{id}/contracts/ 10.GET /api/v1/clients/{id}/contracts/{id} 13.GET /api/v1/clients/{id}/contracts/{id}/events/ 15.GET /api/v1/clients/{id}/contracts/{id}/events/{id}	                    |	    R	      |
# |	Support	  |	16.PUT /api/v1/clients/{id}/contracts/{id}/events/{id}	|	  U own	    |
# |	Mngnt	  |	admin	                                                |	CRUD /users	|
# |	Mngnt	  |	all E.P.	                                            |	CRUD	      |

# §1 Authentication is managed in the has_permission method of every perm class .
# authenticated users can Read all clients & dependencies they are contact to any


class EmployeeRole(BasePermission):
    def has_permission(self, request, view):
        # for accessing an api view one needs to be authenticated
        user_employee = User.objects.get(id=request.user.id)
        user_role = user_employee.department
        # the support guy is the only one not allowed to [C]reate
        if not request.user.is_superuser and user_role == "A" and view.action == "create":
            return False
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # here the request.user.is_authenticated

        # lookup section obj in ['Client','Contract','Event']
        if view.kwargs.get("pk"):
            current_client_id = int(view.kwargs.get("pk"))
        if obj.pk:
            current_obj_pk = obj.pk
        # get the sale contact person for the current client (own status)
        if isinstance(obj, Client) or isinstance(obj, Contract) or isinstance(obj, Event):
            if not view.kwargs.get("pk"):
                current_client_id = current_obj_pk
            sale_contact = Client.objects.get(id=current_client_id).sale_contact.id
        # get the request user department
        user_employee = User.objects.get(id=request.user.id)
        user_role = user_employee.department

        # authorise section
        # let superuser be superuser == have full access as well as managment
        if request.user.is_superuser or user_role == "M":
            return bool(request.user and request.user.is_superuser)
        # all authenticated employees can read all obj
        if request.method in cts.READ_METHODS:
            return True
        if user_role == "S":
            # sales person can create Client
            if request.method in cts.CREATE_METHODS:
                if isinstance(obj, Client):
                    return True
                else:
                    # only sales contact can create Contract, Event
                    if user_employee.id == sale_contact:
                        return True
            elif request.method in cts.EDIT_DELETE_METHODS:
                # to update or delete you shall be the contact
                if user_employee.id == sale_contact:
                    return True
        elif user_role == "A":
            # support person can't create anything
            if request.method in cts.EDIT_METHODS and isinstance(obj, Event):
                # support person can only update own event
                support_contact = obj.support_contact
                if user_employee.id == support_contact:
                    return True
        return False
