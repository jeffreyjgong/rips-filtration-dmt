class IndexedCell:
    """
    A class to represent a n-dimensional cell.

    Attributes:
    - vertices (list): A list of indices representing the vertices of the cell
    - dimension ()
    """
    def __init__(self, vertices):
        """
        Initialize a new cell with the given vertex indices

        Parameters:
        vertices (list): A list of indices representing the vertices of the cell
        """

        assert(len(vertices) > 0)
        assert(len(set(vertices)) == len(vertices))
        self.sorted_vertices = sorted(vertices)
        self.dimension = len(vertices) - 1
    
    def __repr__(self):
        return f"{self.dimension}-Cell: {self.sorted_vertices}"
    

def main():
    bruh = IndexedCell([1,2,3])
    print(bruh)


if __name__ == "__main__":
    main()


    
