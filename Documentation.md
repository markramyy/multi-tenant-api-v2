## Multi-Tenants project Documentation
---

- [Config App](#config-app)
- [Core App](#core-app)
- [Tenants App](#tenants-app)
- [Items App](#items-app)

---
### Config App

---

- Houses the Django project configurations including settings, URLs, ASGI, and WSGI.

- Acts as the central configuration hub for the entire project, linking other apps.

---
#### 1. settings(Where we set the rules for how the project works)

---
1. **Database Upgrade**: Think of the database like a filing cabinet where all the project's information is stored. We switched out a small, simple filing cabinet (SQLite) for a big, secure one (PostgreSQL) that's better for handling lots of data safely and quickly. 

2. **Additional Tools**: We've added some new tools to our toolbox:
    
    - Tools for creating nice web pages (Django REST framework) that our project uses to talk to the internet.
    - A special tool (DRF Spectacular) that makes a map of all the ways our project can talk to other programs, and a pretty guidebook (Swagger) so people know how to use it.
    - A tool to connect to our big filing cabinet (psycopg2).
    - And we've made sure our project knows about the different parts we built, like the sections for managing users, the people who use our services (tenants), and the things they can do or get (items).

---

3. **Custom Sign-In**: Instead of using a generic way for people to prove who they are to use our project (like a library card), we set up our own system that uses their email.

4. **Guidebook Settings**: We set up our guidebook (Swagger) with a title and some information about what our project does, which helps people understand how to talk to our project and use its features.

---
#### 2. urls (Which is like the address book for our project)

---

- **Help Pages**: We added special pages that show a map (schema) of how everything connects and a help manual (documentation), making it easier for people to understand and use our project.

- **Organized Sections**: We made sure the web addresses for the user section and the items section are neatly organized under one main address, kind of like having different departments in a store under one roof.

- **Welcome Direction**: When someone comes to the main page of our project, we set it up to take them straight to the help manual, so they can get assistance right away instead of being lost.

---
### Core App

---
- Contains core functionality shared across the project, such as admin configurations, models, and tests.

- Likely includes base models and utility functions that are essential for the project's operation.

---
#### 1. models (Where we define the data structure)

---

- We have the customer user setup where users sign in with their email instead of a username. Their information is kept secure, and they can have different levels of access, like being an admin.

- There's also a setup for items that belong to users, like products in a store. Each product has a name, description, price, and the date it was added to the system.

---
#### 2. admin (How we manage data through a web interface)

---

- We've made a special dashboard that lets us see and manage user accounts easily, including details like their email, name, and when they last logged in.

- This dashboard also lets us add new users and edit existing ones, including setting up their access rights.

---
#### 3. test_models (Checking that everything works)

---

- We run tests to make sure that when we create a new user account with an email, it's set up correctly, the email looks right, and the user's password is secure.

- We also check that we can create a superuser (an admin with all access) properly, and that our product setup works, meaning we can add a new product and its details are saved correctly.

---
#### 4. test_admin (Making sure the admin dashboard works)

---

- Before we let anyone use the admin dashboard, we make sure it's working. We test logging in as an admin, looking at the list of users, and checking that we can edit a user's details or create a new user without any hiccups.

---
### Tenants App

---

- Manages the tenant-specific aspects, facilitating a multi-tenancy architecture with its own views, serializers, and URLs.

- Provides the logic for tenant separation, data isolation, and tenant-specific operations.

---
#### 1. serializers (Where we define how tenant data is converted to and from JSON)

---

- We have a tool that helps us take tenant information, like their email and password, and safely turn it into a format that our system can store and understand.

- There's a secure process to check if a tenant's email and password are correct, giving them a special key that proves they are who they say they are.

---
#### 2. views (How we set up the tenant web pages)

---

- We've created special web pages that allow new tenants to sign up, existing tenants to get their special access key, and tenants to see or update their own information.

- These pages make sure that only tenants who have proven their identity can see or change their personal details.

---
#### 3. urls (The map to our tenants' web pages)

---

- It's like a signpost that guides you to different web pages: one for signing up as a new tenant, one for logging in, and one for tenants to look at and change their own information.

---
#### 4. test_tenant_api (Our checklist to make sure the tenant features work)

---

- We have a series of checks to ensure tenants can sign up with a proper email and password, and they can't sign up with an email that's already taken or a password that's too short.

- We also make sure that when tenants put in their correct email and password, they get their special access key, and if they put in the wrong information, they don't get the key.

- Tests are in place to ensure that tenants must be logged in to see or change their information, and that they can indeed update their information correctly when they are.

---
### Items App

---

- Manages the item-related features of the project, with dedicated views, serializers, and URLs.

- Handles item-specific operations, possibly providing APIs for item creation, retrieval, update, and deletion (**CRUD**).

---
#### 1. serializer (How we format item data)

---

- We set up a system to neatly arrange item information, such as the item's name and price, into a digital format that's easy for everyone to read and understand.

- There's also a special format for when we need more detailed information about an item, like its full description, for times when someone wants to learn more about a specific product.

---
#### 2. views (Where we control what you can do with items)

---

- We created a digital storefront where items can be added, viewed, updated, or removed, but only by people who have proven they're part of the shop (authenticated users).

- This storefront makes sure that shopkeepers can only see and manage their own items, keeping everything organized and secure.

---
#### 3. urls (The directory of our digital storefront)

---

- It's like a mall directory that helps you find where to add a new item to your shop, look at all the items you have, or get more details about a specific item

---
#### 4. test_item_api (Our quality check for the digital storefront)

---

- We run several tests to make sure that only shopkeepers who have identified themselves can see and manage their items.

- We check that items can be added correctly, that shopkeepers can only see their own items, and that they can update or remove an item as needed.

- We also make sure that shopkeepers can't accidentally change which shop an item belongs to or remove someone else's item.

---
