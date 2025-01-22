from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler
import os
from tkinter import Tk, filedialog, simpledialog
import json  # Importa biblioteca para manipulação de JSON

# Dicionário para armazenar todas as MIBs compiladas.
compiled_mibs = {}

# Função de callback que salva cada MIB compilada no dicionário.
def printOut(mibName, jsonDoc, cbCtx):
    if jsonDoc:
        print(f"MIB {mibName} foi processada com sucesso.")
        compiled_mibs[mibName] = json.loads(jsonDoc)
    else:
        print(f"Falha ao processar a MIB: {mibName}")

# Função para abrir a janela de seleção de arquivos e retornar os MIBs escolhidos.
def select_files():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter.
    root.title("Selecione os arquivos MIB")
    file_paths = filedialog.askopenfilenames(
        title="Selecione os arquivos MIB para converter",
        filetypes=[("Arquivos MIB", "*.mib"), ("Todos os Arquivos", "*.*")]
    )
    return file_paths

# Função para solicitar o nome do arquivo de saída.
def get_output_filename():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter.
    root.title("Nome do Arquivo de Saída")
    file_name = simpledialog.askstring(
        "Nome do Arquivo", "Digite o nome do arquivo de saída (sem extensão):"
    )
    return file_name

# Seleciona os arquivos que o usuário deseja converter.
selected_files = select_files()
if not selected_files:
    print("Nenhum arquivo foi selecionado. O programa será encerrado.")
    exit()

# Solicita o nome do arquivo de saída.
output_file_name = get_output_filename()
if not output_file_name:
    print("Nenhum nome de arquivo foi fornecido. O programa será encerrado.")
    exit()

output_file = f"{output_file_name}.json"

# Inicializa a infraestrutura do compilador de MIBs.
mibCompiler = MibCompiler(SmiStarParser(), JsonCodeGen(), CallbackWriter(printOut))

# Adiciona os diretórios locais como fontes de MIBs.
mibCompiler.add_sources(*[FileReader(os.path.dirname(file)) for file in selected_files])

# Corrige a criação de HttpReader: aceita apenas a URL base como argumento.
http_base_url = "https://mibs.pysnmp.com/asn1/@mib@"
mibCompiler.add_sources(HttpReader(http_base_url))

# Configura o compilador para nunca recompilar MIBs que contêm MACROs já baseadas no padrão.
mibCompiler.add_searchers(StubSearcher(*JsonCodeGen.baseMibs))

# Extrai apenas os nomes dos arquivos selecionados para compilação (sem extensões).
inputMibs = [os.path.splitext(os.path.basename(file))[0] for file in selected_files]

# Executa a compilação recursiva das MIBs selecionadas.
results = mibCompiler.compile(*inputMibs)

# Depura os resultados da compilação.
for mib, status in results.items():
    print(f"MIB: {mib}, Status: {status}")

# Verifica se alguma MIB foi compilada com sucesso.
if compiled_mibs:
    # Salva todas as MIBs compiladas em um único arquivo JSON.
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(compiled_mibs, f, indent=4, ensure_ascii=False)
    print(f"Todas as MIBs compiladas foram salvas no arquivo: {output_file}")
else:
    print("Nenhuma MIB foi compilada com sucesso. Verifique os arquivos selecionados.")
