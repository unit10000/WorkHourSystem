from whmgsystem import app
from .admin import admin
from .api import api
from .user import user
from .super_admin import super_admin
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(api,url_prefix='/api')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(super_admin,url_prefix='/super_admin')