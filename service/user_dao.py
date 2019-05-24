import logging
from dao_helper import get_all_objects, make_request, GRAPH_URL

RESOURCE_PATH = '/users/'


def create_user_from_array(user_data_array):
    def __try_create(user_data):
        """
        Internal function to create user
        :param user_data: json object with user details
        :return: void
        """
        logging.info(f'trying to create user {user_data.get("userPrincipalName")}')
        make_request(f'{GRAPH_URL}{RESOURCE_PATH}', 'POST', user_data)
        logging.info(f'user {user_data.get("userPrincipalName")} created successfully')

    def __try_update(user_data):
        """
        Internal function to update user
        Update user with passwordProfile is not possible without Directory.AccessAsUser.All
        which is not exist in "application" permission so we need to remove this part if exist
        :param user_data: json object with user details, must contain user identifier
        (id or userPrincipalName property)
        :return: void
        """
        user_id = user_data['id'] if user_data.get('id') else user_data['userPrincipalName']

        if not user_id:
            raise Exception("Couldn't find id for user, at least id or userPrincipalName needed")

        if user_data.get('passwordProfile'):
            del user_data['passwordProfile']

        logging.info(f'trying to update user {user_data.get("userPrincipalName")}')
        make_request(f'{GRAPH_URL}{RESOURCE_PATH}{user_id}', 'PATCH', user_data)
        logging.info(f'user {user_data.get("userPrincipalName")} updated successfully')

    for user in user_data_array:
        try:
            __try_create(user)
        except Exception as e:
            print(e)
            __try_update(user)


def get_all_users(delta=None):
    """
    Fetch and stream back users from Azure AD via MS Graph API
    :param delta: delta token from last request
    :return: generated JSON output with all fetched users
    """
    yield from get_all_objects(f'{RESOURCE_PATH}delta', delta)
