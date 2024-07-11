from typing import List, Self

class VRFiltrationIndexedCell:
    """
    A class to represent a n-dimensional cell.

    Attributes:
    - vertices (list): A list of indices representing the vertices of the cell
    - dimension (int): Dimension of the cell
    - facets (list): A list of facets of the cell
    - cofacets (list): A list of cofacets of the cell
    """

    def __init__(self, vertices: List[int]):
        """
        Initialize a new cell with the given vertex indices

        Parameters:
        vertices (list): A list of indices representing the vertices of the cell
        """

        assert(len(vertices) > 0)
        assert(len(set(vertices)) == len(vertices))
        self.vertex_set = set(vertices)
        self.dimension = len(vertices) - 1
        self.co_1_faces: List[Self] = []
        self.co_neg_1_cofaces: List[Self] = []
    
    def add_co_1_face(self, other: Self):
        """
        Add a codimension 1 face
        """
        assert(other.is_face_of(self) == 1)
        self.co_1_faces.append(other)

    def add_co_neg_1_coface(self, other: Self):
        """
        Add a codimension -1 face
        """
        assert(self.is_face_of(other) == 1)
        self.co_neg_1_cofaces.append(other)
    
    def is_face_of(self, other: Self):
        """
        Returns the codimension of other w.r.t self, returns -1 if not a face
        """

        if self.dimension >= other.dimension:
            return -1
        
        if self.vertex_set.issubset(other.vertex_set):
            return len(other.vertex_set) - len(self.vertex_set)
        
        return -1


        

    def __repr__(self):
        return f"{self.dimension}-Cell: {self.sorted_vertices}"
    
class VRFiltrationSimplicialComplex:
    """
    A class to represent a VR Filtration simplicial complex

    Attributes:
    - maximal_simplices (list): A list of IndexedCells representing the maximal simplices
    - num_vertices (int): A number of vertices, assumed to be unchanging
    - dimension (int): The dimension of the maximal simplex
    - n_simplex_dict (dict): A dictionary of all the simplices per dimension
    """
    
    def __init__(self, maximal_simplices: List[VRFiltrationIndexedCell]):
        self._check_full_vertex_range(maximal_simplices)
        self._check_no_faces(maximal_simplices)

        #
    
    def _check_full_vertex_range(maximal_simplices: List[VRFiltrationIndexedCell]):
        # check that each vertex is represented from [1,n]
        vertex_tracker = set()
        for maximal_simplex in maximal_simplices:
            for vertex_index in maximal_simplex.sorted_vertices:
                vertex_tracker.add(vertex_index)
        
        max_vertex = max(vertex_tracker)
        full_range = set(range(1, max_vertex+1))

        assert(full_range.issubset(vertex_tracker))
    
    def _check_no_faces(maximal_simplices: List[VRFiltrationIndexedCell]):
        for i in range(len(maximal_simplices)-1):
            for j in range(i+1, len(maximal_simplices)):
                assert(maximal_simplices[i].is_face_of(maximal_simplices[j]) == -1)
                assert(maximal_simplices[j].is_face_of(maximal_simplices[i]) == -1)

def main():
    bruh = VRFiltrationIndexedCell([1,2,3])
    bruhh = VRFiltrationIndexedCell([3])

    print(bruhh.is_face_of(bruh))


if __name__ == "__main__":
    main()


    
