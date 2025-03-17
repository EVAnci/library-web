from app import db
from main.models import UserModel, BookModel, BookCopyModel, RentModel, NotificationModel, CommentModel, AuthorModel
from DB.gen_json import generate_test_data
import json, os

def fill_database():
    """
    Fill the database with test data from the files in the DB directory.
    
    Requires the following files in the DB/test-data/ directory:
    - users.json
    - books.json
    - authors.json
    - book_copies.json
    - rents.json
    - notifications.json
    - comments.json
    
    The format of the json files should be an array of objects, where each object
    represents an instance of the model and has the same keys as the corresponding
    model's columns.
    """
    user_path = './DB/test-data/users.json'
    author_path = './DB/test-data/authors.json'
    book_path = './DB/test-data/books.json'
    book_copy_path = './DB/test-data/book_copies.json'
    rent_path = './DB/test-data/rents.json'
    notification_path = './DB/test-data/notifications.json'
    comment_path = './DB/test-data/comments.json'

    if os.path.exists(user_path):
        with open(user_path, 'r') as users:
            users = json.load(users)
            for user in users:
                db.session.add(UserModel.from_json(user))
        try:
            db.session.commit()
            print("    [!] Usuarios cargados")
        except Exception as e:
            db.session.rollback()
            print("    [!] Error al cargar los usuarios. Detalles del error:", e)

    if os.path.exists(author_path):
        with open(author_path, 'r') as authors:
            authors = json.load(authors)
            for author in authors:
                db.session.add(AuthorModel.from_json(author))
        try:
            db.session.commit()
            print("    [!] Autores cargados")
        except Exception as e:
            db.session.rollback()
            print("    [!] Error al cargar los autores. Detalles del error:", e)

    if os.path.exists(book_path):
        with open(book_path, 'r') as books:
            books = json.load(books)
            for book in books:
                db_book = BookModel.from_json(book)
                db.session.add(db_book)
        try:
            db.session.commit()
            print("    [!] Libros cargados")
        except Exception as e:
            db.session.rollback()
            print("    [!] Error al cargar los libros. Detalles del error:", e)

    if os.path.exists(book_copy_path):
        with open(book_copy_path, 'r') as book_copies:
            book_copies = json.load(book_copies)
            for book_copy in book_copies:
                db.session.add(BookCopyModel.from_json(book_copy))
        try:            
            db.session.commit()
            print("    [!] Copias de libros cargadas")
        except Exception as e:
            db.session.rollback()
            print("    [!] Error al cargar las copias de libros. Detalles del error:", e)

    if os.path.exists(rent_path):
        with open(rent_path, 'r') as rents:
            rents = json.load(rents)
            for rent in rents:
                db.session.add(RentModel.from_json(rent))
        try:
            db.session.commit()
            print("    [!] Prestamos cargados")
        except Exception as e:
            db.session.rollback()
            print("    [!] Error al cargar los prestamos. Detalles del error:", e)

    if os.path.exists(notification_path):
        with open(notification_path, 'r') as notifications:
            notifications = json.load(notifications)
            for notification in notifications:
                db.session.add(NotificationModel.from_json(notification))
        try:
            db.session.commit()
            print("    [!] Notificaciones cargadas")
        except Exception as e:
            db.session.rollback()
            print("    [!] Error al cargar las notificaciones. Detalles del error:", e)

    if os.path.exists(comment_path):
        with open(comment_path, 'r') as comments:
            comments = json.load(comments)
        try:
            for comment in comments:
                db.session.add(CommentModel.from_json(comment))
                db.session.commit()
            print("    [!] Comentarios cargados")
        except Exception as e:
            db.session.rollback()
            print("    [!] Error al cargar los comentarios. Detalles del error:", e)

if __name__ == '__main__':
    db.create_all()
    gen_data = input("[+] Generar datos de prueba? (Y/n): ")
    if gen_data != 'N' and gen_data != 'n':
        print("[+] Generando datos de prueba...\n[+] Cantidades de datos por defecto:")
        print("    [+] Autores: 26")
        print("    [+] Libros: 70")
        print("    [+] Copias de libros: 120")
        print("    [+] Comentarios: 100")
        print("    [+] Notificaciones: 50")
        print("    [+] Prestamos: 60")
        print("    [+] Usuarios: 80")
        default_data = input("[+] Desea usar las cantidades de datos por defecto? (Y/n): ")
        if default_data != 'N' and default_data != 'n':
            generate_test_data()
        else:
            user_count = int(input("[+] Cantidad de usuarios a generar: "))
            book_count = int(input("[+] Cantidad de libros a generar: "))
            book_copy_count = int(input("[+] Cantidad de copias de libros a generar: "))
            comment_count = int(input("[+] Cantidad de comentarios a generar (cantidad de comentaros <= cantidad de usuarios * cantidad de libros): "))
            notification_count = int(input("[+] Cantidad de notificaciones a generar: "))
            rent_count = int(input("[+] Cantidad de rentas a generar (cantidad de rentas <= cantidad de copias de libros): "))
            author_count = int(input("[+] Cantidad de autores a generar: "))
            generate_test_data(
                user_count=user_count, 
                book_count=book_count, 
                book_copy_count=book_copy_count, 
                comment_count=comment_count, 
                notification_count=notification_count, 
                rent_count=rent_count, 
                author_count=author_count
            )
    fill_database()
    print("[+] Base de datos llenada con exito")
    