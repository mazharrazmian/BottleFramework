from bottle import run, route , template, static_file,request,get,post
import requests, json
import sqlite3
import sys
"""Adding a path for static files to link them with my templates"""
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename,root='./static')

""" Creating an index page, which is where the user will land upon accesing the site"""
@route('/', method='get')
def index():
    return template('index')



"""Ajax requests and from data from index.js will be handled here"""
@route('/',method='post')
def filter_data():

  #getting values of form fields from the request
    city = request.POST.get('city')
    city2 = request.POST.get('city2')
    
  #requesting the API to fetch data and then storing it, APPID in the url is the API key
    city_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID=a177cd96746098695c1234fa679d306c'
    r = requests.get(url=city_url)
    city_json=r.json()
    city2_url =f'http://api.openweathermap.org/data/2.5/weather?q={city2}&units=imperial&APPID=a177cd96746098695c1234fa679d306c'
    req = requests.get(url=city2_url)
    city2_json = req.json()

    """Returning ERROR if the status code is not 200, i.e if the response is invalid"""
    if city_json['cod'] != 200:
      return city_json
    elif city2_json['cod'] != 200:
      return city2_json

    """Filtering the API data and sending the Filtered data to the client side"""
    city_data = {
      'cod': city_json['cod'],
      'name' : city_json['name'],
      'temp' : city_json['main']['temp'],
      'pressure': city_json['main']['pressure'],
      'humidity' : city_json['main']['humidity'],
      'wind_speed' : city_json['wind']['speed'],
    }
    city2_data = {
      'cod': city2_json['cod'],
      'name' : city2_json['name'],
      'temp' : city2_json['main']['temp'],
      'pressure': city2_json['main']['pressure'],
      'humidity' : city2_json['main']['humidity'],
      'wind_speed' : city2_json['wind']['speed'],
    }
    
    filtered_data = []
    filtered_data.append(city_data)
    filtered_data.append(city2_data)
    return json.dumps(filtered_data)
    




""" Function for storing the comments in database and displaying them when needed"""

@route('/comments',method='POST')
def post_comments():

    #getting the name and comment of the user from request
    comment = request.POST.get('comment')
    name = request.POST.get('name')
    #connect the database
    con = sqlite3.connect('data\\comments.dat')
    cur = con.cursor()
    rec = cur.execute('INSERT INTO comments VALUES(null,?,?)',(comment,name))
    con.commit()
    context = cur.execute('SELECT * FROM comments')
    return template('comments',context= context)

# Display all comments if the user just wants to read them
@route('/comments',method="GET")
def get_comments():
    con = sqlite3.connect('data\\comments.dat')
    cur = con.cursor()
    context = cur.execute('SELECT * FROM comments')
    return template('comments',context= context)


@route('/forecast',method='get')
def get_forecast():
  return template('forecast')

        """Function to handle form data entered by the user to forecast"""
@route('/forecast',method='post')
def post_forecast():      
    #requesting the API to fetch data and then storing it, APPID in the url is the API key
    city = request.POST.get('city')
    city2 = request.POST.get('city2')
    city_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=imperial&APPID=a177cd96746098695c1234fa679d306c'
    r = requests.get(url=city_url)
    city_json=r.json()
    city2_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city2}&units=imperial&APPID=a177cd96746098695c1234fa679d306c'
    req = requests.get(url=city2_url)
    city2_json = req.json()
    
   

    """Filtering the returned data to send limited data to the client"""
    city_data=[]
    city2_data=[]
    filtered_data=[]

    #Collecting data with gap of 24 hours in the for loops, the API returns 5 days of data with
    # gap of 3 hours. This gives us 5 datasets for 5 days for each city
    index = 0
    for item in city_json['list']:
      if index%8 == 0:
        city_data.append(item)
      else:
        pass
      index=index+1
      
    
    index = 0
    for item in city2_json['list']:
      print(index%8)
      if index%8 == 0:
        city2_data.append(item)
      else:
        pass
      index=index+1
    
      
    filtered_data.append(city_data)
    filtered_data.append(city2_data)
    return json.dumps(filtered_data)
    
if __name__ == '__main__':
  run(host='127.0.0.1',port=8000,debug=True,reloader= True)