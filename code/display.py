import time
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont
from lib import LCD_1inch28, Touch_1inch28
import os
import time

class Display:
    path = '/home/pi/Desktop/galah/'
    def __init__(self, bg_colour='WHITE', font_name='Font00', font_size=24, mode=0):
        self.mode = mode
        self.bg_colour = bg_colour
        self.touch = Touch_1inch28.Touch_1inch28()
        self.disp = LCD_1inch28.LCD_1inch28()
        self.disp.Init()
        self.touch.init()
        self.touch.Set_Mode(self.mode)
        self.disp.clear()
        self.image = Image.new('RGB', (240, 240), bg_colour)
        self.draw = ImageDraw.Draw(self.image)
        self.Font = ImageFont.truetype(f'{Display.path}lib/{font_name}.ttf', font_size)
        
    def get_input(self):
        if self.mode == 1:
            self.touch.get_point()
            x = self.touch.X_point
            y = self.touch.Y_point
            return x, y
        else:
            return self.touch.Touch_Read_Byte(0x01)
        
    def switch_mode(self, mode):
        self.mode = mode
    
    def update(self):
        self.disp.ShowImage(self.image)
        
    def fill_colour(self, colour='WHITE'):
        self.draw.rectangle((0, 0, 240, 240), fill=colour, outline=None, width=1)
        
    def write(self, text='Hello World!', coordinates=(0, 0), fill='BLACK'):
        self.draw.text(coordinates, text, fill=fill, font=self.Font)
        
    def rectangle(self, coordinates=(0, 0, 240, 240), fill='RED'):
        self.draw.rectangle(coordinates, fill=fill, outline=None, width=1)
        
    def line(self, start=(0, 0), end=(0, 0), width=1, colour='BLACK'):
        self.draw.line((start, end), width=width, fill=colour)
        
    def load_image(self, file_name=None):
        if file_name:
            self.image = Image.open(file_name)
            self.draw = ImageDraw.Draw(self.image)
            
    def four_menu(self, colours=['crimson', 'cornflowerblue', 'forestgreen', 'gold']):
        self.fill_colour(colour='white')
        self.rectangle(coordinates=(0, 0, 120, 120), fill=colours[0])
        self.rectangle(coordinates=(121, 0, 240, 120), fill=colours[1])
        self.rectangle(coordinates=(0, 121, 120, 240), fill=colours[2])
        self.rectangle(coordinates=(121, 121, 240, 240), fill=colours[3])
        self.line(start=(120, 0), end=(120, 240), width=4)
        self.line(start=(0, 120), end=(240, 120), width=4)
    
    def main_menu(self):
        self.four_menu(colours=['crimson', 'cornflowerblue', 'forestgreen', 'gold'])
        self.write(text='Camera', coordinates=(4, 122))
        self.write(text='SMS', coordinates=(128, 122))
        self.write(text='Settings', coordinates=(128, 84))
        self.write(text='Notes', coordinates=(4, 84))
        
    def settings(self, wifi_mode='sim', has_internet=True, speaker=True):
        modes = ['wifi', 'sim', 'none']
        wifi_colours = ['green', 'blue', 'gray']
        wifi_colour = wifi_colours[modes.index(wifi_mode)]
        self.four_menu(colours=[wifi_colour, 'yellow', 'purple', 'red'])
        self.write(text='Wifi mode', coordinates=(4, 56))
        self.write(text=wifi_mode, coordinates=(4, 84))
        self.write(text='Interwebs?', coordinates=(128, 56))
        self.write(text='yes' if has_internet else 'no', coordinates=(128, 84))
        self.write(text='Speaker', coordinates=(4, 122))
        self.write(text='on' if speaker else 'off', coordinates=(12, 148))
        self.write(text='Exit', coordinates=(128, 122))
        
    def camera_stream(self, img):
        self.image = img
        self.draw = ImageDraw.Draw(self.image)
        
    def text_notes(self, lines=[]):
        self.fill_colour(colour='white')
        for i in range(len(lines)):
            y = i*24+48
            self.write(text=lines[i], coordinates=(30, y))
        self.rectangle(coordinates=(0, 0, 24, 240), fill='red')
        self.rectangle(coordinates=(0, 216, 240, 240), fill='green')
        self.rectangle(coordinates=(216, 0, 240, 240), fill='blue')
        self.write(text='save', coordinates=(80, 210))
        
        self.write(text='e', coordinates=(4, 64))
        self.write(text='x', coordinates=(4, 88))
        self.write(text='i', coordinates=(4, 112))
        self.write(text='t', coordinates=(4, 136))
        
        self.write(text='n', coordinates=(216, 64))
        self.write(text='e', coordinates=(216, 88))
        self.write(text='w', coordinates=(216, 112))
        
    def draw_notes(self, drawing=Image.new('RGB', (192, 192), 'white'), note=''):
        self.fill_colour(colour='white')
        self.rectangle(coordinates=(0, 0, 24, 240), fill='red')
        self.rectangle(coordinates=(0, 216, 240, 240), fill='green')
        self.rectangle(coordinates=(216, 0, 240, 240), fill='blue')
        self.write(text='save', coordinates=(80, 210))
        
        self.write(text='e', coordinates=(4, 64))
        self.write(text='x', coordinates=(4, 88))
        self.write(text='i', coordinates=(4, 112))
        self.write(text='t', coordinates=(4, 136))
        
        self.write(text='->', coordinates=(216, 64))
        
        self.write(text='X', coordinates=(216, 112))
        
        self.image.paste(drawing, (24, 24))
        self.write(text=note, coordinates=(50, 10))
        
    def notes_menu(self):
        self.four_menu(colours=['white', 'green', 'blue', 'red'])
        self.write(text='View all', coordinates=(4, 84))
        self.write(text='Dictate', coordinates=(128, 84))
        self.write(text='Draw', coordinates=(4, 122))
        self.write(text='Exit', coordinates=(128, 122))
        
    def show_notes(self, num_imgs=0):
        self.fill_colour('black')
        for i in range(num_imgs):
            img = Image.open(f'{Display.path}drawing{i}.png').resize((60, 60))
            x = i%4 * 60
            y = 60 + i//4*60
            self.image.paste(img, (x, y))
            
    def home_screen(self, weather_info='weather', icon_url='/home/pi/Desktop/galah/current_weather.png', time='00:00', pitch=0, roll=0):
        self.fill_colour('white')
        img = Image.open(icon_url).convert('RGBA').resize((60, 60))
        self.image.paste(img, (40, 40))
        self.write(text=weather_info[0], coordinates=(110, 40))
        self.write(text=weather_info[1], coordinates=(40, 100))
        self.write(text=time, coordinates=(20, 160))
        self.write(text=f'Pitch: {round(pitch, 1)}° Roll: {round(roll, 1)}°', coordinates=(20, 130))
        
    def loading(self):
        self.fill_colour('white')
        self.write(text='loading...', coordinates=(40, 100))
        self.update()
        
if __name__ == '__main__':
    d = Display()
    d.main_menu()
    d.update()
    time.sleep(5)
