""" Remember, to use a file in sage, you have to
`attach([file])`. 

The grey algorithm simply cycle to all possible edge
orientations permutations to generate all the possible
orientations.
 """

from time import process_time_ns


def compute_orientations_grey_algorithm(graph, girth=+Infinity):
    a = process_time_ns()
    orientations = grey_algorithm(graph, girth)
    b = process_time_ns()
    print(
        f"Found {len(orientations)} orientations in {(b-a)/1000000000}s"
    )

def grey_algorithm(graph, girth):
    nAcyclic_orientations = []
    for orientation in graph.orientations():
        if orientation.girth() >= girth:
            nAcyclic_orientations.append(orientation.edges(labels=False))
    return nAcyclic_orientations


triangle_orientations = [[(0,1),(1,2),(2,0)]]
class TestGreyAlgorithm:
    """How can you test sage files?"""

    def test_grey_algorithm_triangle(self):
        graph = Graph([(0,1),(1,2),(2,0)])
        orientations = grey_algorithm(graph)
        assert orientations == triangle_orientations
