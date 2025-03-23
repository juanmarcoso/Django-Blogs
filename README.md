# My Django Blog Project

This is a Django project that implements a blog with features such as **post search**, **email sharing**, a **commenting system**, **RSS feeds**, and a **sitemap**. The project was initially developed using *SQLite3* and has been migrated to *PostgreSQL* for production.

# Project Structure

- mysite/
  - blog/
    - static/
      - blog.css
    - templates/
      - pagination.html
      - blog/
        - base.html
      - post/
        - comment.html
        - detail.html
        - latest_posts.html
        - list.html
        - search.html
        - share.html
      - includes/
        - comment_form.html
    - templatetags/
      - __init__.py
      - blog_tags.py
    - admin.py
    - apps.py
    - feeds.py
    - forms.py
    - models.py
    - sitemaps.py
    - tests.py
    - urls.py
    - views.py
  - mysite/
    - __pycache__/
    - __init__.py
    - asgi.py
    - settings.py
    - urls.py
    - wsgi.py
  - README.md
  - manage.py


## Key Features

- **Post Search:** Users can search for posts by keywords.
- **Share Posts:** Users can share posts via email.
- **Comments:** Users can leave comments on posts.
- **RSS Feed:** Users can subscribe to an RSS feed of the latest posts.
- **Sitemap:** The project includes a sitemap for better SEO.
- **Database:** Migrated from SQLite to PostgreSQL for production.

## Views Functionality

The project includes the following views:

- **`post_share(request, post_id)`:** Handles sharing a post via email.
- **`post_detail(request, year, month, day, post)`:** Displays the details of a specific post.
- **`post_comment(request, post_id)`:** Handles adding comments to a post (requires POST method).
- **`post_search(request)`:** Handles searching for posts based on a query.

## Forms

The project includes the following forms:

- **`EmailPostForm(forms.Form)`:** Form for sharing posts via email.
- **`CommentForm(forms.ModelForm)`:** Form for submitting comments on posts.
- **`SearchForm(forms.Form)`:** Form for searching posts.

## Project Setup

1. **Clone the repository:**

```bash
>> git clone git@github.com:juanmarcoso/Django-Blogs.git
```

2. **Create a virtual environment:**

```bash
>> python3 -m venv venv
>> source venv/bin/activate
```

3. **Install dependencies:**

```bash
>> pip install -r requirements.txt
```

### Configure the database:

* Ensure PostgreSQL is installed and configured.
* Update the database configuration in mysite/settings.py.
* Apply migrations:

```bash
>> python manage.py migrate
```

* Create a superuser:

```bash    
>> python manage.py createsuperuser
```

* Run the development server:

```bash
>> python manage.py runserver
```

### Usages

* Access the admin panel at http://127.0.0.1:8000/admin/.

* Explore posts at http://127.0.0.1:8000/blog/.

* Use the search feature to find specific posts.

* Share posts via email using the "Share" button.

* Leave comments on posts.

## Contributing

If you'd like to contribute to this project, please follow these steps:

* Fork the repository.
* Create a new branch (git checkout -b feature/new-feature).
* Make your changes and commit them (git commit -am 'Add new feature').
* Push to the branch (git push origin feature/new-feature).
* Open a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
Contact

### If you have any questions or suggestions, feel free to contact me at juanmadev69@gmail.com.