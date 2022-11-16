# Name: Megan Le
# email: mle25@wisc.edu
# Class/Semester: CS 540 Spring 2021
# Instructor: Sharon Li

import csv
import math
import random

import numpy as np
import matplotlib.pyplot as plt


def load_data(filepath):
    pokemon_list = []
    fields = ['#', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    reader = csv.DictReader(open(filepath), fieldnames=fields)
    next(reader)
    for x in range(20):
        line = next(reader)
        del line[None]  # removes the Generation and Legendary columns
        for column in line:
            try:
                line[column] = int(line[column])
            except ValueError:
                continue
        pokemon_list.append(line)
    return pokemon_list


def calculate_x_y(stats):
    x = stats['Attack'] + stats['Sp. Atk'] + stats['Speed']  # calculates Pokemon's total offensive strength
    y = stats['Defense'] + stats['Sp. Def'] + stats['HP']  # calculates Pokemon's total defensive strength
    return int(x), int(y)


def make_valid(dataset):
    for x in range(len(dataset)):
        for col in range(len(dataset[x])):
            if not math.isfinite(col):
                dataset[col] = 0
    return dataset


def calc_cluster_distance(c1, c2):
    dist = 0
    for i in range(len(c1)):
        dist += (c1[i] - c2[i]) ** 2
    return np.sqrt(dist)


def update_smallest(c1, p1, c2, p2):
    if c1["#"] < c2["#"]:  # if c1 has smaller cluster index
        smallest = {"C1": c1["#"], "C2": c2["#"], "Dist": calc_cluster_distance(p1, p2),
                    "Points": c1["Points"] + c2["Points"]}
    else:  # if c2 has smaller cluster index
        smallest = {"C1": c2["#"], "C2": c1["#"], "Dist": calc_cluster_distance(p1, p2),
                    "Points": c1["Points"] + c2["Points"]}
    return smallest


def tie_break(c1, p1, c2, p2, smallest):
    if min(c1["#"], c2["#"]) < smallest["C1"]:
        smallest.update(update_smallest(c1, p1, c2, p2))
    elif smallest["C1"] == min(c1["#"], c2["#"]):
        if min(c1["#"], c2["#"]) < smallest["C2"]:
            smallest.update(update_smallest(c1, p1, c2, p2))
    return smallest


def hac(dataset):
    dataset = make_valid(dataset)
    m = len(dataset)
    Z = []  # the list/array to return
    clusters = []
    for i in range(m):
        clusters.append({"#": i, "Points": [dataset[i]]})
    for row_num in range(m - 1):  # for indices 20-39
        smallest = dict.fromkeys(["C1", "C2", "Dist", "Points"])
        smallest.update({"Dist": 999999})
        for c1 in clusters:  # for each cluster in clusters (c1)
            for c2 in clusters:  # for each cluster in clusters (c2 -- given c1 != c2)
                if c1 != c2:
                    for p1 in c1["Points"]:
                        for p2 in c2["Points"]:
                            dist = calc_cluster_distance(p1, p2)
                            if dist < smallest["Dist"]:
                                smallest.update(update_smallest(c1, p1, c2, p2))
                            elif dist == smallest["Dist"]:
                                smallest = tie_break(c1, p1, c2, p2, smallest)
        clusters = [c for c in clusters if not (c["#"] == smallest["C1"] or c["#"] == smallest["C2"])]
        clusters.append({"#": m + row_num, "Points": smallest["Points"]})
        row = [points for points in smallest.values()]
        row[3] = len(row[3])  # sets the last element in the list to how many elements are in the cluster
        Z.append(row)
    return np.array(Z)


def hac_lines(dataset):
    dataset = make_valid(dataset)
    m = len(dataset)
    line_points = []  # the list to return
    clusters = []
    goal_dist = 0
    point_1, point_2 = 0, 0
    for i in range(m):
        clusters.append({"#": i, "Points": [dataset[i]]})
    for row_num in range(m - 1):  # for indices 20-39
        smallest = dict.fromkeys(["C1", "C2", "Dist", "Points"])
        smallest.update({"Dist": 999999})
        for c1 in clusters:
            for c2 in clusters:
                if c1 != c2:
                    for p1 in c1["Points"]:
                        for p2 in c2["Points"]:
                            dist = calc_cluster_distance(p1, p2)
                            if dist < smallest["Dist"]:
                                smallest.update(update_smallest(c1, p1, c2, p2))
                            elif dist == smallest["Dist"]:
                                smallest = tie_break(c1, p1, c2, p2, smallest)
        clusters = [c for c in clusters if not (c["#"] == smallest["C1"] or c["#"] == smallest["C2"])]
        clusters.append({"#": m + row_num, "Points": smallest["Points"]})
        row = [points for points in smallest.values()]
        goal_dist = row[2]
        for p1 in row[3]:
            for p2 in row[3]:
                if p1 != p2 and ([p1, p2] not in line_points and [p2, p1] not in line_points) \
                        and (p1 in row[3] and p2 in row[3]):
                    x_1 = p1[0]
                    y_1 = p1[1]
                    x_2 = p2[0]
                    y_2 = p2[1]
                    dist = math.sqrt(((x_2 - x_1) ** 2) + ((y_2 - y_1) ** 2))
                    if dist == goal_dist:
                        if x_1 < x_2:
                            point_1 = p1
                            point_2 = p2
                        elif x_1 == x_2:
                            if y_1 < y_2:
                                point_1 = p1
                                point_2 = p2
                            else:
                                point_1 = p2
                                point_2 = p1
                        else:
                            point_1 = p2
                            point_2 = p1
        line_points.append([point_1, point_2])
    return line_points


def random_x_y(m):
    random_num_list = []
    for num in range(m):
        x = random.randrange(1, 359)
        y = random.randrange(1, 359)
        random_num_list.append((x, y))
    return random_num_list


def imshow_hac(dataset):
    x_val = []
    y_val = []
    color = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
             'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan',
             'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
             'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    for point in dataset:
        x_val.append(point[0])
        y_val.append(point[1])
    line_points = hac_lines(dataset)
    if len(x_val) == 20:
        plt.scatter(x_val, y_val, c=color)
    else:
        plt.scatter(x_val, y_val)
    for line in line_points:
        x_vals = [line[0][0], line[1][0]]
        y_vals = [line[0][1], line[1][1]]
        plt.plot(x_vals, y_vals)
        plt.pause(0.1)
    plt.show()
