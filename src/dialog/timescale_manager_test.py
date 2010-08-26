
"""
 Created by Chouayakh Mahdi                                                       
 26/08/2010                                                                       
 The package contains the unit test of timescale_manager function                                       
    unit_tests : to perform unit tests                                           
"""


def print_time(time):
    print time['year']+'/'+time['month']+'/'+time['day']
    print time['hour']+':'+time['minute']+':'+time['second']
    
    
def timescale_unit_tests():
    time={'year':'2010','month':'August','day':'26','hour':'14','minute':'50','second':'30'}
    print_time(time)

if __name__ == '__main__':
    timescale_unit_tests()