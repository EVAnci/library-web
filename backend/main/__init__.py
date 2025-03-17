from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
import os

api = Api()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mailsender = Mail()

def create_app():
    app=Flask(__name__)
    CORS(app)
    load_dotenv()
    
    upload_folder = os.getenv("UPLOAD_FOLDER")
    app.config['UPLOAD_FOLDER'] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)

    if not os.path.exists(os.getenv("DATABASE_PATH")+os.getenv("DATABASE_NAME")):
        os.mknod(os.getenv("DATABASE_PATH")+os.getenv("DATABASE_NAME"))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)
    migrate.init_app(app,db)

    import main.resources as resources

    # User
    api.add_resource(resources.UsersResources, '/users')
    api.add_resource(resources.UserResources, '/user/<id>')
    # Book
    api.add_resource(resources.BooksResources, '/books')
    api.add_resource(resources.BookResources, '/book/<id>')
    # Rent
    api.add_resource(resources.RentsResources, '/rents')
    api.add_resource(resources.RentResources, '/rent/<id>')
    # Notifications
    api.add_resource(resources.NotificationsResources, '/notifications')
    api.add_resource(resources.NotificationResources, '/notification/<id>')
    # Comments
    api.add_resource(resources.CommentsResources, '/comments')
    api.add_resource(resources.CommentResources, '/comment/<id>')
    # Authors
    api.add_resource(resources.AuthorsResources, '/authors')
    api.add_resource(resources.AuthorResources, '/author/<id>')
    # BookCopy
    api.add_resource(resources.BookCopiesResources, '/copies')
    api.add_resource(resources.BookCopyResources, '/copy/<id>')
    # Upload
    api.add_resource(resources.UploadImageResource, '/upload')


    api.init_app(app)

    # Load secret key

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    app.config["JWT_VERIFY_SUB"]=False
    jwt.init_app(app)

    from main.auth import routes
    app.register_blueprint(routes.auth)
    
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    mailsender.init_app(app)

    return app