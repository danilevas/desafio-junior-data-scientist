# Caminho do arquivo Markdown
arquivo_md = 'testemd.md'

# Função para adicionar conteúdo ao arquivo Markdown
def adicionar_ao_md(conteudo):
    with open(arquivo_md, 'a', encoding='utf-8') as file:
        file.write(conteudo + '\n')

# Função para limpar o arquivo e começar do zero
def reiniciar_arquivo_md():
    with open(arquivo_md, 'w', encoding='utf-8') as file:
        # Isso limpa o arquivo antes de adicionar qualquer conteúdo novo
        pass

# Zerar o arquivo no início do script
reiniciar_arquivo_md()

# Exemplo de resultados que você quer adicionar
resultado_media_diaria = 9.13  # Suponha que este seja o resultado da média diária de chamados

# Texto em formato Markdown
texto = f"""
# Relatório de Chamados

### Média Diária de Chamados

A média diária de chamados para o subtipo 5071, no intervalo de 2022-01-01 até 2024-12-31, foi de **{resultado_media_diaria}** chamados por dia.

---

"""

# Adicionando ao arquivo .md
adicionar_ao_md(texto)

# Agora, você pode adicionar mais coisas ao longo do seu script
outra_informacao = "Aqui podemos adicionar mais informações de outros cálculos ou resultados!"
adicionar_ao_md(outra_informacao)
