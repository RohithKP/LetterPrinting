# from app import app
# from flask_login import LoginManager, current_user

# login_manager = LoginManager(app)


# @login_manager.request_loader
# def load_user_from_request(request):
#     if request.authorization:
#         username, password = request.authorization.username, request.authorization.password

#         # XXX replace this with an actual password check.
#         if username == password:
#             return User.query.filter_by(username=username).first()
#     return None

# if __name__ == '__main__':
#      load_user_from_request()
from secretary import Renderer
def test():
    engine = Renderer()
    print "hello"
