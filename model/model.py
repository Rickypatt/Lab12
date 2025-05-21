import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._graph = nx.Graph()

    def buildGraph(self, country, anno):
        self._graph.clear()
        allNodes = DAO.getRetailers(country)
        for n in allNodes:
            self._idMap[n.Retailer_code] = n

        self._graph.add_nodes_from(allNodes)
        allEdges = DAO.getArchi(country,anno)
        for e in allEdges:
            self._graph.add_edge(self._idMap[e[0]],self._idMap[e[1]],weight = e[2])

    def getPesoVicini(self):
        diz = {}

        for n in self._graph.nodes:
            somma = 0
            for v in self._graph.neighbors(n):
                somma += self._graph[n][v]["weight"]

            diz[n] = somma

        ordinato = sorted(diz.items(), key=lambda item: item[1], reverse=True)
        return ordinato

    def getOptPath(self,n):

        self.solBest = []
        self.bestCosto = 0
        self.ricorsione([],n)
        return self.solBest,self.bestCosto

    def ricorsione(self,parziale,n):



    def getCountry(self):
        return DAO.getCountry()

    def getAnni(self):
        return DAO.getAnni()

    def getNumberOfNodes(self):
        return self._graph.number_of_nodes()

    def getNumberOfEdges(self):
        return self._graph.number_of_edges()

