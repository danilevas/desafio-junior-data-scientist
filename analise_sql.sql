-- Localização de chamados do 1746
-- Questão 1. Quantos chamados foram abertos no dia 01/04/2023?

-- Checando se há algum id_chamado nulo (109,64 MB)
SELECT COUNT(*) AS total_nulls 
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE id_chamado IS NULL;
-- Aqui vemos que há 199 células em que id_chamado é nulo, logo quando fizer meu COUNT, é bom fazer COUNT(id_chamado) ao invés de COUNT(*),
-- para já desconsiderar as linhas com id_chamado nulo

-- Como o campo data_inicio está com data e hora e eu quero só a data, eu vou usar a função DATE() para extrair só o necessário e agrupar corretamente
-- Agrupando por data_inicio (só pela data, sem horário) e contando quantos id_chamados válidos (não nulos) existem para cada data,
-- filtrando só para a data que queremos (01/04/2023) (202,05 MB)
SELECT DATE(data_inicio) AS data, COUNT(id_chamado) AS chamados_por_data 
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01'
GROUP BY data;
-- Resposta Questão 1: foram abertos 1903 chamados no dia 01/04/2023.

-- Questão 2. Qual o tipo de chamado que teve mais teve chamados abertos no dia 01/04/2023?

-- Agrupando pelo tipo de chamado, e contando quantos id_chamados válidos (não nulos) existem para cada tipo,
-- filtrando só para a data que queremos (01/04/2023) (435,05 MB)
SELECT tipo, COUNT(id_chamado) AS chamados_totais
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01'
GROUP BY tipo
ORDER BY chamados_totais DESC;
-- Resposta Questão 2: o tipo de chamado que teve mais teve chamados abertos no dia 01/04/2023 foi "Estacionamento irregular", com 373 chamados abertos.

-- [EXTRA] 10 dias com mais chamados (202,05 MB)
SELECT DATE(data_inicio) AS data, COUNT(id_chamado) AS chamados_por_data 
FROM `datario.adm_central_atendimento_1746.chamado`
GROUP BY data
ORDER BY chamados_por_data DESC
LIMIT 10;

-- Questão 3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?

-- Aqui vemos quais id_bairros tiveram mais chamados abertos no dia 01/04/2023 (250,04 MB)
SELECT id_bairro, COUNT(id_chamado) AS chamados_totais
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01'
GROUP BY id_bairro
ORDER BY chamados_totais DESC;
-- Percebe-se que o id_bairro "NULL" foi o que teve mais chamados abertos nesse dia

-- Agora vamos fazer o join com a tabela "datario.dados_mestres.bairro" para cruzarmos as informações e pegarmos os nomes dos bairros pelo id_bairro (250,04 MB)
SELECT c.id_bairro, b.nome, COUNT(c.id_chamado) AS chamados_totais
FROM `datario.adm_central_atendimento_1746.chamado` c
JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01'
GROUP BY c.id_bairro, b.nome
ORDER BY chamados_totais DESC;
-- Resposta Questão 3: Os 3 bairros que mais tiveram chamados abertos nesse dia foram:
-- Campo Grande (124 chamados), Tijuca (96 chamados) e Barra da Tijuca (60 chamados).

-- Questão 4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?

-- Fazemos novamente o join com a tabela de bairros, mas dessa vez pegando os nomes das subprefeituras dos bairros,
-- e agrupando pelas subprefeituras também (250,04 MB)
SELECT b.subprefeitura, COUNT(c.id_chamado) AS chamados_totais
FROM `datario.adm_central_atendimento_1746.chamado` c
JOIN `datario.dados_mestres.bairro` b ON c.id_bairro = b.id_bairro
WHERE DATE(c.data_inicio) = '2023-04-01'
GROUP BY b.subprefeitura
ORDER BY chamados_totais DESC;
-- Resposta Questão 4: a subprefeitura com mais chamados abertos nesse dia foi a Zona Norte, com 534 chamados abertos.

-- Questão 5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?

-- Reconhecer um chamado não associado a nenhum bairro é simples, são os chamados com id_bairro = NULL.
-- Já para os chamados não associados a nenhuma subprefeitura, pode ser por um de dois motivos:
    -- O chamado não está associado a nenhum bairro (id_bairro = NULL)
    -- O bairro associado a ele não está associado a nenhuma subprefeitura (já que o chamado só se associa à subprefeitura indiretamente através do bairro)

-- Checando se há algum bairro não associado a nenhuma subprefeitura
SELECT COUNT(*) AS total_nulls 
FROM `datario.dados_mestres.bairro`
WHERE subprefeitura IS NULL;
-- Com uma busca rápida, percebemos que todos os bairros estão associados a alguma subprefeitura,
-- logo quando um chamado não está associado a nenhuma subprefeitura, é porque ele não está associado a nenhum bairro.

-- Checamos então quantos casos temos de id_bairro = NULL na tabela de chamados
SELECT COUNT(*) AS total_nulls 
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01' AND id_bairro IS NULL;
-- Temos 131 chamados com id_bairro = NULL

-- Olhamos então para os casos em que id_bairro = NULL na tabela de chamados, para averiguar a situação
-- AINDA NÃO ENTENDI O PORQUÊ

-- Chamados do 1746 em grandes eventos
-- Questão 6
