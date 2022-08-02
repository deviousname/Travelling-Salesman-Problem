import random
import math
import time
import pygame

width, height = 512, 512
amount_of_cities = 16

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def generate_points(n):
    points = []
    for i in range(n):
        points.append((random.randint(0, width), random.randint(0, height)))
    return points

def generate_path(points):
    path = []
    for i in range(len(points)):
        path.append(i)
    random.shuffle(path)
    return path

def path_length(path, points):
    length = 0
    for i in range(len(path) - 1):
        length += distance(points[path[i]], points[path[i + 1]])
    length += distance(points[path[0]], points[path[-1]])
    return length

def swap(path, i, j):
    temp = path[i]
    path[i] = path[j]
    path[j] = temp

def two_opt(path, points):
    best_path = path[:]
    best_length = path_length(path, points)
    for i in range(len(path) - 1):
        for j in range(i + 1, len(path)):
            swap(path, i, j)
            length = path_length(path, points)
            if length < best_length:
                best_path = path[:]
                best_length = length
            swap(path, i, j)
    return best_path

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Travelling Salesman Problem")
    screen.fill((255, 255, 255))
    points = generate_points(amount_of_cities)
    path = generate_path(points)
    print(path)
    print(path_length(path, points))
    path = two_opt(path, points)
    print(path)
    print(path_length(path, points))
    for i in range(len(path) - 1):
        pygame.draw.line(screen, (0, 0, 0), points[path[i]], points[path[i + 1]], 1)
    pygame.draw.line(screen, (0, 0, 0), points[path[0]], points[path[-1]], 1)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

main()
