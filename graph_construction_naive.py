#!/usr/bin/env python3
#
# Creates a graph from the raw skeleton data. The construction algorithm
# is naive and merely checks for all neighbouring pixels, including the
# diagonal one.

import sys

coordinates = set()

width  = 839 
height = 396

"""
Union-find data structure for partitioning the graph into connected
components segments, which may then subsequently be partitioned into
individual segments.
"""
class UnionFind:
    def __init__(self, vertices):
        self.components = dict()

        for vertex in vertices:
            self.components[vertex] = vertex

    """ Parent access with path compression """
    def find(self, vertex):
        if self.components[vertex] == vertex:
            return vertex

        # Path compression
        else:
            self.components[vertex] = self.find( self.components[vertex] )
            return self.components[vertex]

    """ Provides merging functionality """
    def merge(self, u, v):
        cu = self.find(u)
        cv = self.find(v)

        self.components[cu] = cv

    """ Generator for all roots """
    def roots(self):
        for vertex in sorted( self.components.keys() ):
            if self.find(vertex) == vertex:
                yield vertex

    """ Gets all vertices of a specific connected component """
    def vertices(self, root):
        result = list()

        for vertex in self.components.keys():
            if self.find(vertex) == root:
                result.append( vertex )

        return sorted(result)

"""
Basic node class
"""
class Node:
    def __init__(self,x,y,i):
        self.x = x
        self.y = y
        self.i = i # Node ID

def valid(x,y):
    return x >= 0 and x < width and y >= 0 and y < height

def neighbours(x,y):
    offset = [
        ( 0,-1),
        (+1,-1),
        (+1, 0),
        (+1,+1),
        ( 0,+1),
        (-1,+1),
        (-1, 0),
        (-1,-1)
    ]

    return list( filter( lambda x : valid(x[0],x[1]), [ (x+ox,y+oy) for (ox,oy) in offset ] ) )

with open(sys.argv[1]) as f:
    coordinates    = dict()
    edges          = list()
    vertices       = set()
    degrees        = dict()

    for index,line in enumerate(f):
        (x,y)                   = [ int(a) for a in line.split() ]
        coordinates [ (x,y) ]   = index

    #
    # Graph creation
    #

    for (x,y) in sorted( coordinates.keys() ):
        for (a,b) in neighbours(x,y):
            if (a,b) in coordinates:
                u = coordinates[ (x,y) ]
                v = coordinates[ (a,b) ]

                vertices.add(u)
                vertices.add(v)

                if u < v:
                    degrees[u] = degrees.get(u, 0) + 1
                    degrees[v] = degrees.get(v, 0) + 1

                    edges.append( (u,v) )
    
    #
    # Calculate connected components
    #

    uf = UnionFind(vertices)

    for (u,v) in edges:
        uf.merge(u,v)

    for root in uf.roots():
        print(root, len(uf.vertices(root)))

    #
    # Segment the graph
    #

    regularVertices  = [ vertex for vertex in vertices if degrees[vertex] <= 2 ]
    partitionedEdges = [ (u,v) for (u,v) in edges if degrees[u] <= 2 and degrees[v] <= 2 ]
    branchEdges      = [ (u,v) for (u,v) in edges if degrees[u] > 2 or degrees[v] > 2 ]

    ufSegments = UnionFind(regularVertices)

    for (u,v) in partitionedEdges:
        ufSegments.merge(u,v)

    for root in ufSegments.roots():
        print(root, len(ufSegments.vertices(root)))

    # TODO: Add missing vertices to segments

# TODO:
# - Identify segments (union-find)
# - Obtain 'point-to-segment' map
# - Upon matching, keep track of how many points of a segment are being matched
# - 100% segments may be ignored (by greedy matching)
