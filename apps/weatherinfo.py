import appdaemon.plugins.hass.hassapi as hass

#
# Weather to InfoMatrix App
#
# Args:
#

class WeatherInfo(hass.Hass):

  icon_to_unicode = {
    "clear-day": "🌣",
    "clear-night": "🌣",
    "rain": "🌧",
    "snow": "🌨",
    "sleet": "⛆",
    "wind": "🌬",
    "fog": "🌁",
    "cloudy": "🌥",
    "partly-cloudy-day": "🌤",
    "partly-cloudy-night": "🌤"
  }

  def initialize(self):
    self.log("WeatherInfo \o/")
    self.listen_state(self.weather_update, "sensor.dark_sky_icon")
    self.listen_state(self.weather_update, "sensor.dark_sky_temperature")
    self.listen_state(self.weather_update, "binary_sensor.infomatrix_online", new = "on")
    self.listen_state(self.display_waiting, "binary_sensor.infomatrix_waiting", new = "on")
    self.weather_update(None, None, None, None, None)

  def display_waiting(self, entity, attribute, old, new, kwargs):
    self.call_service("mqtt/publish", topic = "devices/infomatrix/display/waiting/set", payload = "false")
    self.weather_update(None, None, None, None, None)

  def weather_update(self, entity, attribute, old, new, kwargs):
    temp = self.get_state("sensor.dark_sky_temperature")
    icon = self.get_state("sensor.dark_sky_icon")
    weather_char = self.icon_to_unicode.get(icon, "?")
    text = "{0} {1}°C".format(
      weather_char,
      round(float(temp))
    )
    self.log("Weather update: " + text)
    self.log(self.get_state("sensor.dark_sky_hourly_summary"))
    self.report(text)

  def report(self, text):
    self.call_service("mqtt/publish", topic = "devices/infomatrix/display/text/set", payload = text, retain = True)
