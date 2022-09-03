#!/usr/local/bin/python3
#
# Authors: Akshay Tiwlekar (akstiwle), Pramey Modi (pmmodi), Rohan Mehta(mehtaro)
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
# Discussed with Dinesh Reddy Challa(dichalla)
# Referred code from \
# https://www.codegrepper.com/code-examples/python/python+sort+array+by+column for sorting column from image matrix

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio

# calculate "Edge strength map" of an image
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale, 0, filtered_y)
    return sqrt(filtered_y ** 2)


# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range(int(max(y - int(thickness / 2), 0)), int(min(y + int(thickness / 2), image.size[1] - 1))):
            image.putpixel((x, t), color)
    return image


def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [(pt[0] + dx, pt[1] + dy) for dx in range(-3, 4) for dy in range(-2, 3) if
                   dx == 0 or dy == 0 or abs(dx) == abs(dy)]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)  # Yellow
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)  # Blue
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)  # Red
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)  # Red star(asterisk)
    imageio.imwrite(filename, new_image)


def probability_function(max_value, value):
    probability = value / max_value
    return probability


def human_feedback(img_edges, ice_x, ice_y, rock_x, rock_y):
    row, col = img_edges.shape
    ice_list, rock_list = simple_bayes_net(img_edges)
    ice = list()
    rock = list()
    ice.append(ice_list[0])
    rock.append(rock_list[0])
    for i in range(1, col):
        columns = img_edges[:, i]
        max_value = max(columns)
        columns_probability = probability_function(max_value, columns)
        previous_ice = ice[i - 1]
        ice_list = list()
        for k in range(len(columns_probability)):
            value_ice = ice_y - k
            human_probability_ice = -1 * (abs(probability_function(col, value_ice)))
            human_value_ice = previous_ice[0] - k
            ice_list.append(columns_probability[k] - abs(probability_function(row, human_value_ice)) +
                            human_probability_ice)
        max_edges_sorted_list_ice = [j for j in sorted(enumerate(ice_list), key=lambda x: x[1], reverse=True)]
        edge_curr = max_edges_sorted_list_ice[0]
        ice.append(edge_curr)

        previous_rock = rock[i - 1]
        rock_list = list()
        for k in range(len(columns_probability)):
            if k < edge_curr[0] + 10:
                rock_list.append(-100)
            else:
                value_rock = rock_y - k
                human_probability_rock = -1 * (abs(probability_function(col, value_rock)))
                human_value_rock = previous_rock[0] - k
                rock_list.append(columns_probability[k] - abs(probability_function(row, human_value_rock)) +
                                 human_probability_rock)
        max_edges_sorted_list_rock = [j for j in sorted(enumerate(rock_list), key=lambda x: x[1], reverse=True)]
        rock.append(max_edges_sorted_list_rock[0])

    return ice, rock


# applying viterbi algorithm
def hidden_markov_method(img_edges):
    emission_probability_ice, emission_probability_rock = simple_bayes_net(img_edges)
    ice = list()
    rock = list()

    # initial element(pixel) for the hmm transition matrix
    initial_ice = emission_probability_ice[0]
    initial_rock = emission_probability_rock[0]

    ice.append(initial_ice)
    rock.append(initial_rock)
    row, col = img_edges.shape
    for i in range(1, col):
        columns = img_edges[:, i]
        max_value = max(columns)
        columns_probability = probability_function(max_value, columns)

        previous_position_ice = ice[i - 1]

        ice_heuristic = list()
        for k in range(len(columns_probability)):
            value = previous_position_ice[0] - k
            ice_heuristic.append(columns_probability[k] - abs(probability_function(row, value)))
        max_edges_sorted_list_ice = [j for j in sorted(enumerate(ice_heuristic), key=lambda x: x[1], reverse=True)]
        edge_curr = max_edges_sorted_list_ice[0]
        ice.append(edge_curr)

        previous_position_rock = rock[i - 1]
        rock_heuristic = list()
        for k in range(len(columns_probability)):
            if k < edge_curr[0] + 10:
                rock_heuristic.append(-100)
            else:
                value = previous_position_rock[0] - k
                rock_heuristic.append(columns_probability[k] - abs(probability_function(row, value)))
        max_edges_sorted_list_rock = [j for j in sorted(enumerate(rock_heuristic), key=lambda x: x[1], reverse=True)]
        rock.append(max_edges_sorted_list_rock[0])

    return ice, rock


# applying simple bayes network to calculating the emission matrix
def simple_bayes_net(img_edges):
    ice_boundary_list = list()
    rock_boundary_list = list()
    row, col = img_edges.shape
    for j in range(col):
        columns = img_edges[:, j]
        max_value = max(columns)
        columns_probability = probability_function(max_value, columns)
        max_edges_sorted_list = [i for i in sorted(enumerate(columns_probability), key=lambda x: x[1], reverse=True)]

        ice = max_edges_sorted_list[0]
        rock = ()
        # print(ice_boundary)

        for i in max_edges_sorted_list[1:]:
            if i[0] > ice[0] + 10:
                rock = i
                break
        ice_boundary_list.append(ice)
        rock_boundary_list.append(rock)

    # print(ice_boundary_list, rock_boundary_list)
    return ice_boundary_list, rock_boundary_list


# def

# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception(
            "Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [int(i) for i in sys.argv[2:4]]
    gt_icerock = [int(i) for i in sys.argv[4:6]]

    # load in image
    input_image = Image.open(input_filename).convert('RGB')
    # print(input_image)
    image_array = array(input_image.convert('L'))
    # print(image_array)

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    # print(edge_strength)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.
    ice_boundary, rock_boundary = simple_bayes_net(edge_strength)
    hmm_ice, hmm_rock = hidden_markov_method(edge_strength)
    feedback_ice, feedback_rock = human_feedback(edge_strength, gt_airice[0], gt_airice[1], gt_icerock[0], gt_icerock[1])

    airice_simple = [x[0] for x in ice_boundary]
    airice_hmm = [x[0] for x in hmm_ice]
    airice_feedback = [x[0] for x in feedback_ice]

    icerock_simple = [x[0] for x in rock_boundary]
    icerock_hmm = [x[0] for x in hmm_rock]
    icerock_feedback = [x[0] for x in feedback_rock]

    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
