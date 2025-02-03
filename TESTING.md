# Testing

The deployed project live link is [Travel Buddy]()
This application was extensively tested via automatic and manual tests these are detailed below 


## Brief Intro
The testing of this application came in three parts, as the testing was extensive and covered varying different
aspects of the code base i decided to opt for a non standard structure and created a testing folder. 

Inside this folder you will find the test files, the testing.md as well as the validation images which
can be seen later in this document.


## Automatic Testing
As the name implies this is testing that was done automatically via the inbuilt django tests or 
the code validation websites. I'll break the two of these up into subcategories.

### Automatic tests


### Validation

#### PEP8 Python Validation

<details>
<summary><strong style="color:yellow"></strong></summary>

</details>

<details>
<summary><strong style="color:yellow"></strong></summary>

</details>

<details>
<summary><strong style="color:yellow"></strong></summary>

</details>

<details>
<summary><strong style="color:yellow"></strong></summary>

</details>

#### JS validation



#### HTML CSS Validation


<details>
<summary><strong style="color:green"></strong></summary>

</details>

<details>
<summary><strong style="color:green"></strong></summary>

</details>

<details>
<summary><strong style="color:green"></strong></summary>

</details>

<details>
<summary><strong style="color:green"></strong></summary>

</details>

## Manual Testing
Manual testing was undertaken in a variety of ways, these included firstly building tests
to test each part of the code base. These are detailed more in the test.py files, as well as
this we tested the responsive design on browsers for clipping or design errors and finally
ran through a batter of manual tests and expected behaviour tests. These are detailed below

### Manually built tests
The manually built tests were designed to do the following:

### Browser Tests
The game was tested on a variety of browsers:

- Chrome
- Edge
- Firefox
- Opera
- Safari

Result:


### Expected Behaviours

| **Feature**              | **Action**                                                                | **Expected Result**                         | **Actual Result** |
| ------------------------ | ------------------------------------------------------------------------- | ------------------------------------------- | ----------------- |
|


### EXTRA TESTS


#### Testing logged out view

One of the biggest issues i ran into was the fact that in dev mode i was always treat as loggin in or authenticated, the only way to fix this was to 
clear my session cache, to simulate a logged out state i utilized a global variable that we could manually apply to force a logged out state:

In travel_buddy.settings

```py
ANON_MODE = True
```

Then whenever i needed to see if a feature appeared or disappeared with a toggle i could add it to the is_authenticated conditionals, this 
helped immensely especially in the early versions as I had not gotten login and signup ready

```py
{% if user.is_authenticated and settings.ANON_MODE %}
```

As we managed to get login systems online I moved to a more django form of testing and cleared my sessions followed by setting up test users, this
was achieved with the following steps:

```py
1/  python manage.py shell

2/  from django.contrib.sessions.models import Session
    Session.objects.all().delete()

3/  python manage.py createsuperuser
    python manage.py shell

4/  from django.contrib.auth.models import User
    User.objects.create_user(username='testuser', email='test@example.com', password='password123')
```

#### Testing Email Sending

I wanted to get the login / logout signup up and running early so that we could create proper views based on user login status, however i did not
want to flood user emails, so to simulate and test email sending with core components i found that adding console rather than smtp (django docs)
i was able to send email information to the console instead so i could get realtime feedback without having to send emails 

```py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

![alt text](test_images/django_shell_email_test.png)

Utilizing the django shell and the test backkend var we tested to see if errors would be raised when emailing the recipient, this 
raised 1 error where we were not using a secure enough account, after enabling two factor and an app password this was no longer 
raised.

Following this i tested sending multiple emails to various accounts to full successes all around

## BUG Fixing
As this was built as a small scale project and django is still relativly fresh to me there was
sadly bound to be present, all known bugs are listed below, for fixing purposes at a later date

### Known Bugs


<br>


### [BACK TO README](https://github.com/shaAnder/travel_buddy/blob/main/README.md)

# Testing

As each section or Function/Model was built during this project, I was testing for functionality and styling issues that may have arisen (see table below), which were corrected or fixed before continuing. I also had friends test the site by signing up, adding and deleting comments using various devices on varying platforms (IOS, Android, Mobile, Tablet etc) and reporting back any issues they encountered with functionality or styling.

## Manual Testing

*For any Fails, there is a more detailed description below the table*

ADMIN
| TEST | OUTCOME | PASS/FAIL|
|:---:|:---:|:---:|
| Create Blog Post | Post successfully created and displayed | Pass |
| Edit Blog Post | Error thrown when editing post title & slug (*) | FAIL |
| Edit Blog Post (after fix) | Post content and category updated successfully | Pass |
| Delete User Comments | Comment deleted successfully | Pass |
| Delete Blog Post | Post deleted successfully | Pass |
| Create 7 Test Posts to check Pagination | Next/Previous Page Appears at bottom of screen | Pass |

(*) - While testing the ability to edit posts (Limited to Admin only), I had a problem when editing the title and slug of the post. This was due to the URL not being able to find the original slug of the post (because it had been changed during the edit) to route it after the editing was complete. At this stage, I felt the easiest fix was to remove the ability to edit the post title and slug in the browser, but this functionality is still available via the django admin panel.

## User

| TEST | OUTCOME | PASS/FAIL|
|:---:|:---:|:---:|
| Create Account | Created successfully | Pass |
| Error Check - Error page when signing up with email address | Unable to replicate(*) | Closed |
| Login | Login Successful | Pass |
| Logout | Logout Successful | Pass |
| Read Full Blog Post | PostDetail page loaded successfully | Pass |
| Add Comment under Blogpost | Comment Added Successfully | Pass |
| Delete Comment | Comment Deleted | Pass |
| Filter Posts by category | Posts marked as selected category displayed successfully | Pass |
| Create User Account to check access to restricted pages (add_post, add_category)| Page displayed correct error message, with no access to restricted content | Pass |

(*) See Bugs below

## Bugs

One of my users reported that they were unable to sign up when including an email address (although the inclusion of an email address is not required), but myself and others were unable to replicate this issue so the bug was marked as closed.

At different points throughout this project, I encountered various bugs involving the styling. These usually appeared after adding a new section or template page. These were all fixed using Bootstrap classes or custom CSS to override any issues caused by Bootstrap itself.

Towards the end of completion, I had an issue with the database, where I had made a change to the Post Model, but hadn't migrated the changes after undoing the changes in the code relating to that change. This required me to reset the database, which was done with help from Rebecca via the Code Institute's Tutor Support. The changes related to the Category Model and the choices available when creating an account.

To enable me to reset the database, I first had to comment out the code (related to "choices" in the model) to stop the code being run and causing an error. Once this was done, the database was reset, seemingly without issue.

Then I had a problem with the "Create a Post" page. When adding a new blog post via the browser, the images were not being sent to cloudinary for cloud storage, and the ElephantSQL cloud database was also not recieving any data. This was a very simple fix as I needed to add ```enctype="multipart/form-data"``` into the form element.

## Lighthouse

The performance scores appear to be low, and I believe this is due to the images uploaded for each blog post being hosted on a third-party cloud-based platform.

Mobile

![Lighthouse Mobile Score](documentation/images/lighthouse_mobile.png)

Desktop

![Lighthouse Desktop Score](documentation/images/lighthouse_desktop.png)

## Validation Testing

### HTML & CSS

HTML & CSS testing was completed using [W3 Validator](https://validator.w3.org/)

When validating the code, I had the error shown below. this was fixed by removing the button and using Bootstrap styles to display the link as a button instead

![HTML Validation - Descendant Error](documentation/testing_documentation/validation/base.html_button_descendant.png)

Fixed:

![HTML Validation Complete- base.html](documentation/testing_documentation/validation/index.html_validation_complete.png)

## Python Testing

Python pep8 validation was done via [Code Institute's Python Linter](https://pep8ci.herokuapp.com/)

The only errors recieved here were where some lines of text exceeded the limit of 79 characters, but these have now been rectified.

Python Files Tested:

- models
- forms
- views
- urls
