from flask import request, abort, make_response
import logging
from Persistence_Layer.Models import RequestObject
from Service_Layer.Flask_Initialization_Service import Flask_Initialization_Service

# initialization
init_object = Flask_Initialization_Service()
app = init_object.app
website_scraper = init_object.website_scraper
dm = init_object.dm


# if email or link doesn't exist, it will insert
@app.route('/all/updateTableWithEmailAndLink', methods=['POST'])
def update_table_with_email_and_link():
    email = request.args.get('email', type=str)
    link = request.args.get('link', type=str)

    try:
        request_object = RequestObject(email, link)
        scraping_response = website_scraper.scrape_request(request_object)

        response_json = dm.update_tables_with_scrape_response(scraping_response)

        response = make_response(response_json, 200)
        return response
    except Exception as e:
        abort(404, description=e)


# may need to protect this endpoint
# send email or do webhook on database
@app.route('/all/updateAllHTMLEntries', methods=['POST'])
def updateAllHTMLEntries():
    try:
        response_json = dm.update_tables_chron_job()

        response = make_response(response_json, 200)
        return response
    except Exception as e:
        abort(404, description=e)


# @app.route('/books/<int:book_id>', methods=['GET'])
# def get_book(book_id):
#     book = Book.query.filter_by(id=book_id).first()
#     if book:
#         return jsonify({'id': book.id, 'title': book.title, 'author': book.author})
#     else:
#         return jsonify({'error': 'Book not found'}), 404
#
#
# @app.route('/books', methods=['POST'])
# def add_book():
#     data = request.get_json()
#     book = Book(title=data['title'], author=data['author'])
#     db.session.add(book)
#     db.session.commit()
#     return jsonify({'id': book.id, 'title': book.title, 'author': book.author}), 201
#
#
# @app.route('/books/<int:book_id>', methods=['PUT'])
# def update_book(book_id):
#     book = Book.query.filter_by(id=book_id).first()
#     if book:
#         data = request.get_json()
#         book.title = data['title']
#         book.author = data['author']
#         db.session.commit()
#         return jsonify({'id': book.id, 'title': book.title, 'author': book.author})
#     else:
#         return jsonify({'error': 'Book not found'}), 404
#
#
# @app.route('/books/<int:book_id>', methods=['DELETE'])
# def delete_book(book_id):
#     book = Book.query.filter_by(id=book_id).first()
#     if book:
#         db.session.delete(book)
#         db.session.commit()
#         return '', 204
#     else:
#         return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
