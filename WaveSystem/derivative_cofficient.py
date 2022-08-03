from function_value import getvalue_function

def derivative_cofficient(listof_data):
    function=listof_data[0]
    x_value=listof_data[1]
    notation=listof_data[2]
    delta_x=0.00001
    if notation>0:
        d_fx=(derivative_cofficient([function,(x_value+delta_x),notation-1])-derivative_cofficient([function,(x_value),notation-1]))/delta_x

    elif notation==0:
        d_fx=getvalue_function(function,x_value)

    return d_fx


