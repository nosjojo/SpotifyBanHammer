from PyQt5.QtCore import QObject, pyqtSlot

class KeyBindings(QObject):
    def __init__(self) -> None:
        self.combination_to_function = {}
        self.pressed_vks = set()
        
    def set_hotkeys(self, hotkey: frozenset):
        self.combination_to_function.update(hotkey)

    def get_vk(self,key):
        return key.vk if hasattr(key, 'vk') else key.value.vk

    def is_combination_pressed(self,combination):
        return all([self.get_vk(key) in self.pressed_vks for key in combination])

    def on_press(self,key):
        vk = self.get_vk(key)
        self.pressed_vks.add(vk)
        for combination in self.combination_to_function:
            if self.is_combination_pressed(combination):
                self.combination_to_function[combination]()

    def on_release(self,key):
        vk = self.get_vk(key)  # Get the key's vk
        self.pressed_vks.discard(vk)  # Remove it from the set of currently pressed keys
    
    def stop_listener(self):
        self.terminate = True
