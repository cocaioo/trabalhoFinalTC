import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from afn import Estado
from conversor import ConversorERparaAFN
from reconhecedor import ReconhecedorAFN
from visualizador import VisualizadorAFN


class InterfaceAFN:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor ER → AFN-ε - Teoria da Computação")
        self.root.geometry("1400x900")

        self.afn = None
        self.reconhecedor = None

        self._criar_interface()

    def _criar_interface(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        frame_er = ttk.LabelFrame(main_frame, text="1. Expressão Regular", padding="10")
        frame_er.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame_er, text="Notação: ab (concat), a|b (união), a* (Kleene), (a|b)* (parênteses)").grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=5
        )

        ttk.Label(frame_er, text="ER:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.entry_er = ttk.Entry(frame_er, width=50, font=('Courier', 12))
        self.entry_er.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)

        self.btn_converter = ttk.Button(frame_er, text="Converter para AFN-ε", command=self._converter)
        self.btn_converter.grid(row=1, column=2, padx=5)

        frame_er.columnconfigure(1, weight=1)

        frame_visual = ttk.LabelFrame(main_frame, text="2. Visualização do AFN-ε", padding="10")
        frame_visual.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        frame_visual.rowconfigure(0, weight=1)
        frame_visual.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(frame_visual)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.frame_grafico = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_grafico, text="Visualização Gráfica")

        frame_texto = ttk.Frame(self.notebook)
        self.notebook.add(frame_texto, text="Estrutura Textual")

        self.text_estrutura = scrolledtext.ScrolledText(
            frame_texto, width=80, height=20, font=('Courier', 10)
        )
        self.text_estrutura.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        frame_reconhecimento = ttk.LabelFrame(main_frame, text="3. Reconhecimento de Cadeias", padding="10")
        frame_reconhecimento.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        frame_reconhecimento.columnconfigure(1, weight=1)
        frame_reconhecimento.rowconfigure(2, weight=1)

        ttk.Label(frame_reconhecimento, text="Cadeia:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.entry_cadeia = ttk.Entry(frame_reconhecimento, width=40, font=('Courier', 12))
        self.entry_cadeia.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.entry_cadeia.bind('<Return>', lambda e: self._reconhecer())

        self.btn_reconhecer = ttk.Button(
            frame_reconhecimento, text="Reconhecer", command=self._reconhecer, state='disabled'
        )
        self.btn_reconhecer.grid(row=0, column=2, padx=5)

        ttk.Label(frame_reconhecimento, text="Resultado:").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        self.text_resultado = scrolledtext.ScrolledText(
            frame_reconhecimento, width=80, height=12, font=('Courier', 10)
        )
        self.text_resultado.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        frame_rodape = ttk.Frame(main_frame)
        frame_rodape.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(
            frame_rodape,
            text="Trabalho Final - Teoria da Computação | UFPI | Prof. Carlos André Batista de Carvalho",
            font=('Arial', 9, 'italic')
        ).pack()

    def _converter(self):
        er = self.entry_er.get().strip()

        if not er:
            messagebox.showwarning("Aviso", "Digite uma expressão regular!")
            return

        try:
            conversor = ConversorERparaAFN(er)
            self.afn = conversor.converter()
            self.reconhecedor = ReconhecedorAFN(self.afn)

            self._atualizar_visualizacao_grafica()

            self.text_estrutura.delete(1.0, tk.END)
            self.text_estrutura.insert(1.0, self.afn.exibir_texto())

            self.btn_reconhecer.config(state='normal')

            self.text_resultado.delete(1.0, tk.END)

            messagebox.showinfo("Sucesso", f"AFN-ε gerado com sucesso!\n\nTotal de estados: {len(self.afn.obter_todos_estados())}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converter:\n{str(e)}")

    def _atualizar_visualizacao_grafica(self):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        visualizador = VisualizadorAFN(self.afn)
        fig = visualizador.visualizar(f"AFN-ε para: {self.entry_er.get()}")

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        plt.close(fig)

    def _reconhecer(self):
        if not self.afn:
            messagebox.showwarning("Aviso", "Primeiro converta uma expressão regular!")
            return

        cadeia = self.entry_cadeia.get()

        try:
            aceita, motivo = self.reconhecedor.reconhecer(cadeia)

            resultado = []
            resultado.append("="*60)
            resultado.append(f"RECONHECIMENTO DA CADEIA: '{cadeia}'")
            resultado.append("="*60)
            resultado.append(f"\nExpressão Regular: {self.entry_er.get()}")
            resultado.append(f"Cadeia: '{cadeia}' (comprimento: {len(cadeia)})")
            resultado.append("\n" + "-"*60)
            resultado.append("PROCESSAMENTO:")
            resultado.append("-"*60)
            resultado.append(self.reconhecedor.obter_historico_texto())
            resultado.append("\n" + "="*60)

            if aceita:
                resultado.append("✓ RESULTADO: ACEITA")
                resultado.append(f"Motivo: {motivo}")
            else:
                resultado.append("✗ RESULTADO: REJEITADA")
                resultado.append(f"Motivo: {motivo}")

            resultado.append("="*60)

            self.text_resultado.delete(1.0, tk.END)
            self.text_resultado.insert(1.0, "\n".join(resultado))

            if aceita:
                self.text_resultado.tag_add("aceita", "end-3l", "end-2l")
                self.text_resultado.tag_config("aceita", foreground="green", font=('Courier', 10, 'bold'))
            else:
                self.text_resultado.tag_add("rejeita", "end-3l", "end-2l")
                self.text_resultado.tag_config("rejeita", foreground="red", font=('Courier', 10, 'bold'))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao reconhecer:\n{str(e)}")


def main():
    root = tk.Tk()
    app = InterfaceAFN(root)
    root.mainloop()


if __name__ == "__main__":
    main()