# Python Weather Application

WeatherCast

A Python-based weather application that provides real-time weather information for any city. This application integrates with the OpenWeatherMap API to fetch weather data such as temperature, humidity, wind speed, visibility, and local time. It also supports automatic location detection using the user's IP address and displays weather condition icons. The app features a user-friendly graphical interface built with `tkinter`.

# Features

- **Real-time Weather Data**: Provides live weather information for any city worldwide.
- **Automatic Location Detection**: Automatically detects the user’s current location based on their IP address and fetches the weather information.
- **Weather Icons**: Displays icons corresponding to the current weather conditions (e.g., clear, cloudy, rainy).
- **Local Time Display**: Shows the local time of the searched city, calculated using the time zone data.
- **Recent Searches**: Users can easily revisit previously searched cities through a recent searches feature.
- **Graphical User Interface (GUI)**: Built with `tkinter` for a clean and interactive experience.
- **Fixed Window Size**: Ensures all content remains visible and accessible in the interface.

# Technologies Used

- **Python**: Core programming language used for the application logic.
- **OpenWeatherMap API**: Used to retrieve real-time weather data.
- **tkinter**: Used to create the graphical user interface (GUI).
- **Pillow (PIL)**: Handles the weather condition icons.
- **Requests**: For making HTTP requests to fetch weather data and detect user location via IP.

# Requirements

To run this application, you will need:

- Python 3.x installed on your machine
- The following Python libraries:
  - `tkinter`
  - `Pillow`
  - `requests`

# Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/weather-app.git
    cd weather-app
    ```

2. Install the required libraries:
    ```bash
    pip install Pillow requests
    ```

3. Obtain an API key from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) and replace the placeholder API key in the code:
    ```python
    api_key = 'your_api_key_here'
    ```

## Usage

1. Run the application:
    ```bash
    python weather_app.py
    ```

2. **Features**:
   - Enter a city name to fetch the weather data.
   - Click the **"Use My Location"** button to automatically detect your current location and fetch the weather data for your city.
   - View weather details such as temperature, humidity, wind speed, and local time, as well as a weather icon based on the conditions.
   - Use the **"Recent Searches"** feature to revisit previously searched cities.


 GitHub: [Muaazp4](https://github.com/muaazp4)

 
