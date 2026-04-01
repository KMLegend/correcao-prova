import cv2
import numpy as np
import os


def create_exam_image(filename, markings, num_rows=7, num_cols=5):
    # Dimensões da imagem e da grade
    cell_width, cell_height = 100, 60
    img_width = cell_width * num_cols + 40
    img_height = cell_height * num_rows + 40

    # Cria fundo branco
    img = np.ones((img_height, img_width, 3), dtype=np.uint8) * 255

    # Coordenadas da grade (com margem de 20px)
    offset_x, offset_y = 20, 20

    # Desenha a grade
    for r in range(num_rows + 1):
        y = offset_y + r * cell_height
        cv2.line(img, (offset_x, y), (offset_x + num_cols * cell_width, y), (0, 0, 0), 2)

    for c in range(num_cols + 1):
        x = offset_x + c * cell_width
        cv2.line(img, (x, offset_y), (x, offset_y + num_rows * cell_height), (0, 0, 0), 2)

    # Adiciona marcações 'X'
    # markings: lista de tuplas (linha_index, coluna_index)
    for row, col in markings:
        x_start = offset_x + col * cell_width + 20
        y_start = offset_y + row * cell_height + 15
        x_end = x_start + cell_width - 40
        y_end = y_start + cell_height - 30
        
        # Desenha um 'X' grosso
        cv2.line(img, (x_start, y_start), (x_end, y_end), (0, 0, 0), 8)
        cv2.line(img, (x_end, y_start), (x_start, y_end), (0, 0, 0), 8)

    # Salva
    if not os.path.exists("test_images"):
        os.makedirs("test_images")
    
    path = os.path.join("test_images", filename)
    cv2.imwrite(path, img)
    print(f"Salvo: {path}")
    return os.path.abspath(path)


if __name__ == "__main__":
    # A=0, B=1, C=2, D=3, E=4
    gabarito_marks = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 0), (6, 1)]
    # Q1-Q5 Correct, Q6 Incorrect (C instead of A), Q7 Correct
    student_marks = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 2), (6, 1)]

    create_exam_image("gabarito.png", gabarito_marks)
    create_exam_image("aluno.png", student_marks)
