# Open edX REST API Wrapper

Python Wrapper around the [Open edX LMS/Studio](https://github.com/edx/edx-platform) REST APIs.

This work is inspired by [zoomus](https://github.com/prschmid/zoomus) (Python Wrapper around zoom.us REST APIs) and [Open edX REST API client ](https://github.com/aulasneo/openedx-rest-api-client) created by Andrés.

I shamelessly copied most of the code from Braden MacDonald's [GitHubGist](https://gist.github.com/bradenmacdonald/930c7655dca32dc648af9cb0aed4a7c5).

# Prerequisite (to be achieved on Open edX instance)

### Enable Mobile Application Features

1. In `/edx/etc/lms.yml` and `/edx/etc/studio.yml` files, add the following lines to the features section (just enable flags if already added).
    ```
    FEATURES:
        ENABLE_MOBILE_REST_API: true
        ENABLE_OAUTH2_PROVIDER: true
        ENABLE_COMBINED_LOGIN_REGISTRATION: true
    ```
2. Save the files and restart the services.

### Create a new OAuth Application

1.  Log in to the Django administration console for your base URL. For example,  `http://{your_URL}/admin`.
2. In **Django OAuth Toolkit** section select **Applications**.
3.  Select  **Add Application**. A dialog box opens with the  **Client id**  and  **Client secret**  populated for the new application.
4.  For the  **Client type**, select  **Public**.
5.  Optionally, enter a  **User**  and an identifying  **Name**.
6.  Select  **Save**.

Use above generated **Client id** and **Client secret** to create Open edX REST API Client

# Usage

```python
# Import Open edX REST API client
from openedx_api_wrapper.client import OpenedxAPIClient
# Create client with lms URL, studio URL, client_id, client_secret
client = OpenedxAPIClient(
    'http://localhost:18000',
    'http://localhost:18010',
    'client_id',
    'client_secret'
)
# Get username
client.user.get_username()
```
# Available methods
- client.user.get_username()
- client.user.get_user_details(username)
- client.user.registration({"name":"john", "username":"johnd", "email":"john.doe@example.com", "password":"edx", "country":"IN", "honor_code":True})

# Future Work
- Publish on [PyPI](https://pypi.org/)
- Add tests
- Gradually add more REST API endpoints from [edx-plafrom](https://github.com/edx/edx-platform)
