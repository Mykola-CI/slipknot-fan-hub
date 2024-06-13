# Testing
## Validator Testing
### W3C HTML

Technique used for validating html in production site (heroku): 

Navigate to a page in Chrome / Chrome Inspect mode / View Page Source / Copy html / Paste to W3C html validator - direct input.

* __Info Messages__

There are html validator messages regarding trailing slash endings as  self-closing tags for the void elements. These are neither errors nor warnings. This issue has been widely covered throughout developer communities. It is said that trailing slashes may cause issues with unquoted attribute values, whereas self-closing tags are required in XHTML ([Mdn reference](https://developer.mozilla.org/en-US/docs/Glossary/Void_element)). 

I do not use unquoted attribute values, and I confirmed that these kinds of tags do not cause any bugs.

- Home page

![Home page validation](documentation/validator_slides/w3c-html/w3c-html-home.png)

- Round And About page

![Round And About page](documentation/validator_slides/w3c-html/w3c-html-about-page.png)

- All Shared Playlists page

![All Shared Playlists page](documentation/validator_slides/w3c-html/w3c-html-playlist-preview-full-list.png)

- Playlist Detail Presentation page  

![Playlist Detail Presentation page](documentation/validator_slides/w3c-html/w3c-html-playlist-presentation.png)

- Playlist Author Presentation page

![Playlist Author Presentation page](documentation/validator_slides/w3c-html/w3c-author-profile-present.png)

- User Profile page

![User Profile page](documentation/validator_slides/w3c-html/w3c-html-profile.png)

- Manage Playlists page

![Manage Playlists](documentation/validator_slides/w3c-html/w3c-html-playlist-manage.png)

- User's Playlist Detail Review page

![User's Playlist Detail Review page](documentation/validator_slides/w3c-html/w3c-html-playlist-profile.png)

- Playlist Create page

![Playlist Create page](documentation/validator_slides/w3c-html/w3c-html-create-playlist.png)

- Playlist Update page

![Playlist Update page](documentation/validator_slides/w3c-html/w3c-html-playlist-update-form.png)

- Playlist Delete page

![Playlist Delete page](documentation/validator_slides/w3c-html/w3c-html-delete-playlist.png)

- Add Playlist Item

![Add Playlist Item](documentation/validator_slides/w3c-html/w3c-html-add-song.png)

- Update Playlist Item page

![Update Playlist Item page](documentation/validator_slides/w3c-html/w3c-html-item-update.png)

- Delete Playlist Item page

![Delete Playlist Item page](documentation/validator_slides/w3c-html/w3c-html-delete-item.png)


### W3C CSS
I use 5 CSS files to serve web-pages in all applications. 

- `style.css` - accessible across all applications
- `profile.css` - serving User profile pages
- `playlist_update.css` - serving User Playlist management pages
- `core_styles` - serving Home page and Playlist Detail pages (accessible for non-logged in users)
- `base_allauth.css` - custom restyling of django-allauth pages. 

__Explanation of Errors Revealed in Validator Results:__

All of the parse errors reported by W3C CSS validator are related to 'CSS nested rules', which the validator does not yet support, the 'nested CSS' syntax being a relatively new feature. The issue has been discussed in a number of places, particularly on GitHub issues , Reddit and some other less popular blogs.

It is acknowledged that such approach as CSS nesting reduces redundancy and simplifies the management of complex styles, leading to cleaner and more organized code. Additionally, CSS nesting aligns with the principles of modular design, which is especially in demand for complex and large-scale projects.
Moreover, CSS nesting is supported by all major modern browsers: 

| Browser Name: | Full support from: | Version released in: |
| ---- | ---- | ---- |
| Chrome | version 120 | released in 2023 |
| Edge | version 120 | released in 2023 |
| Firefox | version 117 | released in 2023 |
| Safari | version 17.2 | released in 2023 |
| Opera | version 106 | released in 2023 |
| Chrome for Android | version 125 | released in 2024 |
| Safari on iOS | version 17.2 | released in 2023 |
| Samsung Internet | version 25 | released in 2024 |
| Opera Mobile | version 80 | released in 2023 |
| Firefox for Android | version 126 | released in 2024 |

[Link to 'Can I Use' reg Nesting Selector](https://caniuse.com/mdn-css_selectors_nesting)

[Using CSS Nesting Selector MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting/Using_CSS_nesting)

In order to avoid ambiguities and ensure that styles are applied as intended across different browsers I used `&` nesting selector. It is said that using the `&` nesting selector helps prevent issues with compound selectors and pseudo-classes, which can be sensitive to whitespace and other syntactical nuances

[MDN '&' Nesting selector uses](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting/Nesting_at-rules)


__Validation Results__

- style.css
![Validation report for style.css](documentation/validator_slides/w3c-css/style-css-w3c.png)

- profile.css
![Validation report for profile.css](documentation/validator_slides/w3c-css/profile-css-w3c.png)

- playlist_update.css
![Validation report for playlist_update.css](documentation/validator_slides/w3c-css/playlist-update-css-w3c.png)

- core_styles.css
![Validation report for core_styles.css](documentation/validator_slides/w3c-css/core-styles-css-w3c.png)

- base_allauth.css
![Validation report for style.css](documentation/validator_slides/w3c-css/base-allauth-css-w3c.png)


### JSHint Validator
- comments.js
![Validator screen comments.js](documentation/validator_slides/jshint-comments.png)

- item-detail-toggle.js
![Validator screen item-detail-toggle.js](documentation/validator_slides/jshint-item-detail-toggle.png)

- user-profile.js
![Validator screen user-profile.js](documentation/validator_slides/jshint-user-profile.png)

__A note on "undefined variable" warning in user_profile.js__

In fact, it is dynamically defined inside a template because external .js files do not support Django template language.

This is the snippet from `profile.html`:

~~~
{% endblock main_content %}

{% block bottom %}
<script>
    var profileUrl = '{% url "profile" %}';
</script>
<script src="{% static 'js/user-profile.js' %}"></script>
{% endblock %}
~~~

### Python Linter
I used the validator provided by the Code Institute [here](https://pep8ci.herokuapp.com/).


I have checked all python-based files on PEP8 integrity and can guarantee that there are no errors found, with one exception. These are commonly known lines in Django settings:
~~~
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
~~~

I left them unscathed for better readability. After all, according to [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/) "A Foolish Consistency is the Hobgoblin of Little Minds".

As far as there are too many python files in the project I do not deliver screenshots of successful tests here.


## Manual Testing
### SignUp and Login.



## Django Unit Testing

Due to the pressing deadline and the substantial number of files, I focused on the most complex test cases. This approach aimed to augment and enhance the outcomes of manual testing rather than duplicate the more obvious scenarios.

### User Profile AJAX-based View.
- __Testing form rendering__

| Test name | Goals |
| --- | --- |
| test_get_email_form | Checking the presence of the mock email address and the label title in the response content |
| test_post_email_form_valid | Checking if form is submitted with valid e-mail address|
| test_post_email_form_invalid | Checking if form is submitted with invalid email address to return error status |
| test_post_name_form_valid | Checking form submit for first and last name |
| test_post_dob_form_valid | Checking form submit for date of birth |
| test_post_about_form_valid | Checking form submit for 'about myself' section |
| test_post_avatar_form_valid | checking form submit for avatar upload |
| test_profile_view_unauthenticated | Testing the profile view for an unauthenticated user. I tried to simulate logging out and then accessing the profile page. Expectation is a redirect to the login page and after that to 'profile' |
| test_profile_view_authenticated | Testing the profile view for an authenticated user. I am checking the response status code and the title of the page |


![User Profile View Forms](documentation/unit_testing/profile-view-9-tests.png)

- __Testing context rendering__

| Test name | Goals |
| --- | --- |
| test_profile_context | Testing status 200, template name and rendering contexts: user_profile, playlists, email_form, password_form, name_form, dob_form, about_form, avatar_form |

![User Profile View Context](documentation/unit_testing/profile-view-contexts.png)

### User Playlist Views.

- __Playlist detail view test__

| Test name | Goals |
| --- | --- |
| test_unauthorized_user_access |  In fact, it is more testing the AuthorRequiredMixin and how it works in conjunction with the PlaylistCreatedView to restrict access of unauthorized user |
| test_context_data | Simply checking if the context data is correctly passed to the template |
| test_non_existent_playlist | Testing the case when the playlist does not exist and 404 error is raised |

![User Playlist Detail View Test](documentation/unit_testing/playlist-created-view.png)

- __Playlist update view test__

| Test name | Goals |
| --- | --- |
| test_logged_in_user_can_access_update_view |  Check if accessed by a logged-in user |
| test_non_logged_in_user_redirected_to_login | Check if NOT accessed by a non-logged-in user |
| test_non_author_user_cannot_access_update_view | Check if NOT accessed by a logged-in but not an author user |
| test_context_contains_playlist_items | Check if the context data is correctly passed to the template |
| test_valid_form_submission_updates_playlist | Test that a valid form submission updates the playlist |

![User Playlist Update View Test](documentation/unit_testing/playlist-update-view-test.png)

- __Playlist Delete View test__

| Test name | Goals |
| --- | --- |
| test_redirect_if_not_logged_in |  Ensure that only authenticated users can access the view |
| test_logged_in_uses_correct_template | Check if a logged in user gets the correct template |
| test_playlist_deletion | Test if a playlist exists after deletion and user is redirected to '/profile/' page |

![User Playlist Delete View Test](documentation/unit_testing/playlist-delete-view-test.png)


### Playlist Form Tests.
- __Form testing for create or update of a Playlist__

| Test name | Goals |
| --- | --- |
| test_form_valid_without_image | Testing if form is valid with mock user data but without image upload |
| test_form_invalid_missing_required_fields | Testing case when the required field 'title' is popped out of form_data set up in `setUp` method |
| test_form_valid_with_image | This test case concentrates on testing upload of avatar image to cloudinary. `@patch('cloudinary.uploader.upload')` is used to avoid error 'Invalid image file' |

![User Playlist Form Tests](documentation/unit_testing/playlist-form-test.png)


- __Form testing for create or update of a Playlist Item__

| Test name | Goals |
| --- | --- |
| test_form_valid_with_files | Testing if form is valid with mock user data with non-image so-called raw files upload |
| test_form_valid_without_files | Testing if valid when no files uploaded |
| test_form_invalid_missing_required_fields | Testing when the required field `song_title` is popped out from a `setUp` dataset |

![User Playlist Item Form Tests](documentation/unit_testing/playlist-item-form-test.png)

### User Profile Signal Test.

| Test name | Goals |
| --- | --- |
| test_user_profile_created | Test when a new user signs up a new related UserProfile instance is created |

![User Profile Signal Tests](documentation/unit_testing/user-profile-signal.png)

### Core Blog Views Testing.

- __Home Page View testing__

| Test name | Goals |
| --- | --- |
| test_home_view_status_code | Just checking response status 200 |
| test_home_view_template_used | Checking if a correct template is rendered |
| test_home_view_pagination | Test that the home_view returns the correct number of posts - 5 per page |
| test_home_view_pagination_second_page | Test that the home_view returns the correct number of posts per 2nd page |
| test_home_view_pagination_last_page | Testing if last page contains the expected number of posts - 3 |
| test_home_view_out_of_range_page | Tests if 9999th page is called it defaults to the last page |
| test_home_view_context_data | Test context rendering |


![Home Page View testing](documentation/unit_testing/home-view-test.png)

- __Playlist Post Detail View Testing__

| Test name | Goals |
| --- | --- |
| test_get_context_data | checking context rendering for `playlist_post`, `playlist`, `author_profile`, `playlist_items`, `comments`, `comment_count`is simulated as 1, `comment_form` is rendered, and verifies that the `liked` context variable is `False` |
| test_post_valid_comment | Logs in user and sends a POST request with valid comment data. Asserts that the response status is 302 (redirect) and the new comment is created in the database |
| test_post_invalid_comment | Logs in user and sends a POST request with invalid comment data (empty text). Asserts that the response status is 200 and the correct template is used. Checks that the invalid comment is not created and the form errors are present in the context |

![Playlist Post Detail View testing](documentation/unit_testing/playlist-post-detail-view.png)

- Comment Delete View Testing

| Test name | Goals |
| --- | --- |
| test_comment_delete_by_author |  Logs in as the author of the comment. Sends a POST request to the comment_delete view. Asserts that the comment is deleted. Checks for the success message. Verifies that the response redirects to the post detail page. |
| test_comment_delete_by_non_author | Logs in as a different user who is not the author of the comment. Sends a POST request to the comment_delete view. Asserts that the comment is not deleted. Checks for the error message. Verifies that the response redirects to the playlist post detail page.

![Comment Delete View testing](documentation/unit_testing/comment-delete-view.png)

### Testing Signal for PlaylistPost Instance


| Test name | Goals |
| --- | --- |
| test_playlist_post_created_when_published | Test if PlaylistPost instance created when Playlist is set to "Published" |
test_playlist_post_slug_set_correctly | Test if PlaylistPost instance created and slug copied from the related Playlist instance correctly. I simulated the 'create' scenario, the previous_status explicitly defined |
| test_playlist_post_deleted_when_draft | Test if PlaylistPost instance deleted when Playlist is set to "Draft" - simulating removing Playlist from blog |
| test_playlist_post_slug_updated | Test if PlaylistPost instance slug updated when Playlist slug updated |
| test_playlist_post_created_when_published_from_draft | The method name is self-explaining. If user changes `status` variable from 0 (stands for "Draft") to 1 ("Published") an appropriate `slug` value must be assigned to PlaylistPost instance `slug` field |

![Core Blog Playlist Post Signal testing](documentation/unit_testing/core-blog-signal-test.png)
