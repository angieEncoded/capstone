# TabiCRM - Capstone project for CS50 Web

## Distinctiveness and Complexity
- Distinctiveness
  - For my project I built a trouble Ticketing CRM that can be used by a typical IT shop. 
  - It's designed to solve some problems that the current CRM system my company is using (vTiger, a fork of SugarCRM) doesn't. 
  - That system was built with a sales force in mind. I designed this to work better for a help desk. 
- Complexity
  - The current items that this system will track are as follows:
    - Customer details
      - Contacts associated with customers
      - Licenses (For Example, Microsoft Office keys) associated with customers
        - Licenses can be a text key or a file upload
      - Equipment (servers, desktops, routers) associated with customers
      - Tickets associated with customers
        - Comments associated with tickets
        - History entries associated with tickets
- What's inside - a list of folders and files top to bottom
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
                - This has all the front end logic for quickly managing data about the contacts
              - manageCustomer.js
                - This has all the front end logic for quickly managing data about the customer
            - viewFunctions
              - viewContact.js
                - This has all the front end logic to show the component with Contact details
              - viewCustomer.js
                - This has all the front end logic to populate the customer quick information modal 
              - viewOpenTicketForm.js
                - This has all the front end logic for quickly opening a new ticket for a customer
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
            - display_contacts - shows a table of all contacts associated with the target customer
            - display_equipment - shows a table of all equipment associated with the target customer
            - display_licenses - shows a table of all licenses associated with the target customer
            - display_tickets - shows a table of all tickets associated with the target customer
            - full_edit_contact - django form for editing contacts
            - full_edit_equipment - django form for editing equipment
            - full_edit_licenses - django form for editing licenses
            - full_edit_tickets - django form for editing tickets
          - partials - This folder has some partial includes that may be shared across pages
            - customer_buttons.html - buttons that open modals for adding items to the customer (contact, license, equipment, ticket)
            - customer_nav.html - Shared navigation tabs for the full forms section of the site
          - add_customer.html - the form to add a new customer
          - all_customers.html - a table showing all currently configured customers in the system
            - This has logic that allows a user to click on a customer which will result in a modal interface that has the customer data, the contacts, licenses, and equipment associated with that customer
            - Some of the items can be 'quick edited' here on the front end - all customer and contact data could be updated from here
            - If there is a record of the customer having a license file, that file can be downloaded from here
            - The user can open a ticket for the customer from this interface
            - The user can click through to go to the full customer details section 
          - customer_full_form.html
            - This holds the full customer logic. The user can click a button to switch to the full edit view, but normally if someone is coming to this page it's because they want to do something with the equipment or the licenses. 
          - index.html
            - This is the landing page which currently will show the user tickets that are in the queue (Status != closed && owned_by == None)
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
        - I ended up learning how to refactor the views.py file into separate files. This project became too unweildy to keep all the routes in one file
        - __init__.py
          - This is the 'entry point' for all the files - this file imports them and then the urls.py can grab from here
        - contact.py - This file holds all my python logic for the contacts
        - customer.py - This file holds all my python logic for the customers
        - equipment.py - This file holds all my python logic for the equipment
        - index.py - This file holds all my python logic for the initial index page. I kept this separate with the intention of expanding the 'dashboard' in the future.
        - license.py - This file holds all my python logic for the licenses
        - login.py - This file holds all my python logic for the login and logout processes. Really, this was default Django stuff that I grabbed from an earlier project.
        - ticket.py - This file holds all my python logic for the tickets
      - admin.py - all my custom display logic for the django admin program
      - forms.py
        - All my custom form logic is in here 
        - I started using the class meta style of creating these forms after learning how to use it when solving an unrelated problem.
        - This contains six forms and one additional helper class
          - form for new customers
          - form for new contacts
          - form for new licenses
          - form for new equipment
          - form for new tickets
          - form for new comments on a ticket
          - and a date input helper class to provide a date widget since django forms doesn't seem to have this built in...
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
- How to run the application
  - This is a standard Django app. Clone the repository from the github page. There's a db attached with starter junk data that can be used
    - admin credentials are admin\admin
    - user credentials are angie\angie
  - Or delete it, run ```python manage.py migrate``` to create a new one
  - 
- Any additional information
  - I actually had to sit down and have a serious talk with myself about scope creep on this one. 
  - For the purposes of this software actually being used - I have a lot more features planned and there are so many cool things it could do and track, additional fields to add to customers, tickets, etc...
  - For the purposes of actually turning in a project for this class, I had to cut it off where I did and at the level of detail I did. 
  - I had a lot of fun on this project and in this class. I am extremely grateful to Harvard for making some of these classes available to those of us who didn't have an opportunity to study at the legendary school itself. 
  - Thank you very much for considering my submission, and I hope you have a wonderful year!
- Any additional packages in a requirements.txt
  - I wasn't 100% sure what this meant (which of course means I don't have anything extra), so I did a search and found this site
    - http://www.learningaboutelectronics.com/Articles/How-to-create-a-requirements-txt-file-for-a-Django-project.php
    - I performed the ```pip freeze > requirements.txt``` which listed all the packages
    - They should all be default - I did not have to install anything additional for this to work, just imported from what came with django.





remember installed humanize package
django serializers package to serialize the json
json package to respond with json
import the re package
imported ModelForm to use the select fields
imported from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone for the form field to default to


Under its own header within the README called Distinctiveness and Complexity: Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.
What’s contained in each file you created.
How to run your application.
Any other additional information the staff should know about your project.
Added jquery and datatables plugin for the pagination and search features on the front end
changed the timezone to America/New_York for timestamps proper
<!-- added this "from django.db.models import Q" in order to do queries on multiple statuses --> not needed ended up using except
added import os to be able to unlink files