from collections import deque
from datetime import datetime, timedelta

class Livro:
    def __init__(self,titulo, autor, categoria, isbn):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.isbn = isbn
        self.emprestado = False


    def __str__(self):
        return f"Título: {self.titulo} | Autor: {self.autor} | Categoria: {self.categoria} | ISBN: {self.isbn}\n "


class NoAVL:
    def __init__(self, livro):
        self.livro = livro
        self.esquerda = None
        self.direita = None
        self.altura = 1

class Emprestimo:
    def __init__(self,livro,dataEmp,dataDev):
        self.livro = livro
        self.dataDev = dataDev
        self.dataEmp = dataEmp

class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.historicoEmpresitmo = deque()

    def adicionarEmprestimo(self, emprestimo):
        self.historicoEmpresitmo.append(emprestimo)

    def desfazerEmprestimo(self):
        if self.historicoEmpresitmo:
            return self.historicoEmpresitmo.pop()
        return None
class GestaoBiblioteca:
    def __init__(self):
        self.raizTitulo = None
        self.raizAutor = None
        self.raizCategoria = None
        self.isbns = set()
        self.usuarios = {}
        self.registro = []

    def _altura(self, no):
        if not no:
            return 0
        return no.altura

    def _fatorBalanceamento(self, no):
        if not no:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)

    def _rotacaoDireita(self, y):
        x = y.esquerda
        T2 = x.direita
        x.direita = y
        y.esquerda = T2

        y.altura = max(self._altura(y.esquerda), self._altura(y.direita)) + 1
        x.altura = max(self._altura(x.esquerda), self._altura(x.direita)) + 1
        return x

    def _rotacaoEsquerda(self, x):
        y = x.direita
        T2 = y.esquerda
        y.esquerda = x
        x.direita = T2

        x.altura = max(self._altura(x.esquerda), self._altura(x.direita)) + 1
        y.altura = max(self._altura(y.esquerda), self._altura(y.direita)) + 1
        return y

    def _balancear_no(self, no, livro, criterio):
        balanceamento = self._fatorBalanceamento(no)

        if balanceamento > 1 and getattr(livro, criterio) < getattr(no.esquerda.livro, criterio):
            return self._rotacaoDireita(no)

        if balanceamento < -1 and getattr(livro, criterio) > getattr(no.direita.livro, criterio):
            return self._rotacaoEsquerda(no)

        if balanceamento > 1 and getattr(livro, criterio) > getattr(no.esquerda.livro, criterio):
            no.esquerda = self._rotacaoEsquerda(no.esquerda)
            return self._rotacaoDireita(no)

        if balanceamento < -1 and getattr(livro, criterio) < getattr(no.direita.livro, criterio):
            no.direita = self._rotacaoDireita(no.direita)
            return self._rotacaoEsquerda(no)

        return no

    def adicionarLivro(self):
        titulo = input("Digite o título do livro: ")
        while not titulo.strip():
            print("O título não pode ficar em branco! Tente novamente.")
            titulo = input("Digite o título do livro: ")

        autor = input("Digite o autor do livro: ")
        while not autor.strip():
            print("O autor não pode ficar em branco! Tente novamente.")
            autor = input("Digite o autor do livro: ")

        categoria = input("Digite a categoria do livro: ")
        while not categoria.strip():
            print("A categoria não pode ficar em branco! Tente novamente.")
            categoria = input("Digite a categoria do livro: ")

        isbn = input("Digite o ISBN do livro: ")
        while not isbn.strip():
            print("O ISBN não pode ficar em branco! Tente novamente.")
            isbn = input("Digite o ISBN do livro: ")

        if isbn in self.isbns:
            print("Já existe um livro cadastrado com este ISBN. LIVRO NÃO ADICIONADO")
            return

        print("Livro adicionado com sucesso!")
        novoLivro = Livro(titulo, autor, categoria, isbn)
        self.isbns.add(isbn)
        self.raizTitulo = self._inserir(self.raizTitulo, novoLivro, "titulo")
        self.raizAutor = self._inserir(self.raizAutor, novoLivro, "autor")
        self.raizCategoria = self._inserir(self.raizCategoria, novoLivro, "categoria")
    def _inserir(self, no, livro, criterio):
        if no is None:
            return NoAVL(livro)

        if getattr(livro, criterio) < getattr(no.livro, criterio):
            no.esquerda = self._inserir(no.esquerda, livro, criterio)
        else:
            no.direita = self._inserir(no.direita, livro, criterio)

        no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))

        return self._balancear_no(no, livro, criterio)

    def _listarLivros(self):
        livros = []
        self._listarLivrosTitulo(self.raizTitulo, livros)
        return livros

    def listarLivrosDisponiveis(self):
        print("Livros disponíveis para empréstimo:")
        for livro in self._listarLivros():
            if not livro.emprestado:
                print(f"{livro.titulo} - {livro.isbn}")
    def _listarLivrosTitulo(self, no, livros):
        if no:
            self._listarLivrosTitulo(no.esquerda, livros)
            livros.append(no.livro)
            self._listarLivrosTitulo(no.direita, livros)

    def buscarLivro(self):
        print("Escolha a opção de busca!")
        print("1.Título")
        print("2.Autor")
        print("3.Categoria")
        print("4.Os 3 critérios juntos")
        opcao = input("Digite sua opção: ")
        busca = input("Digite o que deseja buscar: ")

        if opcao == '1':
            print("Escolha o tipo de busca: ")
            print("1.Busca binária")
            print("2.Busca sequencial")
            tipo = input()
            if tipo == '1':
                self._buscarPorTituloBinaria(busca)
            elif tipo == '2':
                self._buscarPorTituloSequencial(busca)
            else:
                print("Opção inexistente! Tente novamente!")
        elif opcao == '2':
            print("Escolha o tipo de busca: ")
            print("1.Busca binária")
            print("2.Busca sequencial")
            tipo = input()
            if tipo == '1':
                self._buscarPorAutorBinaria(busca)
            elif tipo == '2':
                self._buscarPorAutorSequencial(busca)
            else:
                print("Opção inexistente! Tente novamente!")
        elif opcao == '3':
            print("Escolha o tipo de busca: ")
            print("1.Busca binária")
            print("2.Busca sequencial")
            tipo = input()
            if tipo == '1':
                self._buscarPorCategoriaBinaria(busca)
            elif tipo == '2':
                self._buscarPorCategoriaSequencial(busca)
            else:
                print("Opção inexistente! Tente novamente!")

        elif opcao == '4':
            self._buscarPorMultiplosCriterios()
        else:
            print("OPÇÃO INVÁLIDA. TENTE NOVAMENTE!")

    def _buscarPorTituloBinaria(self, titulo):
        livro = self._buscarTituloBinaria(self.raizTitulo, titulo)
        if livro:
            print(livro)
        else:
            print("Nenhum livro encontrado com este título!")

    def _buscarTituloBinaria(self, no, titulo):
        if no is None:
            return None

        if titulo.lower() == no.livro.titulo.lower():
            return no.livro
        elif titulo.lower() < no.livro.titulo.lower():
            return self._buscarTituloBinaria(no.esquerda, titulo)
        else:
            return self._buscarTituloBinaria(no.direita, titulo)

    def _buscarPorTituloSequencial(self, titulo):
        resultados = []
        self._buscarTituloSequencial(self.raizTitulo, titulo, resultados)
        if resultados:
            for livro in resultados:
                print(livro)
        else:
            print("Nenhum livro encontrado com este título!")

    def _buscarTituloSequencial(self, no, titulo, resultados):
        if no is None:
            return

        if no.livro.titulo.lower() == titulo.lower():
            resultados.append(no.livro)
        self._buscarTituloSequencial(no.esquerda, titulo, resultados)
        self._buscarTituloSequencial(no.direita, titulo, resultados)

    def _buscarPorAutorBinaria(self, autor):
        livro = self._buscarAutorBinaria(self.raizAutor, autor)
        if livro:
            print(livro)
        else:
            print("Nenhum livro encontrado com este autor!")

    def _buscarAutorBinaria(self, no, autor):
        if no is None:
            return None
        if autor.lower() < no.livro.autor.lower():
            return self._buscarAutorBinaria(no.esquerda, autor)
        elif autor.lower() > no.livro.autor.lower():
            return self._buscarAutorBinaria(no.direita, autor)
        else:
            return no.livro

    def _buscarPorAutorSequencial(self, autor):
        resultados = []
        self._buscarAutorSequencial(self.raizAutor, autor, resultados)
        if resultados:
            for livro in resultados:
                print(livro)
        else:
            print("Nenhum livro encontrado com este autor!")

    def _buscarAutorSequencial(self, no, autor, resultados):
        if no is None:
            return

        if no.livro.autor.lower() == autor.lower():
            resultados.append(no.livro)

        self._buscarAutorSequencial(no.esquerda, autor, resultados)
        self._buscarAutorSequencial(no.direita, autor, resultados)

    def _buscarPorCategoriaBinaria(self, categoria):
        livro = self._buscarCategoriaBinaria(self.raizCategoria, categoria)
        if livro:
            print(livro)
        else:
            print("Nenhum livro encontrado com esta categoria!")

    def _buscarCategoriaBinaria(self, no, categoria):
        if no is None:
            return None

        if categoria.lower() < no.livro.categoria.lower():
            return self._buscarCategoriaBinaria(no.esquerda, categoria)
        elif categoria.lower() > no.livro.categoria.lower():
            return self._buscarCategoriaBinaria(no.direita, categoria)
        else:
            return no.livro

    def _buscarPorCategoriaSequencial(self, categoria):
        resultados = []
        self._buscarCategoriaSequencial(self.raizCategoria, categoria, resultados)
        if resultados:
            for livro in resultados:
                print(livro)
        else:
            print("Nenhum livro encontrado com esta categoria!")

    def _buscarCategoriaSequencial(self, no, categoria, resultados):
        if no is None:
            return

        if no.livro.categoria.lower() == categoria.lower():
            resultados.append(no.livro)

        self._buscarCategoriaSequencial(no.esquerda, categoria, resultados)
        self._buscarCategoriaSequencial(no.direita, categoria, resultados)

    def _buscarPorMultiplosCriterios(self):
        titulo = input("Digite o título do livro (ou deixe em branco para ignorar): ").strip().lower()
        autor = input("Digite o autor do livro (ou deixe em branco para ignorar): ").strip().lower()
        categoria = input("Digite a categoria do livro (ou deixe em branco para ignorar): ").strip().lower()

        resultados = []
        livros = self._listarLivros()

        for livro in livros:
            corresponde = True

            if titulo and titulo != livro.titulo.lower():
                corresponde = False
            if autor and autor != livro.autor.lower():
                corresponde = False
            if categoria and categoria != livro.categoria.lower():
                corresponde = False

            if corresponde:
                resultados.append(livro)

        if resultados:
            print("\nLivros encontrados:")
            for livro in resultados:
                print(livro)
        else:
            print("Nenhum livro encontrado com os critérios especificados.")

    def EmprestarLivro(self, nomeUsuario, isbn):
        usuario = self.usuarios.get(nomeUsuario)
        if not usuario:
            print("Este usuário não foi encotrado!")
            return

        for livro in self._listarLivros():
            if livro.isbn == isbn:
                if livro.emprestado:
                    print(f"O livro '{livro.titulo}' já está emprestado!")
                    return

                dataEmp = datetime.now()
                dataDev= dataEmp + timedelta(days=14)
                emprestimo = Emprestimo(livro, dataEmp, dataDev)
                usuario.adicionarEmprestimo(emprestimo)
                livro.emprestado = True
                self.registro.append(emprestimo)
                print(
                    f"Livro {livro.titulo} emprestado para {usuario.nome} com sucesso!. Data de devolução: {dataDev.date()}.")
                return

        print("Livro não encontrado no acervo!")

    def devolverLivro(self, nomeUsuario):
        usuario = self.usuarios.get(nomeUsuario)
        if not usuario:
            print("Este usuário não foi encotrado!")
            return

        emprestimo = usuario.desfazerEmprestimo()
        if emprestimo:
            emprestimo.livro.emprestado = False
            print(f"Livro {emprestimo.livro.titulo} devolvido com sucesso.")
            self.registro.append(emprestimo)
        else:
            print("Nenhum empréstimo encontrado para este usuário.")

    def gerenciarEmprestimo(self):
        while True:
            print("\n --GERENCIAMENTO DE EMPRÉSTIMOS--")
            print("1. Emprestar livro")
            print("2. Devolver livro")
            print("3. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                nomeUsuario = input("Digite o nome do usuário: ")
                self.listarLivrosDisponiveis()
                isbn = input("Digite o ISBN do livro que deseja emprestar: ")
                self.EmprestarLivro(nomeUsuario, isbn)
            elif opcao == '2':
                nomeUsuario = input("Digite o nome do usuário: ")
                self.devolverLivro(nomeUsuario)
            elif opcao == '3':
                break
            else:
                print("Opção inválida! Tente novamente.")

    def gerarRelatorio(self):
        print("--RELATÓRIO DE EMPRÉSTIMOS E DEVOLUÇÕES DOS ÚLTIMOS 7 DIAS--")
        if not self.registro:
            print("NENHUMA OPERAÇÃO REALIZADA!")
            return

        dataAtual = datetime.now()
        dataInicio = dataAtual - timedelta(days=7)
        realizada = False
        for registro in self.registro:
            if registro.dataEmp >= dataInicio:
                print(f"LIVRO: {registro.livro.titulo} | EMPRESTADO EM: {registro.dataEmp.strftime('%d/%m/%Y')} | DEVOLUÇÃO PREVISTA/FEITA: {registro.dataDev.strftime('%d/%m/%Y')}")
                realizada = True

        if not realizada:
            print("NENHUMA OPERAÇÃO REALIZADA!")
    def quickSort(self, livros, criterio):
        if len(livros) <= 1:
            return livros
        else:
            pivot = livros[0]
            menores = []
            maiores = []
            iguais = []

            keyPivot = getattr(pivot, criterio).lower()

            for livro in livros:
                keyLivro = getattr(livro, criterio).lower()
                if keyLivro < keyPivot:
                    menores.append(livro)
                elif keyLivro > keyPivot:
                    maiores.append(livro)
                else:
                    iguais.append(livro)


            return self.quickSort(menores, criterio) + iguais + self.quickSort(maiores, criterio)

    def listarLivrosOrdenados(self):
        print("Escolha como deseja ordenar os livros:")
        print("1. Título")
        print("2. Autor")
        print("3. Categoria")
        opcao = input("Digite a opção desejada: ")

        if opcao == '1':
            criterio = 'titulo'
        elif opcao == '2':
            criterio = 'autor'
        elif opcao == '3':
            criterio = 'categoria'
        else:
            print("Opção inválida!")
            return

        # Listar todos os livros cadastrados e ordenar conforme critério escolhido
        livros = self._listarLivros()
        livros_ordenados = self.quickSort(livros, criterio)

        print("\nLivros Ordenados por", criterio.capitalize() + ":\n")
        if not livros:
            print("NENHUM LIVRO CADASTRADO NO MOMENTO!")
            return

        for livro in livros_ordenados:
            print(livro)

    def adicionarUsuario(self, nome):
        if nome not in self.usuarios:
            self.usuarios[nome] = Usuario(nome)
            print(f"Usuário {nome} cadastrado com sucesso!")
        else:
            print("Usuário já cadastrado!")