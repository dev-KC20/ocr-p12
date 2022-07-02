from rest_framework.permissions import BasePermission

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

    edit_delete_methods = ["PUT", "PATCH", "DELETE"]
    create_methods = ["POST"]
    read_methods = ["GET"]

    def has_permission(self, request, view):

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # here the request.user.is_authenticated

        # lookup section obj in ['Client','Contract','Event']
        if view.kwargs.get("client_pk"):
            current_client_id = view.kwargs.get("client_pk")
        if obj.pk:
            current_obj_pk = obj.pk
        # get the sale contact person for the current client (own status)
        if isinstance(obj, Client) or isinstance(obj, Contract) or isinstance(obj, Event):
            if not view.kwargs.get("client_pk"):
                current_client_id = current_obj_pk
            client_contact = Client.objects.get(id=current_client_id).value("sale_contact")
        print("client_contact", client_contact)
        # get the request user department
        user_employee = User.objects.get(id == request.user)
        user_role = user_employee.department
        print("user ", user_employee, " dept: ", user_role)

        # authorise section
        # let superuser be superuser == have full access as well as managment 
        if request.user.is_superuser or user_role == "M":
            return bool(request.user and request.user.is_superuser)
        # all authenticated employees can read all obj
        if request.method in read_methods:
            return True
        if user_role == "S":
            # sales person can create Client
            if request.method in create_methods:
                if isinstance(obj, Client) :
                    return True
                else: 
                    # only sales contact can create Contract, Event
                    if user_employee.id == client_contact:
                        return True
            elif request.method in edit_delete_methods:
                # to update or delete you shall be the contact
                if user_employee.id == client_contact:
                    return True
        elif user_role == 'A':
            # support person can't create anything
            if request.method in edit_methods and isinstance(obj, Event): 
                # support person can only update own event
                support_contact = obj.support_contact
                print("user ", user_employee, " dept: ", user_role," support_contact: ", support_contact)
                if user_employee.id == support_contact:
                    return True
        return False

