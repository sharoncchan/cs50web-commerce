# Commerce Project

This project is a web application of a commerce website that allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a watchlist.

This project was built using Django as a backend framework and HTML, CSS and Bootstrap as frontend programming tools. All generated details are saved in a database, which is SQLite by default.

All webpages of the project are mobile-responsive.

#### Features of the project 
This project contains the features below where users can:
- create a new listing
- view all the active listings
- add listings to their watchlist
- place bids on the listings
- comment on the listings

#### Running the application
  - Install project dependencies by running `pip install -r requirements.txt`.
  - Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
  - Create superuser with `python manage.py createsuperuser`. This will create a user with admin privileges, with permissions to create, read, update and delete data in the Django admin
  - Run the django server using `python manage.py runserver` to enter the homepage of the web application.

#### Files and directories
  - `auctions` - main application directory.
    - `static/auctions` contains all static content.
        - `styles.css` contains compiled CSS file
       
    - `templates/auctions` contains all application templates.
        - `layout.html` - Base templates. Other templates extend it.
        - `register.html` -  The page that show the register page for user to register for a new account
        - `login.html` -  The page that show the login page for user to log in
        - `index.html` -  The homepage of the webpage, displays all the active listings
        - `create.html` -  The page that allows user to create a new listing
        - `watchlist.html` -  The page that show all the listings the user have added into the user's watchlist
        - `categories.html` -  The page that displays all the categories of the listing. 
        - `category.html` -  The page that displays all the listings of an indiviudal category
        - `sellerproduct.html` -  The page that display an individual listing where the user is the seller of the product
        - `buyerproduct.html` -  The page that display an individual listing where the user is the buyer of the product
   
    - `admin.py` -admin settings for model view
    - `forms.py` - conatins the form for creating a listing
    - `models.py` - contains the six models that I have used in the project- User, Category, Listing, Bid, Watchlist and Comment
    - `urls.py` - contains all application URLs.
    - `views.py`  contains all application views.

My project's video :https://www.youtube.com/watch?v=zC0lY9xuFRU
