from rest_framework.permissions import BasePermission

# from .models import Client

# |   Role     | Project  | Iss/Comm. | Contrib |
# |------------|----------|-----------|---------|
# |anonymous   | Forbidden|	Forbidden |
# |authenticate|  C       |	C         |
# |contributor |  R       |	CR        |
# |author      |  [CR]UD  |	[CR]UD    | C


# 1. Only authenticated user can acces end-points.
# 2. Only contributors can Read Project, Comment or Issue of the project.
# 3. Only the author of a project manages (CRUD) new contributor(members).
# 4. Only authors can update (U) or delete (D) theirs Project, Comment or Issue.

# §1 Authentication is managed in the has_permission method of every perm class .
# authenticated users can Read all projects & dependencies they are contributor of
# any authenticated user can Create a new project & add contributor into


class SalesRole(BasePermission):

    # edit_delete_methods = ["PUT", "PATCH", "DELETE"]
    # create_methods = ["POST"]
    # read_methods = ["GET"]

    def has_permission(self, request, view):

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # here the request.user.is_authenticated

        # lookup section

        # authorise section
        # let superuser be superuser == have full access
        if request.user.is_superuser:
            return bool(request.user and request.user.is_superuser)

        return False


class SupportRole(BasePermission):

    # edit_delete_methods = ["PUT", "PATCH", "DELETE"]
    # create_methods = ["POST"]
    # read_methods = ["GET"]

    def has_permission(self, request, view):

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # here the request.user.is_authenticated

        # lookup section

        # authorise section
        # let superuser be superuser == have full access
        if request.user.is_superuser:
            return bool(request.user and request.user.is_superuser)

        return False
