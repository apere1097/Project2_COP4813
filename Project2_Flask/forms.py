from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, RadioField, SubmitField, DateField
from Project2_Flask import main_functions
import requests


class BookReview(FlaskForm):

    topic_selection = RadioField('topics', choices=[('list', 'Best sellers list'),
                                                    ('reviews', 'Book reviews')])
    
    author = StringField('author', render_kw={"placeholder": "Barack Obama"})

    title = StringField('title', render_kw={"placeholder": "A Promised Land"})

    isbn = IntegerField('isbn', render_kw={"placeholder": "9780307455871"})

    option = SelectField('options', choices=[('', ''),
                                                 ('date', 'Get them by date'),
                                                 ('history', 'History of the best sellers'),
                                                 ('overview', 'Overview of the best sellers')])

    overview_type = SelectField('overview_type', choices=[('', ''),
                                                 ('CPEF', 'Combined Print and E-Book Fiction'),
                                                 ('CPENF', 'Combined Print and E-Book Nonfiction'),
                                                 ('HF', 'Hardcover Fiction'),
                                                 ('HNF', 'Hardcover Nonfiction'),
                                                 ('AHM', 'Advice How-To and Miscellaneous'),
                                                 ('SB', 'Series Books')])

    date = DateField('date', format='%Y-%m-%d', render_kw={"placeholder": "YYYY-MM-DD"})

    search = SubmitField('Search for Book(s)')


def generate_data_from_books_api(data_user_wants):

    if data_user_wants[0] == 'list':

        url = "https://api.nytimes.com/svc/books/v3/lists.json?"

        if data_user_wants[4] == 'date':

            date = data_user_wants[5]

            if date != '' or date != ' ':

                url = "https://api.nytimes.com/svc/books/v3/lists/{}/hardcover-fiction.json?".format(date)

            else:

                url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?"

        elif data_user_wants[4] == 'history':

            url = "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?"

        elif data_user_wants[4] == 'overview':

            url = "https://api.nytimes.com/svc/books/v3/lists/overview.json?"

    elif data_user_wants[0] == 'reviews':

        url = "https://api.nytimes.com/svc/books/v3/reviews.json?"

        if (data_user_wants[1] != "" or data_user_wants[1] != " ") and data_user_wants[0] == 'reviews':

            author_name = add_plus_to_string(data_user_wants[1])

            url = url + "author={}&".format(author_name)

        if (data_user_wants[2] != "" or data_user_wants[2] != " ") and data_user_wants[0] == 'reviews':

            book_title = add_plus_to_string(data_user_wants[2])

            url = url + "title={}&".format(book_title)

        if (data_user_wants[3] != "" or data_user_wants[3] != " ") and data_user_wants[0] == 'reviews':

            isbn = str(data_user_wants[3])

            url = url + "isbn={}&".format(isbn)

    api_key = main_functions.read_from_file("Project2_Flask/JSON_Files/api_key.json")

    my_key = api_key["my_api_key"]

    final_url = url + 'api-key=' + my_key

    response = requests.get(final_url).json()

    main_functions.save_into_file(response, "Project2_Flask/JSON_Files/response.json")

    response_dict = main_functions.read_from_file("Project2_Flask/JSON_Files/response.json")

    return response_dict


    # """"
    #
    #     The section below is for testing various values
    #
    # """

    # url = "https://api.nytimes.com/svc/books/v3/reviews.json?author=Barack+Obama&api-key="
    #
    # api_key = main_functions.read_from_file("JSON_Files/api_key.json")
    #
    # my_key = api_key["my_api_key"]
    #
    # final_url = url + my_key
    #
    # response = requests.get(final_url).json()
    #
    # main_functions.save_into_file(response, "JSON_Files/response.json")
    #
    # response_dict = main_functions.read_from_file("JSON_Files/response.json")
    #
    # title = []
    # article_url = []
    # article_author = []
    # summary = []
    # author = []
    # publication_date = []
    #
    # for i in response_dict['results']:
    #     title.append(i['book_title'])
    #     article_url.append(i['url'])
    #     article_author.append(i['byline'])
    #     summary.append(i['summary'])
    #     author.append(i['book_author'])
    #     publication_date.append(i['publication_dt'])
    #
    # print(title)
    #
    # print('\n')
    #
    # print(title[0])
    # print(article_url[0])
    # print(article_author[0])
    # print(author[0])
    # print(summary[0])
    # print(publication_date[0])


def add_plus_to_string(data):
    index = 0
    array = []
    sent_arr = data.split()

    for i in sent_arr:
        if index < len(sent_arr) - 1:
            array.append(i + "+")
            index = index + 1
        else:
            array.append(i)

    string = ''.join(map(str, array))

    return string
