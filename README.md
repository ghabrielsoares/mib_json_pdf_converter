# Ferramenta de Conversão e Geração de Arquivos MIB JSON PDF

## Descrição
Este projeto combina duas funcionalidades principais em uma única ferramenta:
1. **Conversão de arquivos MIB para JSON**: Compila arquivos MIB em um formato JSON utilizável.
2. **Geração de PDFs a partir de arquivos JSON**: Converte os dados JSON gerados em um arquivo PDF formatado.

## Descrição Rápida
Ferramenta para converter arquivos MIB em JSON e gerar PDFs a partir do JSON resultante.

## Dependências
Para executar este código, é necessário instalar as seguintes bibliotecas Python:

- `pysmi`
- `fpdf`
- `tkinter` (disponível por padrão na maioria das instalações do Python)

### Instalando as Dependências
Execute o seguinte comando no terminal para instalar as bibliotecas necessárias:
```bash
pip install pysmi fpdf
```

## Como Usar

### Passo 1: Iniciar o Programa
Salve o código em um arquivo Python, `mib_json_pdf.py`, e execute-o:
```bash
python mib_json_pdf.py
```

### Passo 2: Conversão de MIB para JSON
1. Uma janela será aberta para selecionar os arquivos MIB.
2. Escolha os arquivos desejados e confirme.
3. Em seguida, forneça o nome para o arquivo JSON de saída (sem extensão).
4. O programa compilará os arquivos MIB selecionados e salvará os resultados em um arquivo JSON.

### Passo 3: Geração de PDF
1. Caso a compilação dos arquivos MIB tenha sido bem-sucedida, o programa solicitará um nome para o arquivo PDF de saída.
2. O arquivo JSON gerado será convertido para um arquivo PDF formatado.

### Passo 4: Resultado Final
Os arquivos gerados serão salvos no mesmo diretório onde o script foi executado:
- Arquivo JSON contendo as MIBs compiladas.
- Arquivo PDF com os dados do JSON formatados.

## Estrutura do Código
O programa é dividido em funções principais:

1. **`compile_mibs`**:
   - Seleciona arquivos MIB.
   - Compila as MIBs em JSON.
   - Salva o JSON em um arquivo.

2. **`generate_pdf_from_json`**:
   - Seleciona um arquivo JSON.
   - Converte os dados JSON em um PDF formatado.

3. **Programa Principal**:
   - Chama as funções na ordem correta para realizar as duas tarefas principais.

## Observações
- Certifique-se de que os arquivos MIB estejam no formato correto antes de tentar compilar.
- O arquivo PDF gerado conterá os dados JSON formatados de maneira legível.

## Exemplo de Uso

1. **Entrada**: Arquivo MIB `example.mib`.
2. **Processo**:
   - Selecione o arquivo MIB.
   - Nomeie o arquivo JSON de saída como `output.json`.
   - Nomeie o arquivo PDF de saída como `output.pdf`.
3. **Saída**:
   - `output.json`: JSON gerado a partir do MIB.
   - `output.pdf`: PDF com o conteúdo do JSON formatado.

Agora você pode usar o script para facilitar o trabalho com MIBs e gerar relatórios formatados de forma rápida!

