def carregarCaminhos():
    arq = open("dados_rodoviaria.csv", 'r')
    arq = arq.readlines()
    arq = arq[0:112]
    caminho = []
    dic_locais = {}
    cont = 0

    for linha in arq:
        l = linha.split(';')
        print(l,"antes da linha onze")
        l = l[0:-6]
        print(l)
        if cont == 0:
            cont1 = 0
            for i in l:
                if i != "":
                    dic_locais[cont1] = i
                    cont1 += 1

        if cont != 0:
            cont1 = 0
            for i in l:
                if cont1 == 38:
                    break
                if cont1 != 0:
                    if i != "none":
                        tupla = (l[0], dic_locais[cont1 - 1], int(i))
                    else:
                        tupla = (l[0], dic_locais[cont1 - 1], None)
                    caminho.append(tupla)
                cont1 += 1

        cont += 1
        nVert = len(dic_locais)
    return caminho, nVert, dic_locais

def insert_caminhos(caminhos):
    for caminho in caminhos:
        c1, c2, p = caminho[0], caminho[1], caminho[2]
        graph.insert_aresta(c1,c2,p)
        print("Rotas inseridas com sucesso")


class Grafo():
    def __init__(self, nVert, dic_locais, ponderado = True):
        self.vertices = nVert
        self.arestas = 0
        self.matriz = []
        self.legenda = {}
        self.ponderado = ponderado
        self.id = dic_locais

        cont = nVert
        for i in range(nVert):
            array = [None]*nVert
            self.matriz.append(array)
            self.legenda[i] = [self.id[i],[]]
            cont -= 1
        del cont

    def insert_aresta(self, c1, c2, peso = None):
        cont = 0
        cVert = [c1, c2]

        for i in self.legenda:
            if cVert[0] == self.legenda[i][0]:
                cVert[0] = i
                cont += 1
            if cVert[1] == self.legenda[i][1]:
                cVert[1] = i
                cont += 1
            if cont == 2:
                break

        min_i, max_i = 0, 1

        if self.matriz[min_i][max_i - min_i] is None:
            self.arestas += 1
            self.legenda[min_i][1].append(self.legenda[max_i][0])
            self.legenda[max_i][1].append(self.legenda[min_i][0])
        self.matriz[min_i][max_i - min_i] = peso

    def imprimir_grafo(self):
        cont = 0
        numVert = self.vertices
        while cont < numVert:
            print(self.legenda[cont][0], self.matriz[cont])
            cont += 1

    def aux_cnome(self, vert):
        for i in self.legenda:
            if self.legenda[i][0] == vert:
                cNome = i
                return cNome
        return False

    def check_peso(self, c1, c2):
        min_i, max_i = min([c1,c2]), max([c1,c2])
        peso = self.matriz[min_i][max_i - min_i]
        return peso

    def dijkstra(self, inicio, fim, instr = None):
        cInicio, cFim = self.aux_cnome(inicio), self.aux_cnome(fim)
        caminho, mCaminho, antecessor, notVisitados, nInf = [], {}, {}, list(self.legenda.keys()), 10*8
        for vertice in notVisitados:
            mCaminho[vertice] = nInf
        mCaminho[cInicio] = 0

        while notVisitados:
            min_vert = None
            for vertice in notVisitados:
                if min_vert is None:
                    min_vert = vertice

                elif mCaminho[vertice] < mCaminho[min_vert]:
                    min_vert = vertice

            for adjacente in self.legenda[min_vert][1]:
                adjacente = self.aux_cnome(adjacente)
                peso = self.check_peso(min_vert, adjacente)
                if peso + mCaminho[min_vert] < mCaminho[adjacente]:
                    mCaminho[adjacente] = peso + mCaminho[min_vert]
                    antecessor[adjacente] = min_vert
            notVisitados.remove(min_vert)
        vFinal = cFim
        while vFinal != cInicio:
            try:
                caminho.insert(0, self.legenda[vFinal][0])
                vFinal = antecessor[vFinal]

            except KeyError:
                print("Não há caminho disponível")
                break
        caminho.insert(0, self.legenda[cInicio][0])
        if mCaminho[cFim] != nInf:
            print("A MELHOR ROTA PARA O SEU DESTINO TEM -> {}".format(mCaminho[cFim]))


caminho, numVert, dic_local = carregarCaminhos()
graph = Grafo(numVert, dic_local, ponderado = True)
insert_caminhos(caminho)
exec = True
while exec:
    ans1 = input("Digite o nome da cidade de origem: ")
    ans2 = input("Digite o nome da cidade de destino: ")
    ans1 = ans1.upper()
    ans2 = ans2.upper()
    fInput = graph.dijkstra(ans1, ans2)
    graffo = graph.imprimir_grafo()
    op = input("Deseja realizar outra consulta? 1 - sim, 2 - não \n")
    if op == "2":
        exec = False

