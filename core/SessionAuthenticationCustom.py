from rest_framework.authentication import SessionAuthentication


class SessionAuthenticationCustom(SessionAuthentication):

    def enforce_csrf(self, request):
        pass
