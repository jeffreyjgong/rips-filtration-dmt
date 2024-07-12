from types import NotImplementedType
from typing import Dict, List, Self

class VRFiltrationIndexedCell:
    """
    A class to represent a n-dimensional cell.

    Attributes:
    - vertices (list): A list of indices representing the vertices of the cell
    - dimension (int): Dimension of the cell
    - facets (list): A list of facets of the cell
    - cofacets (list): A list of cofacets of the cell
    """

    def __init__(self, vertices: List[int]) -> None:
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
    
    def add_co_1_face(self, other: Self) -> None:
        """
        Add a codimension 1 face
        """
        assert(other.is_face_of(self) == 1)
        self.co_1_faces.append(other)

    def add_co_neg_1_coface(self, other: Self) -> None:
        """
        Add a codimension -1 face
        """
        assert(self.is_face_of(other) == 1)
        self.co_neg_1_cofaces.append(other)
    
    def is_face_of(self, other: Self) -> int:
        """
        Returns the codimension of other w.r.t self, returns -1 if not a face
        """

        if self.dimension >= other.dimension:
            return -1
        
        if self.vertex_set.issubset(other.vertex_set):
            return len(other.vertex_set) - len(self.vertex_set)
        
        return -1

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Self):
            return NotImplemented
        
        return self.vertex_set == other.vertex_set

    def __repr__(self) -> str:
        return f"{self.dimension}-Cell: {self.sorted_vertices}"
    
class VRFiltrationSimplicialComplex:
    """
    A class to represent a VR Filtration simplicial complex

    Attributes:
    - maximal_simplices (list): A list of IndexedCells representing the maximal simplices
    - num_vertices (int): A number of vertices, assumed to be unchanging
    - dimension (int): The dimension of the maximal simplex
    - n_cell_dict (dict): A dictionary of all the simplices per dimension
    """
    
    def __init__(self, maximal_simplices: List[VRFiltrationIndexedCell]) -> None:
        self._check_no_faces(maximal_simplices)
        self.num_vertices = self._check_and_output_full_vertex_range(maximal_simplices)
        
        self.dimension = max((len(cell_iter.vertex_set) - 1) for cell_iter in maximal_simplices)
        self.n_cell_dict: Dict[int, List[VRFiltrationIndexedCell]] = {}
        
        for dim in range(0, self.dimension+1):
            self.n_cell_dict[dim] = []
        
        for maximal_simplex in maximal_simplices:
            self._enumerate_and_add(maximal_simplex)
    
    def _check_and_output_full_vertex_range(self, maximal_simplices: List[VRFiltrationIndexedCell]) -> int:
        # check that each vertex is represented from [1,n]
        vertex_tracker = set()
        for maximal_simplex in maximal_simplices:
            for vertex_index in maximal_simplex.sorted_vertices:
                vertex_tracker.add(vertex_index)
        
        max_vertex = max(vertex_tracker)
        full_range = set(range(1, max_vertex+1))

        assert(full_range.issubset(vertex_tracker))
        
        return max_vertex
    
    def _check_no_faces(self, maximal_simplices: List[VRFiltrationIndexedCell]) -> None:
        # check that no maximal simplices are faces of each other
        for i in range(len(maximal_simplices)-1):
            for j in range(i+1, len(maximal_simplices)):
                assert(maximal_simplices[i].is_face_of(maximal_simplices[j]) == -1)
                assert(maximal_simplices[j].is_face_of(maximal_simplices[i]) == -1)
    
    def _add_cell(self, cell_to_add: VRFiltrationIndexedCell) -> None:
        """
        Function to add a cell to the cell dict

        Assumes
        - dimension has already been set
        """
        assert(cell_to_add.dimension >= 0 and cell_to_add.dimension <= self.dimension)
        assert(cell_to_add not in self.n_cell_dict[cell_to_add.dimension])
        self.n_cell_dict[cell_to_add.dimension].append(cell_to_add)
    
    def _enumerate_and_add(self, maximal_simplex: VRFiltrationIndexedCell) -> None:
        # dim = maximal_simplex.dimension
        # max_enum = (1 << (dim + 1)) - 1

        # for enum_iter in range(1, max_enum+1):

        pass
    
    

def _binary_format_list(num: int, size: int) -> List[int]:
        binary_representation = bin(num)[2:][::-1]

        binary_list = [int(bit) for bit in binary_representation]

        # ensure list is of specified size by padding w zeros
        while len(binary_list) < size:
            binary_list.append(0)
        
        return binary_list[:size][::-1]



def main():
    bruh = VRFiltrationIndexedCell([1,2,3])
    bruhh = VRFiltrationIndexedCell([3])

    print(bruhh.is_face_of(bruh))

    print(_binary_format_list(31, 5))


if __name__ == "__main__":
    main()


    
