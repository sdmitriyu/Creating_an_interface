import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        # Задаём название полотна
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Создаём пиксельную основу для холста
        self.image = Image.new("RGB", (600, 400), color="white")
        self.draw = ImageDraw.Draw(self.image)

        # На основе пиксельной основы создаём сам холст
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Инициализируем настройки, которые пропишем позже
        self.setup_ui()

        # Создаём кисть
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'  # Стандартный цвет кисти
        self.eraser_on = False  # Флаг для проверки, включен ли ластик

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

        self.brush_size = tk.IntVar(value=1)
        sizes = [1, 2, 5, 10]
        size_menu = tk.OptionMenu(control_frame, self.brush_size, *sizes)
        size_menu.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

    def use_eraser(self):
        """Переключение на ластик, который рисует цветом фона."""
        self.pen_color = 'white'  # Цвет фона (по умолчанию белый)
        self.eraser_on = True

    def paint(self, event):
        """Отрисовка линии при движении мыши."""
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
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

    def choose_color(self):
        """Выбор цвета для кисти. Также отключаем ластик."""
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.eraser_on = False  # Отключаем режим ластика

    def save_image(self):
        """Сохранение изображения в PNG формате."""
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

main()
