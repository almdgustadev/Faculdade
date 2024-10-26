from Livro import GestaoBiblioteca
def menu():
    print("\n ---Bem vindo ao Sistema de Gestão!--- ")
    print("1. Adicionar livro")
    print("2. Buscar livro")
    print("3. Gerenciar empréstimo")
    print("4. Gerar relatórios")
    print("5. Listar livros ordenados")
    print("6. Adicionar Usuário")
    print("7. Sair")



def main():
    biblioteca = GestaoBiblioteca()

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            biblioteca.adicionarLivro()
        elif opcao == '2':
            biblioteca.buscarLivro()
        elif opcao == '3':
            biblioteca.gerenciarEmprestimo()
        elif opcao == '4':
           biblioteca.gerarRelatorio()
        elif opcao == '5':
            biblioteca.listarLivrosOrdenados()
        elif opcao == '6':
            nomeUsuario = input("Digite o nome do usuário: ")
            biblioteca.adicionarUsuario(nomeUsuario)
        elif opcao == '7':
            print("Encerrando...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()