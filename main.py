from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import requests
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp

from bs4 import BeautifulSoup

def find_stock_price(url, what='Stock'):
    '''
    Finds the latest stock price from Yahoo finance.
    :param url: Give a URL from Yahoo finance for a particular stock
    :param what: Select 'stock', 'down' or 'total down' to return different information
    :return: The 'what' selected price
    '''
    # Make a request to the current page
    request_page = requests.get(url)

    # Use BeautifulSoup to parse HTML content
    soup = BeautifulSoup(request_page.content, 'html.parser')

    # Stock_info is the section on the Yahoo website to scrape
    stock_info = soup.find(class_='My(6px) Pos(r) smartphone_Mt(6px)')
    info = '|'.join(i.text for i in stock_info.select('div > span'))

    # Returns alot of information regarding current stock
    stock_price = info.split('|')[0]
    change = info.split('|')[1]
    change = change.split(' ')
    down = change[0]
    total_down = change[1]

    if what == 'Stock price':
        return 'Stock price is:  '+stock_price+' pence'

    if what == 'Change since last close':
        return 'Stock is '+down+' points since last close'

    if what == '% Change since last close':
        return 'Stock is '+total_down+' % down since last close'

class YourApp(App):

    def build(self):

            # Initiate the format of the GUI
            root_widget = BoxLayout(orientation='vertical')

            # Initialize an input label & output label
            input_label = TextInput(size_hint_y=1,)
            output_label = Label(size_hint_y=1)

            # Specifies the format of the button_grid, layout.
            button_grid = GridLayout(cols=3,
                                     size_hint_y=1)

            # Initialise dropdown for search options
            dropdown = DropDown()

            # Create three buttons
            btn1_stock = Button(text='Stock price', size_hint_y=None)
            btn2_down = Button(text='Change since last close', size_hint_y=None)
            btn3_total_down = Button(text='% Change since last close', size_hint_y=None)

            btn1_stock.bind(on_release=lambda btn: dropdown.select(btn1_stock.text))
            btn2_down.bind(on_release=lambda btn: dropdown.select(btn2_down.text))
            btn3_total_down.bind(on_release=lambda btn: dropdown.select(btn3_total_down.text))

            dropdown.add_widget(btn1_stock)
            dropdown.add_widget(btn2_down)
            dropdown.add_widget(btn3_total_down)

            # Initialise dropdown for company options
            dropdowncompany = DropDown()

            lloy_1 = Button(text='LLOY', size_hint_y=None)
            barc_2 = Button(text='BARC', size_hint_y=None)

            lloy_1.bind(on_release=lambda btn: dropdowncompany.select(lloy_1.text))
            barc_2.bind(on_release=lambda btn: dropdowncompany.select(barc_2.text))

            dropdowncompany.add_widget(lloy_1)
            dropdowncompany.add_widget(barc_2)

            # Generates a button widget for each button symbol
            button_grid.add_widget(Button(text='Search option'))
            button_grid.add_widget(Button(text='Company select'))
            button_grid.add_widget(Button(text='Go'))

            # Clears the text at the top
            clear_button = Button(text='Clear',
                                  size_hint_y=None,
                                  height=100)

            # Resizing the label
            def resize_label_text(label, new_height):
                label.font_size = 0.2*label.height

            output_label.bind(height=resize_label_text)
            input_label.bind(height=resize_label_text)

            def evaluate_result(instance):
                output_label.text = find_stock_price("https://uk.finance.yahoo.com/quote/" + input_label.text.lower() +".L/",
                                                     button_grid.children[2].text)

            def clear_label(instance):
                output_label.text = ''
                input_label.text = ''
            clear_button.bind(on_press=clear_label)


            # Bottom button will search for stock on press
            button_grid.children[0].bind(on_press=evaluate_result)
            button_grid.children[1].bind(on_release=dropdowncompany.open)
            button_grid.children[2].bind(on_release=dropdown.open)

            # Glues the selected text to the dropdown button, and updates.
            dropdown.bind(on_select=lambda instance, x: setattr(button_grid.children[2], 'text', x))

            # dropdowncompany.bind(on_select=lambda instance, x: setattr(button_grid.children[1], 'text', x))
            dropdowncompany.bind(on_select=lambda instance, x: setattr(button_grid.children[1], 'text', x))
            dropdowncompany.bind(on_select=lambda instance, x: setattr(input_label, 'text', x))

            # This is where you can add widgets to the gui
            root_widget.add_widget(input_label)
            root_widget.add_widget(output_label)
            root_widget.add_widget(button_grid)
            root_widget.add_widget(clear_button)

            return root_widget

YourApp().run()
