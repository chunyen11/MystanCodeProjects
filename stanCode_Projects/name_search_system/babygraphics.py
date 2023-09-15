"""
File: babygraphics.py
Name: Alex
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui


FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """

    year_count = len(YEARS)
    window_width_real = width - 2*GRAPH_MARGIN_SIZE
    each_year_space = window_width_real/year_count

    x_coordinate = int(GRAPH_MARGIN_SIZE + (year_index * each_year_space))

    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #

    # top horizontal line
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                       CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, width=LINE_WIDTH)
    # bottom horizontal line
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
                       CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, width=LINE_WIDTH)

    # left vertical line
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT, GRAPH_MARGIN_SIZE, 0, width=LINE_WIDTH)

    # year vertical line
    year_count = 0
    for year in YEARS:
        x_coordinate = get_x_coordinate(CANVAS_WIDTH, year_count)
        canvas.create_line(x_coordinate, 0, x_coordinate, CANVAS_HEIGHT, width=LINE_WIDTH)
        canvas.create_text(x_coordinate, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, text=year, anchor=tkinter.NW)
        year_count += 1


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #

    rank_coefficient = (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) / MAX_RANK

    for i in range(len(lookup_names)):
        lookup_name = lookup_names[i]
        line_list = []
        for j in range(len(YEARS)):
            year_check = str(YEARS[j])

            # draw vertex: name exist in name data and 對應到的 rank <1000
            if year_check in name_data[lookup_name] and int(name_data[lookup_name][year_check]) < 1000:
                rank_check = int(name_data[lookup_name][year_check])
                rank_check_normalize = rank_check * rank_coefficient

                canvas.create_text(get_x_coordinate(CANVAS_WIDTH, j)+TEXT_DX, GRAPH_MARGIN_SIZE+rank_check_normalize,
                                   text=f"{lookup_name} {rank_check}", anchor=tkinter.SW, fill=COLORS[i])

                # save coordinate
                x1 = get_x_coordinate(CANVAS_WIDTH, j)
                y1 = GRAPH_MARGIN_SIZE+rank_check_normalize
                line_list.append(x1)
                line_list.append(y1)

            # draw vertex: name not exist in name data or  name exist in name data 但是對應到的 rank >1000
            else:
                canvas.create_text(get_x_coordinate(CANVAS_WIDTH, j)+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE,
                                   text=f"{lookup_name} *", anchor=tkinter.SW, fill=COLORS[i])

                # save coordinate
                x2 = get_x_coordinate(CANVAS_WIDTH, j)
                y2 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                line_list.append(x2)
                line_list.append(y2)

            # draw line:
            if len(line_list) == 4:      # list 存滿兩組座標就要畫線
                canvas.create_line(line_list[0], line_list[1], line_list[2], line_list[3],
                                   width=LINE_WIDTH, fill=COLORS[i])

                # 存第2組 x2,y2 座標 給下一 round 用
                line_x2_temp = line_list[2]
                line_y2_temp = line_list[3]

                # reset line_list and 放第2組x2,y2 coordinate 當作第一組 coordinate
                line_list = []
                line_list.append(line_x2_temp)
                line_list.append(line_y2_temp)


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
