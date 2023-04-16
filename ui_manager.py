from singleton import Singleton

class UIManager(metaclass=Singleton):
  def get_welcome_screen_button_params(self, width: int, height: int):

    button_params = {
        "spacing": 80,
        "width": 200,
        "height": 50,
    }

    button_params["x"] = (width / 2) - (button_params["width"] / 2)
    button_params["y"] = (height / 2) - (button_params["height"] / 2)
    
    return button_params
