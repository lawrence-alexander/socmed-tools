def code_profile_config(user_data):
    ''' Codes Twitter profile configuration to integer '''
    ''' Codes all 8 Boolean profile attributes to decimal value '''
    ''' Takes Twitter USER JSON as input, returns positive integer in range 1-256'''
    profile_config_coded = [user_data['protected'],
                            user_data['verified'],
                            user_data['geo_enabled'],
                            user_data['contributors_enabled'],
                            user_data['profile_background_tile'],
                            user_data['profile_use_background_image'],
                            user_data['default_profile'],
                            user_data['default_profile_image']]
    binary_string = ""    
    for boolean_attribute in profile_config_coded:
        if boolean_attribute == True:
            binary_string +="1"
        else:
            binary_string+="0"
    return int(binary_string, 2) 