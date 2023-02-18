

def generate_user_code():
    from django.contrib.auth import get_user_model   
    User = get_user_model()                          

    last_customer = User.objects.order_by('id').last()       
    
    if not last_customer:
        return 'USR10001'
    user_code = last_customer.user_code
    user_code_int = int(user_code.split('USR')[-1])
    new_user_code_int = user_code_int + 1
    new_user_code = 'USR' + str(new_user_code_int) 

    return new_user_code