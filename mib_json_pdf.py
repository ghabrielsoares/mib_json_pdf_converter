import os
import json
from tkinter import Tk, filedialog, simpledialog
from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler
from fpdf import FPDF

# Dicionário para armazenar as MIBs compiladas
compiled_mibs = {}

# Função de callback que salva cada MIB compilada no dicionário
def save_mib_to_dict(mibName, jsonDoc, cbCtx):
    if jsonDoc:
        print(f"MIB {mibName} foi processada com sucesso.")
        compiled_mibs[mibName] = json.loads(jsonDoc)
    else:
        print(f"Falha ao processar a MIB: {mibName}")

# Função para abrir janela de seleção de arquivos
def select_files(file_type, title, extensions):
    root = Tk()
    root.withdraw()
    root.title(title)
    file_paths = filedialog.askopenfilenames(
        title=title,
        filetypes=[(file_type, extensions)]
    )
    return file_paths

# Função para solicitar o nome do arquivo de saída
def get_output_filename(prompt):
    root = Tk()
    root.withdraw()
    root.title(prompt)
    file_name = simpledialog.askstring("Nome do Arquivo", f"{prompt} (sem extensão):")
    return file_name

# Função para compilar as MIBs selecionadas
def compile_mibs():
    # Seleciona os arquivos MIB
    selected_files = select_files("Arquivos MIB", "Selecione os arquivos MIB", "*.mib")
    if not selected_files:
        print("Nenhum arquivo foi selecionado. O programa será encerrado.")
        return None

    # Nome do arquivo de saída JSON
    output_file_name = get_output_filename("Digite o nome do arquivo JSON")
    if not output_file_name:
        print("Nenhum nome foi fornecido. O programa será encerrado.")
        return None
    output_file = f"{output_file_name}.json"

    # Configuração do compilador de MIBs
    mibCompiler = MibCompiler(SmiStarParser(), JsonCodeGen(), CallbackWriter(save_mib_to_dict))
    mibCompiler.add_sources(*[FileReader(os.path.dirname(file)) for file in selected_files])
    http_base_url = "https://mibs.pysnmp.com/asn1/@mib@"
    mibCompiler.add_sources(HttpReader(http_base_url))
    mibCompiler.add_searchers(StubSearcher(*JsonCodeGen.baseMibs))

    # Compila as MIBs
    inputMibs = [os.path.splitext(os.path.basename(file))[0] for file in selected_files]
    results = mibCompiler.compile(*inputMibs)

    for mib, status in results.items():
        print(f"MIB: {mib}, Status: {status}")

    # Salva as MIBs compiladas em um arquivo JSON
    if compiled_mibs:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(compiled_mibs, f, indent=4, ensure_ascii=False)
        print(f"MIBs compiladas salvas em: {output_file}")
        return output_file
    else:
        print("Nenhuma MIB foi compilada com sucesso.")
        return None

# Função para gerar um PDF a partir de um arquivo JSON
def generate_pdf_from_json(json_file):
    if not json_file:
        return

    # Nome do arquivo de saída PDF
    output_file_name = get_output_filename("Digite o nome do arquivo PDF")
    if not output_file_name:
        print("Nenhum nome foi fornecido para o arquivo de saída.")
        return
    output_pdf = f"{output_file_name}.pdf"

    # Carrega os dados do JSON
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Configura o PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adiciona os dados JSON no PDF
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    pdf.multi_cell(0, 10, json_str)

    # Salva o PDF
    pdf.output(output_pdf)
    print(f"PDF gerado com sucesso: {output_pdf}")

# Programa principal
if __name__ == "__main__":
    json_file = compile_mibs()
    if json_file:
        generate_pdf_from_json(json_file)
