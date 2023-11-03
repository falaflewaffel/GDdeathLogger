import flet as ft

class Image:
    def __init__(self, src: str, width: int, height: int, fit) -> None:
        self.src = src
        self.width = width
        self.height = height
        self.fit = fit
        
    def value(self):
        return ft.Image(
            src = self.src,
            width = self.width,
            height = self.height,
            fit = self.fit
        )

class FilledButton:
    def __init__(self, text: str, width: int, height: int, on_click, disabled: bool = False) -> None:
        self.text = text
        self.width = width
        self.height = height
        self.on_click = on_click
        self.disabled = disabled
        
    def value(self):
        return ft.FilledButton(
            text = self.text,
            width = self.width,
            height = self.height,
            on_click = self.on_click,
            disabled = self.disabled
        )
        
class EmptySpace:
    @staticmethod
    def shiftDown(height: int):
        return ft.Text('', height=height)
    
    @staticmethod
    def shiftRight(width: int):
        return ft.Text('', width=width)
    
class TextField:
    def __init__(self, label: str, width: int, height: int, hintText: str = None) -> None:
        self.label = label
        self.width = width
        self.height = height
        self.hintText = hintText
        
    def value(self):
        return ft.TextField(
            label = self.label,
            width = self.width,
            height = self.height,
            hint_text = self.hintText
        )

class Text:
    def __init__(self, text: str, visible: bool = True, color: str = 'white', width: int = None, height: int = None) -> None:
        self.text = text
        self.visible = visible
        self.color = color
        self.width = width
        self.height = height
        
    def value(self):
        return ft.Text(self.text, visible = self.visible, color = self.color, width = self.width, height = self.height)
    
class FilledTonalButton:
    def __init__(self, text: str, width: int, height: int, on_click, disabled: bool = False) -> None:
        self.text = text
        self.width = width
        self.height = height
        self.on_click = on_click
        self.disabled = disabled
        
    def value(self):
        return ft.FilledTonalButton(
            text = self.text,
            width = self.width,
            height = self.height,
            on_click = self.on_click,
            disabled = self.disabled
        )

