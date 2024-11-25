import requests
import tkinter as tk
from tkinter import messagebox, Toplevel
from tkinter import ttk
from datetime import datetime, timedelta
from PIL import Image, ImageTk  

# API Key
api_key = os.getenv('OPENWEATHER_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the 'OPENWEATHER_API_KEY' environment variable.")

# List to store recent searches
recent_searches = []
icon_image = None  # Global variable to store the image

# Function to fetch and display weather data, including local time and icon
def get_weather(city=None):
    global icon_image  # To ensure we keep a reference to the image and it doesn't get garbage collected
    
    if city is None:
        city = city_entry.get().strip()

    if not city.replace(' ', '').isalpha():
        messagebox.showerror("Input Error", "City names must contain only letters.")
        return

    try:
        # Fetch weather data
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}")
        weather_data.raise_for_status()

        # Extract weather data
        weather = weather_data.json()['weather'][0]['description'].capitalize()
        temp = round(weather_data.json()['main']['temp'])
        feels_like = round(weather_data.json()['main']['feels_like'])
        humidity = weather_data.json()['main']['humidity']
        pressure = weather_data.json()['main']['pressure']
        wind_speed_mps = weather_data.json()['wind']['speed']
        wind_speed_mph = round(wind_speed_mps * 2.237, 2)
        visibility_meters = weather_data.json().get('visibility', 'N/A')
        visibility_miles = round(visibility_meters * 0.000621371, 2) if visibility_meters != 'N/A' else 'N/A'
        
        # Extract timezone data and calculate local time
        timezone_offset = weather_data.json()['timezone']  # Timezone offset in seconds
        local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
        local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')  # Format local time

        # Fetch the weather icon
        icon_code = weather_data.json()['weather'][0]['icon']  # Get the icon code
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"  # URL to the icon
        icon_image = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))  # Fetch and convert icon to PhotoImage
        icon_label.config(image=icon_image)  # Update the label to display the icon

        # Display city name in large bold text
        city_name.set(city.upper())  # Large and bold city name

        # Display weather details and current local time
        weather_info.set(f"Description: {weather}\n"
                         f"Temperature: {temp}ºC\n"
                         f"Feels like: {feels_like}ºC\n"
                         f"Humidity: {humidity}%\n"
                         f"Pressure: {pressure} hPa\n"
                         f"Wind speed: {wind_speed_mph} mph\n"
                         f"Visibility: {visibility_miles} miles\n"
                         f"Local Time: {local_time_str}")  # Include local time in the display

        # Add to recent searches if not already present
        if city not in recent_searches:
            recent_searches.append(city)

    except requests.exceptions.HTTPError:
        messagebox.showerror("Error", "City not found or an issue occurred.")
    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Network error, please try again.")

# Function to detect location using IP address
def detect_location():
    try:
        # Get location data using ip-api.com (no API key needed for basic usage)
        location_data = requests.get("http://ip-api.com/json").json()
        city = location_data.get('city')
        if city:
            get_weather(city)  # Fetch the weather for the detected city
        else:
            messagebox.showerror("Location Error", "Could not detect location. Please enter city manually.")
    except Exception as e:
        messagebox.showerror("Error", f"Location detection failed: {e}")

# Function to display recent searches in a new window
def show_recent_searches():
    if not recent_searches:
        messagebox.showinfo("No Recent Searches", "You haven't searched for any cities yet.")
        return
    
    # Create a new window for recent searches
    top = Toplevel(root)
    top.title("Recent Searches")
    
    label = tk.Label(top, text="Click on a city to view its weather:", font=("Helvetica", 12, "bold"))
    label.pack(pady=10)
    
    # Display each recent search as a hoverable label in the pop-up window
    for city in recent_searches:
        city_label = tk.Label(top, text=city, font=("Arial", 10), fg="black", cursor="hand2")  # 'hand2' for pointer cursor
        city_label.pack(pady=5)

        # Bind hover events
        city_label.bind("<Enter>", on_hover)  # On mouse enter
        city_label.bind("<Leave>", off_hover)  # On mouse leave

        # Bind click event
        city_label.bind("<Button-1>", lambda event, c=city: get_weather(c))

# Function to handle hover effect
def on_hover(event):
    event.widget.config(fg="blue", font=("Arial", 10, "underline"))  # Change color and underline on hover

# Function to remove hover effect when mouse leaves
def off_hover(event):
    event.widget.config(fg="black", font=("Arial", 10))  # Revert to normal on mouse leave

# GUI setup
root = tk.Tk()
root.title("WeatherCast")
root.geometry("400x500")
root.configure(bg="#00BFFF")  # Set the window background color

# Input frame to hold the city input and buttons
input_frame = tk.Frame(root, bg="#00BFFF")
input_frame.pack(pady=20)

# Create the user input field 
city_label = tk.Label(input_frame, text="Enter City:", font=("Helvetica", 12), bg="#00BFFF", fg="#333333")
city_label.grid(row=0, column=0, padx=5)

city_entry = tk.Entry(input_frame, width=20, font=("Helvetica", 10))  # Adjusted width
city_entry.grid(row=0, column=1, padx=5)

# Create the "Get Weather" button
get_weather_button = ttk.Button(input_frame, text="Get Weather", command=get_weather)
get_weather_button.grid(row=0, column=2, padx=5)  # Positioned next to the input box

# Add a "Use My Location" button to fetch weather by IP address
location_button = ttk.Button(input_frame, text="Use My Location", command=detect_location)
location_button.grid(row=1, column=0, columnspan=3, pady=10)  # Spanning the full row for centered alignment

# Weather information display
city_name = tk.StringVar()  # City names displayed here
weather_info = tk.StringVar()  # Weather details displayed here

# City name label 
city_name_label = tk.Label(root, textvariable=city_name, font=("Helvetica", 20, "bold"), bg="#00BFFF", fg="#333333")
city_name_label.pack(pady=10)

# Weather icon display 
icon_label = tk.Label(root, bg="#00BFFF")  # Placeholder for weather icon
icon_label.pack(pady=10)

# Weather details label 
weather_info_label = tk.Label(root, textvariable=weather_info, justify="left", font=("Arial", 10), bg="#00BFFF", fg="#333333")
weather_info_label.pack(pady=20)

# Frame for the exit button at the bottom-left
exit_button_frame = tk.Frame(root, bg="#00BFFF")
exit_button_frame.pack(side="left", anchor="s", padx=20, pady=20)  # Aligning it to the bottom-left

# Create the exit button
exit_button = ttk.Button(exit_button_frame, text="Exit", command=root.quit)
exit_button.grid(row=0, column=0, padx=10, pady=10)

# Frame for the recent searches button at the bottom-right
recent_searches_frame = tk.Frame(root, bg="#00BFFF")
recent_searches_frame.pack(side="right", anchor="s", padx=20, pady=20)  # Aligning it to the bottom-right

# Create the  recent searches button
recent_searches_button = ttk.Button(recent_searches_frame, text="Recent Searches", command=show_recent_searches)
recent_searches_button.grid(row=0, column=0, padx=10, pady=10)

# Run the GUI loop
root.mainloop()
