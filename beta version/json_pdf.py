import json
from fpdf import FPDF
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring

# Função para selecionar o arquivo JSON
def selecionar_arquivo():
    Tk().withdraw()  # Oculta a janela principal do Tkinter
    arquivo_selecionado = askopenfilename(
        title="Selecione o arquivo JSON",
        filetypes=[("Arquivos JSON", "*.json")]
    )
    return arquivo_selecionado

# Função para obter o nome do arquivo de saída
def obter_nome_saida():
    Tk().withdraw()  # Oculta a janela principal do Tkinter
    nome_saida = askstring(
        "Nome do Arquivo de Saída",
        "Digite o nome desejado para o arquivo PDF (sem extensão):"
    )
    return nome_saida

# Seleciona o arquivo JSON
json_file = selecionar_arquivo()

# Verifica se o usuário selecionou um arquivo
if not json_file:
    print("Nenhum arquivo foi selecionado.")
else:
    # Obtém o nome do arquivo de saída
    nome_saida = obter_nome_saida()

    if not nome_saida:
        print("Nenhum nome foi fornecido para o arquivo de saída.")
    else:
        output_pdf = f"{nome_saida}.pdf"

        # Carregar o conteúdo do arquivo JSON
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Configura o PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Função para adicionar JSON ao PDF
        def add_json_to_pdf(pdf, json_data):
            # Converte o JSON para string formatada
            json_str = json.dumps(json_data, indent=4, ensure_ascii=False)

            # Adiciona o conteúdo do JSON no PDF
            pdf.multi_cell(0, 10, json_str)

        # Adiciona os dados JSON no PDF
        add_json_to_pdf(pdf, data)

        # Salva o PDF final
        pdf.output(output_pdf)
        print(f"Arquivo PDF gerado com sucesso: {output_pdf}")
