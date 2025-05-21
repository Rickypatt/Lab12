import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        self._listaCountry = self._model.getCountry()
        self._listaAnni = self._model.getAnni()

        for c in self._listaCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        for a in self._listaAnni:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        self._view.update_page()

    def handle_graph(self, e):
        nazione = self._view.ddcountry.value
        anno = self._view.ddyear.value
        if nazione is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione! Selezionare una nazione"))
            self._view.update_page()
            return

        if anno is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione! Selezionare una anno"))
            self._view.update_page()
            return

        try:
            annoint = int(anno)

        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione! Anno non è un intero"))
            self._view.update_page()
            return

        self._model.buildGraph(nazione, annoint)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumberOfNodes()} Numero di archi: {self._model.getNumberOfEdges()}"))
        self._view.update_page()

    def handle_volume(self, e):
        dizionario = self._model.getPesoVicini()
        for i in dizionario:
            self._view.txtOut2.controls.append(ft.Text(f"{i[0]} --> {i[1]}"))
            self._view.update_page()




    def handle_path(self, e):
        pass
