import numpy as np

def closest_value(input_list, input_value):
 
  arr = np.asarray(input_list)
 
  i = (np.abs(arr - input_value)).argmin()
 
  return arr[i]



# est = pytz.timezone('US/Eastern')
# time = time_sales[1].get('datetime')
# a = datetime.fromisoformat(time[:-1]).astimezone(est)
# print(a.hour,":",a.minute)
