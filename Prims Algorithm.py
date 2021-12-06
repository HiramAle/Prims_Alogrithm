import tabulate as tab
from colors import red, green, blue


class Node:
    def __init__(self) -> None:
        """
        Constructor from Node Class
        """
        # List of edges
        self.edge_list = []
        # Visited flag for Node
        self.visited = False
        return


class Edge:
    def __init__(self, start: str, end: str, cost: int) -> None:
        """
        Constructor for Edge
        :param start: Start Node for the Edge
        :param end: End Node for the Edge
        :param cost: Cost of the Edge
        """
        self.start = start
        self.end = end
        self.cost = cost
        return

    def print_info(self) -> None:
        """
        Prints the info of the Edge using the notation
        Start_Node -> End_Node (Cost)
        :return: None
        """
        print(self.start, "->", self.end, "(" + str(self.cost) + ")")
        return


class PriorityQueue:
    def __init__(self) -> None:
        """
        Constructor from the PriorityQueue
        """
        # Queue to store the Edges in the PriorityQueue
        self.queue = []
        return

    def put(self, edge: Edge) -> None:
        """
        Put and Edge in the Queue and print the actual PriorityQueue
        :param edge: Edge to add
        :return: None
        """
        self.queue.append(edge)
        # Ones the Edge is added, sort the queue from from highest to lowest
        self.queue.sort(key=lambda x: x.cost, reverse=True)
        # Prints the Queue info
        print(blue("Put:"), end=" ")
        edge.print_info()
        self.print_queue()
        return

    def get(self) -> Edge:
        """
        Pop up the last Edge in the queue ('Cause the queue is sort by thew cost of the Edge from highest to
        lowest, the last Edge in the queue is the cheapest Node in the queue).
        :return: Edge: Return the last Edge in the queue
        """
        if self.queue:
            edge = self.queue.pop()
            print(red("Get:"), end=" ")
            edge.print_info()
            self.print_queue()
            return edge
        else:
            # In case the queue is empty
            raise Exception("Can't get from empty queue")

    def is_empty(self) -> bool:
        """
        Check if the queue is empty and return True or False
        :return: True if is empty and False if not
        """
        if self.queue:
            return False
        return True

    def node_in_queue(self, node_name: str) -> bool:
        """
        Check it is an Edge in the queue that points to the Node required
        :param node_name: Name of the node to search in the Edges Queue
        :return: True if it is and Edge pointing to the Node, and False if not
        """
        for edge in self.queue:
            if node_name == edge.end:
                return True
        return False

    def get_edge(self, node: str) -> Edge:
        """
        Only used in Eager Implementation
        Pop Up the Edge from the Priority Queue that points to the node searched
        :param node: Name of the Node to search
        :return: Edge
        """
        for i, edge in enumerate(self.queue):
            if node == edge.end:
                return self.queue.pop(i)

    def print_queue(self) -> None:
        """
        Print the Priority Queue
        :return: None
        """
        data = []
        for edge_queue in self.queue:
            data.append([edge_queue.start + " -> " + edge_queue.end + " (" + str(edge_queue.cost) + ") "])
        print(tab.tabulate(data, headers=["Priority Queue"], tablefmt="psql"))
        return


class Graph:
    def __init__(self) -> None:
        """
        Constructor for the Graph
        """
        # Node list
        self.node_list = {}
        # Priority Queue from the Graph
        self.priority_queue = PriorityQueue()
        return

    def add_node(self, name: str, node_list: list, weight_list: list) -> None:
        """
        Adds a Node to the Graph
        :param name: Name of the Node
        :param node_list: The adjacency list of the Node
        :param weight_list: The weights of the edges of each Node in the adjacency list
        :return: None
        """
        if len(node_list) == len(weight_list):
            new_node = Node()
            if name in self.node_list:
                new_node = self.node_list[name]
            for i in range(len(node_list)):
                edge = Edge(name, node_list[i], weight_list[i])
                new_node.edge_list.append(edge)
            self.node_list[name] = new_node
        else:
            # In case the parameters of the node_list and the weight_list are not the same size
            raise Exception("Node list an weight list are not the same size")
        return

    def queue_edges(self, name: str) -> None:
        """
        Queue the Edge in the Priority Queue only if the pointing Node is not visited
        :param name: Name of the Node to queue
        :return: None
        """
        # Get the node from the node_list of the Graph
        node = self.node_list[name]
        # Set the Node visited
        node.visited = True
        # Iterates the edge_list of the node
        for edge in node.edge_list:
            # Get the pointing Node of the Edge
            next_node = self.node_list[edge.end]
            # Only adds the Edge if it's visited
            if not next_node.visited:
                self.priority_queue.put(edge)
        return

    def queue_min_edge(self, name: str) -> None:
        """
        Only used in the Eager version.
        Check if there's an Edge that points to the Node searched
        If there's no Edge pointing to that Node, adds the Edge to the Priority Queue
        If there's an Edge pointing to that Node, compare the actual Edge and the one in the Priority Queue
        If the actual Edge cost less than the one in the Priority Queue, adds the Edge to the Priority Queue
        Otherwise adds the other Edge back to the Priority Queue
        :param name: Name of the Node to search
        :return: None
        """
        # Get the node to search in
        node = self.node_list[name]
        # Set the node to visited
        node.visited = True
        # Iterates the edge_list of the node
        for edge in node.edge_list:
            # Get the pointing Node of the edge
            name_point_node = edge.end
            point_node = self.node_list[name_point_node]
            # Check if the pointing node is already visited
            if not point_node.visited:
                # Check if the Priority Queue has an Edge that points to the Node
                if self.priority_queue.node_in_queue(name_point_node):
                    # Get the Edge in the Priority Queue that already points to the Node
                    existing_edge = self.priority_queue.get_edge(name_point_node)
                    # Check if the actual Edge is cheaper than the Edge in the Priority Queue
                    if edge.cost <= existing_edge.cost:
                        # Add the actual node to the Priority Queue
                        self.priority_queue.put(edge)
                    else:
                        # Return the existing edge to the Priority Queue
                        self.priority_queue.put(existing_edge)
                else:
                    # If  there isn't any Edge pointing to that Node, adds the Edge to the Priority Queue
                    self.priority_queue.put(edge)
        return

    def lazy_prim(self, start_node="A"):
        """
        Start the Lazy Prim's Algorithm in the starting node.
        :param start_node: Indicates the name of the starting node. Default: A
        """
        # Set the Priority Queue to an empty Queue
        self.priority_queue = PriorityQueue()
        # Store the Minimum Spanning Tree
        mst = []
        # Start to queue the edges in the starting node
        self.queue_edges(start_node)
        # As long as the priority queue is not empty, the algorithm continues
        while self.priority_queue.queue:
            # Get the cheapest Edge and the pointing Node
            edge = self.priority_queue.get()
            node = self.node_list[edge.end]
            # If the node is already visited, skip the node
            if not node.visited:
                mst.append(edge)
                self.queue_edges(edge.end)
        # Print the MST information
        print(green("Minimum Spanning Tree"))
        cost = 0
        for edge in mst:
            print(edge.start, "->", edge.end)
            cost += edge.cost
        print("Cost:", cost)

    def eager_prim(self, start_node="A"):
        """
        Start the Eager Prim's Algorithm in the starting node.
        :param start_node: Indicates the name of the starting node. Default: A
        """
        # Set the Priority Queue to an empty list
        self.priority_queue = PriorityQueue()
        # Store the Minimum Spanning Tree
        mst = []
        # Queue the Edges from the starting node
        self.queue_min_edge(start_node)
        # As long as the priority queue is not empty, the algorithm continues
        while self.priority_queue.queue:
            # If the node is already visited, skip the node
            edge = self.priority_queue.get()
            node = self.node_list[edge.end]
            # If the node is already visited, skip the node
            if not node.visited:
                self.queue_min_edge(edge.end)
                mst.append(edge)
        # Print the MST information
        print(green("Minimum Spanning Tree"))
        cost = 0
        for edge in mst:
            print(edge.start, "->", edge.end)
            cost += edge.cost
        print("Cost:", cost)


def main():
    graph = Graph()
    graph.add_node("A", ["B", "H"], [4, 8])
    graph.add_node("B", ["A", "H", "C"], [4, 11, 8])
    graph.add_node("C", ["B", "I", "F", "D"], [8, 2, 4, 7])
    graph.add_node("D", ["C", "F", "E"], [7, 14, 9])
    graph.add_node("E", ["D", "F"], [9, 10])
    graph.add_node("F", ["G", "C", "D", "E"], [2, 4, 14, 10])
    graph.add_node("G", ["H", "I", "F"], [1, 6, 2])
    graph.add_node("H", ["A", "B", "I", "G"], [8, 11, 7, 1])
    graph.add_node("I", ["H", "G", "C"], [7, 6, 2])
    # graph.lazy_prim()
    graph.eager_prim()

    return


if __name__ == '__main__':
    main()
