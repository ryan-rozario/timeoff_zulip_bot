from .leave import LeavesApi, LeaveApi
from .auth import SignupApi, LoginApi
#from .reset_password import ForgotPassword, ResetPassword

def initialize_routes(api):
    api.add_resource(LeavesApi, '/api/leaves')
    api.add_resource(LeaveApi, '/api/leaves/<id>')
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    #api.add_resource(ForgotPassword, '/api/auth/forgot')
    #api.add_resource(ResetPassword, '/api/auth/reset')
