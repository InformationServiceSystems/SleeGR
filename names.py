from collections import namedtuple

User_type_names = namedtuple('User_type_names', ['user_general', 'user_fitness', 'user_trainer', ])
Service_type_names = namedtuple('Service_type_names', ['service_general', 'service_user_map'])
service_type_names = Service_type_names('general_service', 'user_map_service')
user_type_names = User_type_names('general_user', 'fitness_user', 'user_trainer')

type = '_type'

user_type = 'user_type'
first_name = 'first_name'
last_name = 'last_name'
email = 'email'
password = 'password'

birthday = 'birthday'
height = 'height'
weight = 'weight'
general_user_id = 'general_user_id'

service_name = 'service_name'
service_allowed_users = 'allowed_users'

service_id = 'service_id'

user_id = 'user_id'
