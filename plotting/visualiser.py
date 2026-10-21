import matplotlib.pyplot as plt
import numpy as np
from inline_labels import add_inline_labels

class Visualiser:
    def __init__(self, frame, results):
        self.frame = frame
        self.results = results

    def _plot_elements(self, ax):
        for i, element in enumerate(self.frame.elements, start=1):
            x = [element.start.x, element.end.x]
            y = [element.start.y, element.end.y]
            ax.plot(x, y, 'k', label = i)
            add_inline_labels(ax)

    def _plot_nodes(self, ax):
        for node in self.frame.nodes:
            ax.plot(node.x, node.y, "ko")
            ax.annotate(node.id, (node.x, node.y))

    def _load_position(self, load):
        element = load.element
        start = element.start
        end = element.end

        dx = end.x - start.x
        dy = end.y - start.y
        L = element.length()

        x_load = start.x + (load.a / L) * dx
        y_load = start.y + (load.a / L) * dy

        return x_load, y_load

    def _load_direction(self, load):
        element = load.element

        dx = element.end.x - element.start.x
        dy = element.end.y - element.start.y

        theta = np.arctan2(dy, dx)

        local_x = np.cos(load.angle)
        local_y = -np.sin(load.angle)

        direction_x = (
            np.cos(theta) * local_x
            - np.sin(theta) * local_y
            )

        direction_y = (
            np.sin(theta) * local_x
            + np.cos(theta) * local_y
            )

        return direction_x, direction_y

    def _plot_loads(self, ax):
        arrow_length = 0.2 * self.frame.elements[0].length()

        for load in self.frame.loads:
            direction_x, direction_y = self._load_direction(load)
            x_load, y_load = self._load_position(load)

            ax.annotate(
                f"{load.P} kN",
                (x_load, y_load),
                (
                    x_load - arrow_length * direction_x,
                    y_load - arrow_length * direction_y
                    ),
                arrowprops=dict(arrowstyle="->")
                )

    def plot_frame_structure(self):
        fig, ax = plt.subplots()

        self._plot_elements(ax)
        self._plot_nodes(ax)
        self._plot_loads(ax)

        ax.set_aspect('equal')
        ax.grid(True)

        plt.show()