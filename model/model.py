import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._graph = nx.Graph()
        self.solBest = []
        self.bestCosto = 0

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

    def getOptPath(self, nEdges):

        self.solBest = []
        self.bestCosto = 0
        parziale = []
        for start in self._graph.nodes:
            self.ricorsione(parziale, nEdges, start, [start])
        return self.solBest,self.bestCosto

    def ricorsione(self,parziale,nEdges, start, visitati):

        if len(parziale) > 0:
            nodoCorrente = parziale[-1][1]
        else:
            nodoCorrente = start

        if len(parziale) == nEdges:
            if nodoCorrente == start:
                if self.score(parziale) > self.bestCosto:
                    self.bestCosto = self.score(parziale)
                    self.solBest = copy.deepcopy(parziale)
        else:
            for v in self._graph.neighbors(nodoCorrente):
                if v == start and len(parziale) == nEdges - 1:
                        # Ultimo passo: torna al nodo iniziale
                        parziale.append((nodoCorrente, v, self._graph[nodoCorrente][v]['weight']))
                        self.ricorsione(parziale, nEdges, start, visitati)
                        parziale.pop()
                elif v not in visitati:
                    parziale.append((nodoCorrente, v, self._graph[nodoCorrente][v]['weight']))
                    visitati.append(v)
                    self.ricorsione(parziale, nEdges, start, visitati)
                    visitati.remove(v)
                    parziale.pop()


    def score(self,listaDiArchi):
        tot = 0
        for i in listaDiArchi:
            tot += i[2]

        return tot

    def getCountry(self):
        return DAO.getCountry()

    def getAnni(self):
        return DAO.getAnni()

    def getNumberOfNodes(self):
        return self._graph.number_of_nodes()

    def getNumberOfEdges(self):
        return self._graph.number_of_edges()

