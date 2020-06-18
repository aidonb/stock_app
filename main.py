from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import requests

from bs4 import BeautifulSoup

def find_stock_price(page):
    '''
    Finds the latest stock price from Yahoo finance.

    :param page: Give a URL from Yahoo finance for a particular stock
    :return: The current stock price
    '''
    request_page = requests.get(page)
    soup = BeautifulSoup(request_page.content, 'html.parser')
    stock_info = soup.find(class_='My(6px) Pos(r) smartphone_Mt(6px)')
    info = '|'.join(i.text for i in stock_info.select('div > span'))
    stock_price = info.split('|')[0]
    return 'Share price is '+stock_price


class YourApp(App):

    def build(self):

        # Initiate the format of the GUI
        root_widget = BoxLayout(orientation='vertical')

        # Initialize an input label & output label
        input_label = TextInput(size_hint_y=1,   )
        output_label = Label(size_hint_y=1)

        # Specifies the format of the button_grid, layout.
        button_grid = GridLayout(cols=1,
                                 size_hint_y=1)

        # Generates a button widget for each button symbol (in this case, 1)
        button_grid.add_widget(Button(text='Search'))

        # Clears the text at the top
        clear_button = Button(text='clear',
                              size_hint_y=None,
                              height=100)

        # Resizing the label
        def resize_label_text(label, new_height):
            label.font_size = 0.2*label.height

        output_label.bind(height=resize_label_text)
        input_label.bind(height=resize_label_text)

        def evaluate_result(instance):
            output_label.text = find_stock_price("https://uk.finance.yahoo.com/quote/"+input_label.text.lower()+".L/")

        # Bottom button will search for stock on press
        button_grid.children[0].bind(on_press=evaluate_result)

        def clear_label(instance):
            output_label.text = ''
            input_label.text = ''
        clear_button.bind(on_press=clear_label)


        # This is where you can add widgets to the gui
        root_widget.add_widget(input_label)
        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(clear_button)

        return root_widget


YourApp().run()
