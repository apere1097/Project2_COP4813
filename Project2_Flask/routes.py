from Project2_Flask import app, forms
from flask import request, render_template
from pprint import pprint


@app.route('/', methods=['GET', 'POST'])
def selection():
    my_form = forms.BookReview(request.form)

    if request.method == 'POST':

        topic_selection = request.form["topic_selection"]  # list or reviews
        author = request.form["author"]
        title = request.form["title"]
        isbn = request.form["isbn"]
        date = request.form["date"]
        option = request.form["option"]  # date, history, overview
        overview_type = request.form["overview_type"]
        search = request.form["search"]

        response = [topic_selection, author, title, isbn, option, date, overview_type, search]

        if response[0] == 'list':

            data = forms.generate_data_from_books_api(response)

        elif response[0] == 'reviews':

            data = forms.generate_data_from_books_api(response)

        return render_template('results.html', form=my_form, response=response, data=data)

    return render_template('search.html', form=my_form)

