import tkinter as tk
from tkinter import messagebox
import math

def main_variables():
    # Początkowe dane dla wyszukiwania
    row_length = float(entry_row_length.get())
    shielding_effectiveness = float(entry_shielding_effectiveness.get())
    frequency = float(entry_frequency.get())
    return row_length, shielding_effectiveness, frequency

def main_calculations(frequency):
    # Obliczamy długość fali(λ) = c/f
    c = 2.9979250
    wavelength = 299792458 / frequency * 10**9

    wavelength = round(wavelength)
    num = wavelength
    power = len(str(num)) - 1
    wavelength = num / (10 ** power)
    wavelength = round(wavelength, 18)

    result_text = "Długość fali: {} cm\n".format(wavelength)

    # S = 20log(λ/2l)

    l = wavelength / (2 * math.pow(10, (shielding_effectiveness+6)/20))

    result_text += "Wymiar liniowy otworu: {} cm\n".format(l)

    # Szukamy odlłeglość pomiędzy λ / 2 i λ / 10, zaczynamy od λ / 2

    distance_for_search = wavelength / 2

    return l, wavelength, result_text, distance_for_search

def find_hexagons_radius(l):
    # Promień otworu dla sześciokąta R=l/6
    radius = l / 6
    return radius

def find_circle_radius(l):
    # Promień otworu dla koła R=l/2π
    radius = l / (2 * math.pi)
    return radius

def find_square_radius(l):
    # Promień otworu dla kwadratu dla R=a√2/2
    a = l / 4
    radius = a * (2) ** 0.5 / 2
    return radius

def find_rectangle_radius(l):
    # Promień otworu dla prostokąta ze stronami 2 do 3 dla R=√a^2+b^2
    length_ratio = 2 / (2 + 3)
    width_ratio = 3 / (2 + 3)

    half_perimeter = l / 2

    length = half_perimeter * length_ratio
    width = half_perimeter * width_ratio

    radius = math.sqrt(length ** 2 + width ** 2)

    return radius

def find_equailiateral_triangle_radius(l):
    # Promień otworu dla trójkąta_równobocznego R=a/√3
    a = l / 3
    radius = a / math.sqrt(3)
    return radius

def calculate_distance(n_holes_per_raw, distance_for_search, radius, row_length):
    # funkcja wyszukiwania odłeglości między otworami
    distance_per_row_for_search = 0
    while distance_per_row_for_search < row_length:
        n_holes_per_raw += 1
        distance_per_row_for_search = (distance_for_search + (distance_for_search + radius * 2) * n_holes_per_raw)
    else:
        distance = distance_for_search - (distance_per_row_for_search - row_length) / (n_holes_per_raw + 1)
    return n_holes_per_raw, distance

def check_and_calculate_distance(n_holes_per_raw, distance_for_search, radius, row_length, distance):
    # funkcja sprawdzania i wyszukiwania odległości między otworami, jeśli w poprzedniej funkcji odległość jest większa niż λ / 2
    while distance + radius * 2 > distance_for_search:
        n_holes_per_raw += 1
        distance_per_row_for_search = (distance_for_search + ((distance_for_search + radius * 2) * n_holes_per_raw))
        distance = distance_for_search - (distance_per_row_for_search - row_length) / (n_holes_per_raw + 1)
        return n_holes_per_raw, distance
    else:
        return n_hexagons_per_raw, distance

def check_distance(radius, distance_for_search, row_length):
    # funkcja sprawdzania czy jest potrzeba w wykorzystaniu funkcji check_and_calculate_distance (dla sprawdzania czy jest odłeglość większa niż λ / 2)
    try:
        n_holes_per_raw, distance = calculate_distance(0, distance_for_search, radius, row_length)
        if distance + radius * 2 > distance_for_search:
            n_holes_per_raw, distance = check_and_calculate_distance(n_holes_per_raw, distance_for_search, radius, row_length, distance)
        else:
            n_holes_per_raw, distance = calculate_distance(0, distance_for_search, radius, row_length)
        return n_holes_per_raw, distance
    except Exception as e:
        print("Error occurred while checking distance:", e)

def results(distance_for_search, radius, row_length, wavelength, l):
    #Wyświetlania wyników

    n_holes_per_raw, distance = check_distance(radius, distance_for_search, row_length)

    # Sprawdzamy czy suma otworów z odległością w rzędzie = 50 cm
    total_holes_and_distance = round((distance+(distance+radius*2)*n_holes_per_raw), 4)
    result_text = "Długość fali: {} cm\n".format(wavelength)
    result_text += "Wymiar liniowy otworu: {} cm\n".format(l)
    result_text += "Promień otworu: {} cm\n".format(radius)
    result_text += "λ/2: {} cm\n".format(distance_for_search)
    result_text += "Suma otworów z odległością w rzędzie: {} cm\n".format(total_holes_and_distance)
    result_text += "Odłeglość pomiędzy otworami: {} cm\n".format(distance)
    result_text += "Ostateczna liczba otworów w kwadracie {} cm x {} cm: {} otworów\n".format(row_length, row_length, n_holes_per_raw**2)
    result_text += "Liczba otworów w rzędzie: {}\n".format(n_holes_per_raw)

    neighbours = 4

    result_text += "Ilość sąsiadów: {}\n".format(neighbours)

    # S = 20log(λ/2l)
    shielding_effectiveness = 20 * math.log10(wavelength / (2 * l))
    # S = -20log√n
    damping = round(-20*math.log10(math.sqrt(neighbours)))

    result_text += "Skuteczność ekranowania: {} dB\n".format(shielding_effectiveness)
    result_text += "Tłumienia: {} dB\n".format(damping)
    result_text += "Skuteczność: {} dB\n".format(shielding_effectiveness + damping)

    result_text_widget.delete('1.0', tk.END)  # Clear previous results
    result_text_widget.insert(tk.END, result_text)  # Insert new results
    result_text_widget.config(width=80)  # Set the width of the Text widget

    create_gui1(distance, row_length, radius, n_holes_per_raw)

def draw_circles(canvas, radius, distance, n_holes_per_row):
    # Rysowanie dziur
    x_offset = distance
    y_offset = distance
    for i in range(n_holes_per_row):
        for j in range(n_holes_per_row):
            canvas.create_oval(x_offset - radius, y_offset - radius, x_offset + radius, y_offset + radius, outline="black")
            x_offset += 2 * radius + distance
        x_offset = distance
        y_offset += 2 * radius + distance

def create_gui1(distance, row_length, radius, n_holes_per_row):
    #Tworzenie GUI dla przykładowej płyty
    root = tk.Tk()
    root.title("Example of a disc")

    scale_factor = 10
    canvas = tk.Canvas(root, width=row_length * scale_factor, height=row_length * scale_factor, bg="white", highlightthickness=0)
    canvas.pack()

    canvas.create_rectangle(distance, distance, row_length * scale_factor - distance, row_length * scale_factor - distance, outline="black")

    draw_circles(canvas, radius * scale_factor, distance * scale_factor, n_holes_per_row)

    root.mainloop()

def create_gui():
    # Tworzenie GUI dla kalkulatora ekranowania elektromagnetycznego
    root = tk.Tk()
    root.title("EM Shielding Calculator")

    root.geometry("600x500")

    label_row_length = tk.Label(root, text="Row Length [cm]:")
    label_row_length.grid(row=0, column=0, padx=10, pady=5)
    label_shielding_effectiveness = tk.Label(root, text="Shielding Effectiveness [dB]:")
    label_shielding_effectiveness.grid(row=1, column=0, padx=10, pady=5)
    label_frequency = tk.Label(root, text="Frequency [GHz]:")
    label_frequency.grid(row=2, column=0, padx=10, pady=5)
    label_shape = tk.Label(root, text="Select Shape:")
    label_shape.grid(row=3, column=0, padx=10, pady=5)

    global entry_row_length, entry_shielding_effectiveness, entry_frequency
    entry_row_length = tk.Entry(root, width=20)
    entry_row_length.grid(row=0, column=1, padx=10, pady=5)
    entry_shielding_effectiveness = tk.Entry(root, width=20)
    entry_shielding_effectiveness.grid(row=1, column=1, padx=10, pady=5)
    entry_frequency = tk.Entry(root, width=20)
    entry_frequency.grid(row=2, column=1, padx=10, pady=5)

    global shape_var
    shape_var = tk.StringVar(root)
    shape_var.set("Hexagon")  # Default shape
    shapes = ["Hexagon", "Rectangle", "Equilateral Triangle", "Circle", "Square"]
    shape_dropdown = tk.OptionMenu(root, shape_var, *shapes)
    shape_dropdown.grid(row=3, column=1, padx=10, pady=5)

    button_calculate = tk.Button(root, text="Calculate", command=calculate, width=20)
    button_calculate.grid(row=4, columnspan=2, padx=10, pady=5)

    global result_text_widget
    result_text_widget = tk.Text(root, width=80, height=20)
    result_text_widget.grid(row=5, columnspan=2, padx=10, pady=5)

    root.mainloop()

def calculate():
    #funkcja obliczania promienia otworu w zależności od wybranego kształtu
    global shielding_effectiveness, radius, distance, row_length, n_holes_per_row
    try:
        row_length, shielding_effectiveness, frequency = main_variables()
        l, wavelength, result_text, distance_for_search = main_calculations(frequency)

        shape = shape_var.get()
        if shape == "Hexagon":
            radius = find_hexagons_radius(l)
        elif shape == "Rectangle":
            radius = find_rectangle_radius(l)
        elif shape == "Equilateral Triangle":
            radius = find_equailiateral_triangle_radius(l)
        elif shape == "Circle":
            radius = find_circle_radius(l)
        elif shape == "Square":
            radius = find_square_radius(l)

        results(wavelength / 2, radius, row_length, wavelength, l)


    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values")

if __name__ == "__main__":
    create_gui()