import tabulate as tab


class Node:
    def __init__(self):
        self.edge_list = []
        self.visited = False
        return


class Edge:
    def __init__(self, start: str, end: str, cost: int):
        self.start = start
        self.end = end
        self.cost = cost
        return


class PriorityQueue:
    def __init__(self):
        self.queue = []
        return

    def put(self, edge: Edge):
        self.queue.append(edge)
        self.queue.sort(key=lambda x: x.cost, reverse=True)
        return

    def get(self) -> Edge:
        if self.queue:
            return self.queue.pop()
        else:
            raise Exception("Can't get from empty queue")

    def is_empty(self):
        if self.queue:
            return False
        return True


class Graph:
    def __init__(self):
        self.node_list = {}
        self.priority_queue = PriorityQueue()
        return

    def add_node(self, name: str, node_list: list, weight_list: list):
        if len(node_list) == len(weight_list):
            new_node = Node()
            if name in self.node_list:
                new_node = self.node_list[name]
            for i in range(len(node_list)):
                edge = Edge(name, node_list[i], weight_list[i])
                new_node.edge_list.append(edge)
            self.node_list[name] = new_node
        else:
            raise Exception("Node list an weight list are not the same size")
        return

    def queue_edges(self, name: str):
        node = self.node_list[name]
        node.visited = True
        for edge in node.edge_list:
            next_node = self.node_list[edge.end]
            if not next_node.visited:
                self.priority_queue.put(edge)
        return

    def prim(self, start_node="0"):
        mst = []
        self.queue_edges(start_node)
        while not self.priority_queue.is_empty():
            edge = self.priority_queue.get()
            node = self.node_list[edge.end]
            if not node.visited:
                mst.append(edge)
                self.queue_edges(edge.end)
        print("Minimum Spanning Tree")
        for edge in mst:
            print(edge.start, "->", edge.end)


def main():
    graph = Graph()
    graph.add_node("0", ["1", "2", "3"], [10, 2, 3])
    graph.add_node("1", ["0", "2", "4"], [10, 3, 0])
    graph.add_node("2", ["0", "1", "3", "5"], [1, 3, 2, 8])
    graph.add_node("3", ["0", "2", "5", "6"], [4, 2, 2, 7])
    graph.add_node("4", ["1", "5", "7"], [0, 8, 8])
    graph.add_node("5", ["2", "3", "4", "6", "7"], [8, 2, 1, 6, 9])
    graph.add_node("6", ["3", "5", "7"], [7, 6, 12])
    graph.add_node("7", ["4", "5", "6"], [8, 9, 12])
    graph.prim()

    # graph.priority_queue.put(Edge("A", "B", 2))
    # graph.queue_min_edge("A")
    # graph.priority_queue.print_queue()
    # graph.queue_min_edge("B")
    # graph.priority_queue.print_queue()

    # graph.add_node("0", ["2", "5", "3", "1"], [0, 7, 5, 9])
    # graph.add_node("1", ["0", "3", "6", "4"], [9, -2, 4, 3])
    # graph.add_node("2", ["0", "5"], [0, 6])
    # graph.add_node("3", ["0", "5", "6", "1"], [5, 2, 3, -2])
    # graph.add_node("4", ["1", "6"], [3, 6])
    # graph.add_node("5", ["2", "0", "3", "6"], [6, 7, 2, 1])
    # graph.add_node("6", ["5", "3", "1", "4"], [1, 3, 4, 6])
    # graph.eager_prim()

    # graph.prim()
    # graph.add_node("0", ["1", "2", "3"], [10, 2, 3])
    # graph.add_node("1", ["0", "2", "4"], [10, 3, 0])
    # graph.add_node("2", ["0", "1", "3", "5"], [1, 3, 2, 8])
    # graph.add_node("3", ["0", "2", "5", "6"], [4, 2, 2, 7])
    # graph.add_node("4", ["1", "5", "7"], [0, 8, 8])
    # graph.add_node("5", ["2", "3", "4", "6", "7"], [8, 2, 1, 6, 9])
    # graph.add_node("6", ["3", "5", "7"], [7, 6, 12])
    # graph.add_node("7", ["4", "5", "6"], [8, 9, 12])

    return


if __name__ == '__main__':
    main()
