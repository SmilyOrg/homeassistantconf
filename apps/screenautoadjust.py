import appdaemon.appapi as appapi

#
# Screen Auto Adjust App
#
# Args:
#

class ScreenAutoAdjust(appapi.AppDaemon):

  light_sensor = "sensor.light"
  switch_check = "switch.hexacompy_monitors"
  screen_light = "light.dell_u2515h"

  light_max = 60
  screen_min = 0.4 * 255
  screen_max = 1 * 255
  screen_update_change = 0.05 * 255
  screen_last_value = -1

  def initialize(self):
    self.log("ScreenAutoAdjust \o/")
    self.listen_state(self.screen_update, self.light_sensor)
    self.screen_update(None, None, None, None, None)

  def screen_update(self, entity, attribute, old, new, kwargs):
    # if self.get_state(self.switch_check) != "on":
    #   return
    light = float(self.get_state(self.light_sensor))
    norm = min(1, light/self.light_max)
    screen = round(self.screen_min + norm * (self.screen_max - self.screen_min))
    delta = screen - self.screen_last_value
    # Debug
    # self.log("Light: {} Norm: {:.3f} Screen: {} Delta: {}".format(light, norm, screen, delta))
    if abs(delta) >= self.screen_update_change:
      self.log("Light: {} Norm: {:.3f} Screen: {} Delta: {}".format(light, norm, screen, delta))
      self.screen_adjust(screen)

  def screen_adjust(self, screen):
    self.screen_last_value = screen
    self.call_service("light/turn_on", entity_id = self.screen_light, brightness
 = screen)
