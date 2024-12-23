import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk


class DrawingApp:
    def __init__(self, root):
        # Задаём название полотна
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Связывание горячих клавиш
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

        self.bg_color = 'white'

        # Создаём пиксельную основу для холста
        self.image = Image.new("RGB", (600, 400), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

        # На основе пиксельной основы создаём сам холст
        self.canvas = tk.Canvas(root, width=600, height=400, bg=self.bg_color)
        self.canvas.pack()

        # Цвет кисти и флаг ластика
        self.pen_color = 'black'
        self.eraser_on = False

        # Настройки интерфейса
        self.setup_ui()

        # Создаём кисть
        self.last_x, self.last_y = None, None

        # Привязываем события мыши
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.erase_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        self.erase_button.pack(side=tk.LEFT)

        # Кнопка для добавления текста
        text_btn = tk.Button(control_frame, text='Текст', command=self.add_text)
        text_btn.pack(side='left', padx=5)

        # Кнопка для изменения фона
        bg_btn = tk.Button(control_frame, text='Изменить фон', command=self.change_background)
        bg_btn.pack(side='left', padx=5)

        # Предварительный просмотр цвета
        self.color_preview = tk.Label(control_frame, width=2, bg=self.pen_color)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        # Привязка правой кнопки мыши к методу pick_color
        self.canvas.bind('<Button-3>', self.pick_color)

        sizes = [1, 2, 5, 10]
        self.brush_size = tk.IntVar(value=1)
        size_menu = tk.OptionMenu(control_frame, self.brush_size, *sizes)
        size_menu.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        self.resize_button = tk.Button(control_frame, text='Изм. разм. окна', command=self.resize_window)
        self.resize_button.pack(side=tk.LEFT)

    def change_background(self):
        (r, g, b), color = colorchooser.askcolor()  # Получение RGB и шестнадцатеричного формата
        self.bg_color = color
        if color:
            self.canvas.config(background=color)
            self.image.paste(Image.new('RGB', (500, 400), (r, g, b)))
            self.draw = ImageDraw.Draw(self.image)

    def update_canvas(self):
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)

    def resize_window(self):
        width = simpledialog.askinteger(
            title='Изменение ширины экрана',
            prompt='Введите новую ширину экрана'
        )
        height = simpledialog.askinteger(
            title='Изменение высоты экрана',
            prompt='Введите новую высоту экрана'
        )
        try:
            if width is not None and height is not None:
                # Задаём название полотна
                self.root.title("Рисовалка с сохранением в PNG")

                # Создаём пиксельную основу для холста
                self.image = Image.new("RGB", (height, width), color="white")
                self.draw = ImageDraw.Draw(self.image)

                # На основе пиксельной основы создаём сам холст
                self.canvas.config(width=width, height=height)
                self.canvas.delete('all')
        except Exception:
            print('Ещё раз нажмите кнопку изменения размера экрана и введите валидные данные')

    def pick_color(self, event):
        x, y = event.x, event.y
        rgb = self.image.getpixel((x, y))
        self.pen_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
        self.update_color_preview()

    def update_color_preview(self):
        """Обновление цвета предварительного просмотра."""
        self.color_preview.config(bg=self.pen_color)

    def use_eraser(self):
        """Переключение на ластик, который рисует цветом фона."""
        self.pen_color = self.bg_color
        self.eraser_on = True
        self.update_color_preview()

    def paint(self, event):
        """Отрисовка линии при движении мыши."""
        if self.last_x and self.last_y:
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                width=self.brush_size.get(), fill=self.pen_color,
                capstyle=tk.ROUND, smooth=tk.TRUE
            )
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size.get())
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        """Сброс координат при отжатии кнопки мыши."""
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Очистка холста."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        """Выбор цвета для кисти. Также отключаем ластик."""
        color = colorchooser.askcolor(color=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.update_color_preview()
        self.eraser_on = False

    def save_image(self, event=None):
        """Сохранение изображения в PNG формате."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG files', '*.png')])
        if file_path:
            self.image.save(file_path, "PNG")

    def add_text(self):
        self.text = simpledialog.askstring("Введите текст", "Введите текст для добавления:")
        self.canvas.bind("<Button-1>", self.place_text)

    def place_text(self, event):
        if self.text:
            x, y = event.x, event.y
            self.draw.text((x, y), self.text, fill=self.pen_color)
            self.update_canvas()
            self.text = None

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
