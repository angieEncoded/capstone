# TabiCRM - Capstone project for CS50 Web

## Distinctiveness and Complexity
### Distinctiveness

- For my project I built a Trouble Ticketing CRM that can be used by a typical IT shop. 
- It's designed to solve some problems that the current CRM system my company is using (vTiger, a fork of SugarCRM) doesn't. 
- That system was built with a sales force in mind. I designed this to work better for a help desk.
 
### Complexity
- The current items that this system will track are as follows:
  - Customer details
    - Contacts associated with customers
    - Licenses (For Example, Microsoft Office keys) associated with customers
      - Licenses can be a text key or a file upload
    - Equipment (servers, desktops, routers with their IP, serial, OS information) associated with customers
    - Trouble Tickets associated with customers through various stages of completion
      - Comments associated with tickets
      - History entries associated with tickets
  
## What's inside - a list of folders and files top to bottom
- archives
  - This folder has files that are either on standby or that were rejected from the project as development wore on. 
  - I keep my 'scratchpad' data in here if I need to swap out code
  - There is nothing here of particular importance to the system currently running
- capstone
  - The main Django project 
  - settings.py
    - I added MESSAGE_TAGS in here so I could take advantage of the flash messaging system
      - This works in conjunction with "from django.contrib import messages"
    - I added "'django.contrib.humanize'" to the installed apps in order to nicely format some of the front-end items
    - I added "AUTH_USER_MODEL = 'tabicrm.User'" since I made some changes to the base User class
    - I added "LOGIN_URL = '/login/'" to make the login decorator work correctly
  - urls.py
    - There is only the single app as part of this project. One url to tabicrm (path("", include("tabicrm.urls")))
-  favicon_io
   -  This folder contains the favicons I generated for this project
-  licenses
   -  This folder holds any uploaded licenses for the customers 
   -  The system will separate them into folders by month_day_year
-  tabicrm - the main application
   - migrations 
      - The django migration files needed to set up the database
    - static
      - tabicrm
        - images
          - favicon.ico - the favicon in use
        - javascript - all the js files
          - manageFunctions
            - manageContacts.js
              - This has all the front end logic for quickly managing data about the contacts. 
              - The functions in here allow the user to update individual fields directly from the front end without needing to go to the full form
            - manageCustomer.js
              - This has all the front end logic for quickly managing data about the customer
              - This is much the same as the contacts javascript - allows the user to edit individual fields from the front end modal display. 
              - The idea behind this is most of the time, folks taking calls will be opening tickets for the tech team to deal with, but they might take a call requesting an update to the address or something simple that doesn't require escalation. They can edit those simple fields right there. 
          - viewFunctions
            - viewContact.js
              - This has all the front end logic to show the component with Contact details
            - viewCustomer.js
              - This has all the front end logic to populate the customer quick information modal. 
              - The modal is generated on the fly when a user clicks on a customer from the table. 
            - viewOpenTicketForm.js
              - This has all the front end logic for quickly opening a new ticket for a customer
              - It's the same as the full form but handled on the front end for the tier I help desk folks to quickly be able to get a ticket opened
          - jquery3_6_0.js
            - jquery is here for the data tables plugin that nicely formats tables on the front end
          - modals.js
            - This has front end logic for creating the various modals that are in use throughout the site
          - utility.js
            - This holds some other logic that didn't really fit in any of the other classifications - like getting the csfr token and such
        - styles.css
          - This file has my custom styles, bootstrap overrides, etc. This project uses Bootstrap 5.
    - templates - my django templates folder
      - tabicrm
        - full_forms - This folder has templates that are exclusively django template generated
          - display_contacts.html - shows a table of all contacts associated with the target customer
          - display_equipment.html - shows a table of all equipment associated with the target customer
          - display_licenses.html - shows a table of all licenses associated with the target customer
          - display_tickets.html - shows a table of all tickets associated with the target customer
          - full_edit_contact.html - django form for editing contacts
          - full_edit_equipment.html - django form for editing equipment
          - full_edit_licenses.html - django form for editing licenses
          - full_edit_tickets.html - django form for editing tickets
        - partials - This folder has some partial includes that may be shared across pages
          - customer_buttons.html - buttons that open modals for adding items to the customer (contact, license, equipment, ticket)
          - customer_nav.html - Shared navigation tabs for the full forms section of the site
        - add_customer.html - the django form to add a new customer
        - all_customers.html - a table showing all currently configured customers in the system
          - This has logic that allows a user to click on a customer which will result in a modal interface that has the customer data, the contacts, licenses, and equipment associated with that customer
          - Some of the items can be 'quick edited' here on the front end - all customer and contact data could be updated from here (see javascript notes above)
          - If there is a record of the customer having a license file, that file can be downloaded from here
          - The user can open a ticket for the customer from this interface
          - The user can click through to go to the full customer details section 
        - customer_full_form.html
          - This holds the full customer logic. The user can click a button to switch to the full edit view which will swap to the django form, but normally if someone is coming to this page it's because they want to do something with the equipment or the licenses. 
        - index.html
          - This is the landing page which currently will show the user tickets that are in the queue (status != closed && owned_by == None)
          - This will also show the user their own open tickets
        - layout.html 
          - The basic boilerplate 
          - I'm using some google fonts, bootstrap 5, line awesome for icons and all my javascript and jquery includes are in here
        - login.html
          - The basic login page
    - util - my utility classes
      - angie.py
        - I work with Javascript a lot more, and console.log is in my muscle memory. So at almost the beginning of the course I wrote this little class to translate print() to console.log()
    - views
      - I ended up learning how to refactor the views.py file into separate files. This project became too unweildy to keep all the routes in one views.py file
      - __init__.py
        - This is the 'entry point' for all the files - this file imports them and then the urls.py can grab from here
      - contact.py - This file holds all my python logic for the contacts
        - I imported JsonResponse, serializers, json and re into this file so I could respond to the front end javascript with json
        - re is used as a quick check that we're getting only the allowed characters. 
        - this file also imports the messages package to take advantage of flash messaging
      - customer.py - This file holds all my python logic for the customers
        - This imports all the same packages as contact.py and uses them in much the same way
      - equipment.py - This file holds all my python logic for the equipment
        - I didn't need json or re in this one because there is no front-end interface for editing equipment. The thought process behind this is the only folks who will be editing equipment are the next level technicians who will be working more deeply in the system. The first level of phone support isn't going to be making adjustments to the customer's equipment, they will open a ticket for a tech to look into it. 
      - index.py - This file holds all my python logic for the initial index page. I kept this separate with the intention of expanding the 'dashboard' in the future.
      - license.py - This file holds all my python logic for the licenses
        - This one has an additional import - os
        - I added this in order to manage the license files attached to the system. Django out of the box allows for uploading files and deleting files when the model forms are processed, but in order to change an uploaded file, for example in the case the user clicked the wrong file, I needed to manage that logic myself. 
        - So the edit route will check if a file was recorded, and then unlink the file if there was one.
      - login.py - This file holds all my python logic for the login and logout processes. Really, this was default Django stuff that I grabbed from an earlier project. It's as boilerplate as it gets. 
      - ticket.py - This file holds all my python logic for the tickets
        - there aren't any json imports in here - ticket logic is handled almost exclusively through the django forms
        - There IS some front end logic to send requests but all requests are redirected afterward to the main ticket form. I did this in some places, like this one, because we lose the power of the Django system if we run everything from the front end. I like SPAs, but in some cases I just don't feel it's necessary to lose the power of the framework's design just to avoid a page refresh. 
    - admin.py - all my custom display logic for the django admin program
      - I imported UserAdmin to be able to adjust passwords from the admin interface. I also set up a custom user admin class here to be able to adjust the user class. There is no interface in the app to add users - that is a task for the administrator of the system. So I wanted to make sure that all the fields could be managed from the admin interface. 
    - forms.py
      - All my custom form logic is in here - this is where I really started having a lot of fun with the system
      - I started using the class meta style with ModelForms to take advantage of the more powerful select features
        - form for new customers
        - form for new contacts
        - form for new licenses
        - form for new equipment
        - form for new tickets
        - form for new comments on a ticket
        - and a date input helper class to provide a date widget since django forms doesn't seem to have this built in. 
    - models.py
      - This holds all my models and some additional helper classes to automatically populate some data for the forms
      - I imported timezone in order to set up an automatic three year add on to the date. Most of the licenses we sell are on a three year renewal period, so I thought it would be handy for it to be auto populated for the users. 
      - There is a User class that I expanded to have additional fields
      - The customer class is pretty basic
      - As is the contact class
      - The License class is where it gets interesting. So I built in fields here to automatically populate the drop down menus the forms will have. In this case, there are choices for license types automatically populated. For the date fields in expiration_date and end_of_life I added my helper class default date
      - The Equipment class is much the same, with a variety of equipment that will automatically populate the form. 
      - The ticket class is the most complex with several different places where a menu selection was appropriate.
      - Ticket comments and ticket history are pretty basic classes. 
    - urls.py
      - This contains some 30+ routes for performing various tasks in the system.
        - After about route 20, I realized that '<int:id>' was way too ambiguous, since I have customer ids and ticket ids and contact ids and so forth, so I changed everything to specifically identify which kind of id is expected

## How to run the application
- To run the application with the 'starter data' database
  - Clone the repository from the github page. There's a db attached with starter junk data that can be used - you will see the same data as was in the video at the time of recording
    - admin credentials are admin\admin
    - user credentials are angie\tabicrm1
  - run the server with ```python manage.py runserver``` 
  - navigate to http://localhost:8000 to use the system!
- To run the application with a fresh database
  - delete the db.sqlite3 file
  - run ```python manage.py migrate``` to migrate the database changes to a new one
  - create a new superuser with ```python manage.py createsuperuser```
  - run the system with ```python manage.py runserver```
  - log into the admin program at http://localhost:8000/admin and create a new system user
  - log into the system at http://localhost:8000 and enjoy using the application!

## Any additional information
- I actually had to sit down and have a serious talk with myself about scope creep on this one. 
- For the purposes of this software actually being used - I have a lot more features planned and there are so many cool things it could do and track, additional fields to add to customers, tickets. I want to add additional views where users can sort all tickets by status, generate reports on tickets and equipment, generate invoices, prepare quotes... So many things this system will be able to do!
- For the purposes of actually turning in a project for this class, I had to cut it off where I did and at the level of detail I did. 
- I had a lot of fun on this project and in this class. I am extremely grateful to Harvard for making some of these classes available to those of us who didn't have an opportunity to study at the legendary school itself. 
- Thank you very much for considering my submission, and I hope you have a wonderful year!

## Any additional packages in a requirements.txt
- I wasn't 100% sure what this meant (which I guess means I don't have anything extra and this didn't apply), so I did a search and found this site
  - http://www.learningaboutelectronics.com/Articles/How-to-create-a-requirements-txt-file-for-a-Django-project.php
  - I performed the ```pip freeze > requirements.txt``` which listed all the packages this project uses
  - They should all be default - I did not have to install anything additional for this to work, just imported from what came with django and worked with that