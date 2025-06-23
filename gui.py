import tkinter as tk
from tkinter import ttk, messagebox, Listbox, Text, END, ACTIVE

import data_manager as dm

FONT_LABEL = ('Helvetica', 10)
FONT_TITULO = ('Helvetica', 14, 'bold')
GENEROS_LISTA = ('Aventura', 'Auto Ajuda', 'Biografia', 'Culinário', 'Comédia', 'Fanfic', 'Ficção', 'Ficção Científica', 'Fantasia', 'Histórico', 'HQ', 'Infantil', 'Mangá', 'Mistério', 'Poesia', 'Romance', 'Suspense', 'Terror', 'Religioso', 'Outro')
NOTA_LISTA = ('0', '1', '2', '3', '4', '5')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Bookcase")
        self.geometry("500x500")
        self.resizable(False, False)
        try:
            self.iconbitmap('assets/pilha-de-livros.ico')
        except tk.TclError:
            print("Ícone 'pilha-de-livros.ico' não encontrado.")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (FramePrincipal, FrameCadastro, FrameLista):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("FramePrincipal")

    def mostrar_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "FrameLista":
            frame.atualizar_lista_livros()
        frame.tkraise()

class FramePrincipal(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=(60, 40))
        self.controller = controller

        ttk.Label(self, text="The Bookcase", font=('Helvetica', 30, 'bold')).pack(pady=20)
        ttk.Label(self, text="Organize, salve e avalie seus livros!").pack(pady=10)
        
        ttk.Button(self, text="Cadastrar Livro", command=lambda: controller.mostrar_frame("FrameCadastro"), padding=10).pack(pady=10, fill='x')
        ttk.Button(self, text="Listar Livros", command=lambda: controller.mostrar_frame("FrameLista"), padding=10).pack(pady=10, fill='x')
        ttk.Button(self, text="Sair", command=self.controller.destroy, padding=10).pack(pady=10, fill='x')

class FrameCadastro(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=(20, 10))
        self.controller = controller
        
        ttk.Label(self, text="Cadastrar Novo Livro", font=FONT_TITULO).grid(row=0, column=0, columnspan=2, pady=10, sticky="W")

        self.nome_var = tk.StringVar()
        ttk.Label(self, text="Nome:", font=FONT_LABEL).grid(row=1, column=0, sticky="W", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.nome_var, width=50).grid(row=1, column=1, sticky="EW", padx=5, pady=5)

        self.genero_var = tk.StringVar()
        ttk.Label(self, text="Gênero:", font=FONT_LABEL).grid(row=2, column=0, sticky="W", padx=5, pady=5)
        genero_cb = ttk.Combobox(self, textvariable=self.genero_var, values=GENEROS_LISTA, state='readonly', width=20)
        genero_cb.grid(row=2, column=1, sticky="W", padx=5, pady=5)
        genero_cb.set("Aventura")

        self.autor_var = tk.StringVar()
        ttk.Label(self, text="Autor:", font=FONT_LABEL).grid(row=3, column=0, sticky="W", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.autor_var, width=50).grid(row=3, column=1, sticky="EW", padx=5, pady=5)

        self.avaliacao_var = tk.StringVar()
        ttk.Label(self, text="Avaliação:", font=FONT_LABEL).grid(row=4, column=0, sticky="W", padx=5, pady=5)
        avaliacao_cb = ttk.Combobox(self, textvariable=self.avaliacao_var, values=NOTA_LISTA, state='readonly', width=5)
        avaliacao_cb.grid(row=4, column=1, sticky="W", padx=5, pady=5)
        avaliacao_cb.set("0")
        
        ttk.Label(self, text="Descrição:", font=FONT_LABEL).grid(row=5, column=0, sticky="NW", padx=5, pady=5)
        self.desc_text = Text(self, width=40, height=10, font=FONT_LABEL)
        self.desc_text.grid(row=5, column=1, sticky="EW", padx=5, pady=5)
        
        botoes_frame = ttk.Frame(self)
        botoes_frame.grid(row=6, column=0, columnspan=2, pady=20)
        ttk.Button(botoes_frame, text="Salvar", command=self.salvar_livro).pack(side="left", padx=10)
        ttk.Button(botoes_frame, text="Voltar", command=lambda: controller.mostrar_frame("FramePrincipal")).pack(side="right", padx=10)

        self.grid_columnconfigure(1, weight=1)

    def salvar_livro(self):
        nome = self.nome_var.get().strip()
        autor = self.autor_var.get().strip()
        genero = self.genero_var.get()
        avaliacao = self.avaliacao_var.get()
        descricao = self.desc_text.get("1.0", END).strip()

        if not nome or not autor:
            messagebox.showerror("Erro", "Os campos 'Nome' e 'Autor' são obrigatórios.")
            return

        if dm.adicionar_livro(nome, genero, autor, avaliacao, descricao):
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
            self.limpar_campos()
            self.controller.mostrar_frame("FrameLista")
        else:
            messagebox.showerror("Erro", f"O livro '{nome}' já está cadastrado.")

    def limpar_campos(self):
        self.nome_var.set("")
        self.autor_var.set("")
        self.desc_text.delete("1.0", END)

class FrameLista(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=(10, 10))
        self.controller = controller

        top_frame = ttk.Frame(self)
        top_frame.pack(fill='x', pady=5)

        self.pesquisa_var = tk.StringVar()
        ttk.Label(top_frame, text="Pesquisar:").pack(side='left', padx=(0, 5))
        pesquisa_entry = ttk.Entry(top_frame, textvariable=self.pesquisa_var, width=30)
        pesquisa_entry.pack(side='left', fill='x', expand=True)
        pesquisa_entry.bind('<KeyRelease>', self.buscar_livro)

        self.genero_filtro_var = tk.StringVar()
        genero_cb = ttk.Combobox(top_frame, textvariable=self.genero_filtro_var, values=['Todos'] + list(GENEROS_LISTA), state='readonly', width=15)
        genero_cb.pack(side='left', padx=5)
        genero_cb.set("Todos")
        genero_cb.bind('<<ComboboxSelected>>', self.filtrar_por_genero)

        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True, pady=5)
        
        self.caixa_livros = Listbox(list_frame, height=15, width=60)
        self.caixa_livros.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.caixa_livros.yview)
        scrollbar.pack(side='right', fill='y')
        self.caixa_livros.config(yscrollcommand=scrollbar.set)
        
        botoes_frame = ttk.Frame(self)
        botoes_frame.pack(fill='x', pady=10)

        ttk.Button(botoes_frame, text="Mostrar/Editar", command=self.mostrar_livro_selecionado).pack(side='left', expand=True, fill='x', padx=2)
        ttk.Button(botoes_frame, text="Remover Livro", command=self.remover_livro_selecionado).pack(side='left', expand=True, fill='x', padx=2)
        ttk.Button(botoes_frame, text="Limpar Estante", command=self.limpar_toda_estante).pack(side='left', expand=True, fill='x', padx=2)
        ttk.Button(botoes_frame, text="Voltar ao Menu", command=lambda: controller.mostrar_frame("FramePrincipal")).pack(side='left', expand=True, fill='x', padx=2)

    def atualizar_lista_livros(self, lista_nomes=None):
        livros = lista_nomes if lista_nomes is not None else dm.get_todos_os_livros()
        
        self.caixa_livros.delete(0, END)
        for nome in livros:
            self.caixa_livros.insert(END, nome)

    def buscar_livro(self, event=None):
        termo_busca = self.pesquisa_var.get().strip().upper()
        todos_os_livros = dm.get_todos_os_livros()
        
        if not termo_busca:
            self.atualizar_lista_livros(todos_os_livros)
            return
        
        resultados = [nome for nome in todos_os_livros if termo_busca in nome.upper()]
        self.atualizar_lista_livros(resultados)

    def filtrar_por_genero(self, event=None):
        genero_selecionado = self.genero_filtro_var.get()
        if genero_selecionado == "Todos":
            self.atualizar_lista_livros()
            return

        todos_os_livros = dm.get_todos_os_livros()
        resultados = []
        for nome in todos_os_livros:
            detalhes = dm.get_detalhes_livro(nome)
            if detalhes and detalhes[0] == genero_selecionado:
                resultados.append(nome)
        self.atualizar_lista_livros(resultados)

    def _get_livro_selecionado(self):
        indices = self.caixa_livros.curselection()
        if not indices:
            messagebox.showwarning("Atenção", "Por favor, selecione um livro da lista.")
            return None
        return self.caixa_livros.get(indices[0])

    def remover_livro_selecionado(self):
        nome_livro = self._get_livro_selecionado()
        if not nome_livro:
            return

        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o livro '{nome_livro}'?"):
            dm.remover_livro(nome_livro)
            messagebox.showinfo("Sucesso", "Livro removido com sucesso.")
            self.atualizar_lista_livros()

    def mostrar_livro_selecionado(self):
        nome_livro = self._get_livro_selecionado()
        if nome_livro:
            JanelaEditar(parent=self, controller=self.controller, nome_livro=nome_livro)

    def limpar_toda_estante(self):
        if messagebox.askyesno("Confirmar Limpeza", "ATENÇÃO! Isso apagará TODOS os livros cadastrados.\nDeseja continuar?"):
            dm.limpar_estante()
            messagebox.showinfo("Sucesso", "A estante foi limpa.")
            self.atualizar_lista_livros()

class JanelaEditar(tk.Toplevel):
    def __init__(self, parent, controller, nome_livro):
        super().__init__(parent)
        self.controller = controller
        self.nome_antigo = nome_livro

        detalhes = dm.get_detalhes_livro(nome_livro)
        if not detalhes:
            messagebox.showerror("Erro", "Não foi possível carregar os dados do livro.")
            self.destroy()
            return
        
        self.title(f"Editando: {nome_livro}")
        self.geometry("450x400")
        self.resizable(False, False)
        try:
            self.iconbitmap('assets/abra-o-livro.ico')
        except tk.TclError:
            print("Ícone 'abra-o-livro.ico' não encontrado.")
        self.focus()
        self.transient(parent)

       
        frame = ttk.Frame(self, padding=(20, 10))
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Editar Livro", font=FONT_TITULO).grid(row=0, column=0, columnspan=2, pady=10, sticky="W")

        self.nome_var = tk.StringVar(value=nome_livro)
        ttk.Label(frame, text="Nome:", font=FONT_LABEL).grid(row=1, column=0, sticky="W", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.nome_var, width=50).grid(row=1, column=1, sticky="EW", padx=5, pady=5)

        self.genero_var = tk.StringVar(value=detalhes[0])
        ttk.Label(frame, text="Gênero:", font=FONT_LABEL).grid(row=2, column=0, sticky="W", padx=5, pady=5)
        ttk.Combobox(frame, textvariable=self.genero_var, values=GENEROS_LISTA, state='readonly', width=20).grid(row=2, column=1, sticky="W", padx=5, pady=5)

        self.autor_var = tk.StringVar(value=detalhes[1])
        ttk.Label(frame, text="Autor:", font=FONT_LABEL).grid(row=3, column=0, sticky="W", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.autor_var, width=50).grid(row=3, column=1, sticky="EW", padx=5, pady=5)

        self.avaliacao_var = tk.StringVar(value=detalhes[2])
        ttk.Label(frame, text="Avaliação:", font=FONT_LABEL).grid(row=4, column=0, sticky="W", padx=5, pady=5)
        ttk.Combobox(frame, textvariable=self.avaliacao_var, values=NOTA_LISTA, state='readonly', width=5).grid(row=4, column=1, sticky="W", padx=5, pady=5)
        
        ttk.Label(frame, text="Descrição:", font=FONT_LABEL).grid(row=5, column=0, sticky="NW", padx=5, pady=5)
        self.desc_text = Text(frame, width=40, height=8, font=FONT_LABEL)
        self.desc_text.grid(row=5, column=1, sticky="EW", padx=5, pady=5)
        self.desc_text.insert("1.0", detalhes[3])
        
        botoes_frame = ttk.Frame(frame)
        botoes_frame.grid(row=6, column=0, columnspan=2, pady=20)
        ttk.Button(botoes_frame, text="Salvar Alterações", command=self.salvar_edicao).pack(side="left", padx=10)
        ttk.Button(botoes_frame, text="Cancelar", command=self.destroy).pack(side="right", padx=10)

        frame.grid_columnconfigure(1, weight=1)

    def salvar_edicao(self):
        nome_novo = self.nome_var.get().strip()
        autor = self.autor_var.get().strip()
        
        if not nome_novo or not autor:
            messagebox.showerror("Erro", "Os campos 'Nome' e 'Autor' são obrigatórios.", parent=self)
            return

        dm.editar_livro(
            nome_antigo=self.nome_antigo,
            nome_novo=nome_novo,
            genero=self.genero_var.get(),
            autor=autor,
            avaliacao=self.avaliacao_var.get(),
            descricao=self.desc_text.get("1.0", END).strip()
        )
        messagebox.showinfo("Sucesso", "Livro editado com sucesso.", parent=self)
        self.destroy()
        self.controller.frames["FrameLista"].atualizar_lista_livros()