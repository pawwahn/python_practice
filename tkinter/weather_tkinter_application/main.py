import tkinter as tk
from PIL import Image, ImageTk
import requests

root = tk.Tk()

root.title("Weather App")
root.geometry("600x500")

#Key: e4277258bcb8d9fc62ad01058fba0bb5
#API URL: api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
#link: https://home.openweathermap.org/api_keys

def get_weather(city):
    weather_key = 'e4277258bcb8d9fc62ad01058fba0bb5'
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'APPID':weather_key, 'q': city, 'units':'imperial'}
    response = requests.get(url, params)
    print(response.json())
    weather = response.json()
    print(weather)
    #result['text'] = format_response(weather)

def format_response(weather):
    try:
        print(weather)
        city=weather['name']
        condition=weather['weather'][0]['description']
        temp=weather['main']['temp']
        final_str='City:{}\nCondtition:{}\nTemp:{}\n'.format(city,condition,temp)
    except:
        final_str = 'There was some problem retrieving the information for this city'
    return final_str

weather_img_path = 'D:\Pavan\sample_project\weather.jpg'

img = Image.open(weather_img_path,'r')
img = img.resize((600,500),Image.ANTIALIAS)
img_photo = ImageTk.PhotoImage(img)
bg_label = tk.Label(root,image=img_photo)
bg_label.place(x=0, y=0, width=600, height=500)

heading_title = tk.Label(bg_label, text='Earth including over 2 lakh cities',fg='red', font=('times new roman',16))
heading_title.place(x=80,y=20)

frame1 = tk.Frame(bg_label, bg='#42c2f4', bd=5)
frame1.place(x=80, y=60, width=450, height=50)

text_box = tk.Entry(frame1, font=('times new roman',23), width=17)
text_box.grid(row=0, column=0, sticky='w')

frame2 = tk.Frame(bg_label, bg='#42c2f4', bd=5)
frame2.place(x=80, y=130, width=450, height=300)

result = tk.Label(frame2, font=40, bg='white',justify='left')
result.place(relwidth=1, relheight=1)

btn=tk.Button(frame1, text='find weather', fg='green', font=('times new roman',16, 'bold'),command=lambda:get_weather(text_box.get()))
btn.grid(row=0, column=1,padx=10)

root.mainloop()