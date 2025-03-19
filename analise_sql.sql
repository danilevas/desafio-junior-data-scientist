-- NO FINAL BOTAR ; NO FINAL DE TODAS AS CONSULTAS

-- ||| Localização de chamados do 1746 |||
-- Questão 1. Quantos chamados foram abertos no dia 01/04/2023?

-- Checando se há algum id_chamado nulo (109,64 MB)
SELECT COUNT(*) AS total_nulls 
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE id_chamado IS NULL;
-- Aqui vemos que há 200 células em que id_chamado é nulo, logo quando fizer meu COUNT, é bom fazer COUNT(id_chamado) ao invés de COUNT(*),
-- para já desconsiderar as linhas com id_chamado nulo

-- INVESTIGAÇÃO DOS NULLS (são todos da GM no mesmo dia e horário de 2020)

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

-- Checando se há algum bairro não associado a nenhuma subprefeitura (1,85 KB)
SELECT COUNT(*) AS total_nulls 
FROM `datario.dados_mestres.bairro`
WHERE subprefeitura IS NULL;
-- Com uma busca rápida, percebemos que todos os bairros estão associados a alguma subprefeitura,
-- logo quando um chamado não está associado a nenhuma subprefeitura, é porque ele não está associado a nenhum bairro.

-- Checamos então quantos casos temos de id_bairro = NULL na tabela de chamados (140,44 MB)
SELECT COUNT(*) AS total_nulls 
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01' AND id_bairro IS NULL;
-- Temos 131 chamados com id_bairro = NULL

-- Olhamos então para os casos em que id_bairro = NULL na tabela de chamados, para averiguar a situação
-- AINDA NÃO ENTENDI O PORQUÊ

-- ||| Chamados do 1746 em grandes eventos |||
-- Questão 6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?

-- Agrupando por subtipo para vermos os chamados por subtipo no período especificado, filtrando para o subtipo "Perturbação do sossego" (750,27 MB)
SELECT subtipo, COUNT(id_chamado) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE subtipo = 'Perturbação do sossego'
AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
GROUP BY subtipo
ORDER BY subtipo
-- A consulta não nos traz nenhum resultado. Isso deve significar que não houveram chamados com esse subtipo no período especificado.
-- Para termos certeza, vamos checar isso.

-- Checando se há algum chamado desse subtipo no dataset, em qualquer data (657,84 MB)
SELECT subtipo, COUNT(id_chamado) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE subtipo = 'Perturbação do sossego'
GROUP BY subtipo
ORDER BY subtipo
-- A consulta nos retorna que existem 21991 chamados com esse subtipo no dataset.
-- Vamos ver agora quando esses chamados foram abertos.

-- Checando em quais datas houveram chamados do subtipo "Perturbação do sossego" (750,27 MB)
SELECT subtipo, DATE(data_inicio) AS data, COUNT(id_chamado) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE subtipo = 'Perturbação do sossego'
GROUP BY subtipo, data
ORDER BY data
-- Olhando a tabela proveniente dessa consulta, vemos que após o dia 31/12/2020, só houveram chamados do subtipo "Perturbação do sossego" novamente
-- no dia 08/03/2024. Há um gap de mais de 3 anos sem chamados desse subtipo. Logo, realmente podemos afirmar que houveram 0 chamados deste subtipo
-- desde 01/01/2022 até 31/12/2023 (incluindo extremidades).

-- Poderíamos nos contentar com essa resposta. Mas não iremos!
-- Primeiro eu pensei: será que pode haver algum outro subtipo parecido com esse, com alguma diferença de grafia?
-- Vendo todos os subtipos distintos na tabela chamado em ordem alfabética (548,16 MB)
SELECT DISTINCT subtipo
FROM `datario.adm_central_atendimento_1746.chamado`
ORDER BY subtipo
-- Olhando essa tabela, vejo que a única versão do subtipo "Perturbação do sossego" é a escrita dessa forma
-- (chequei por versões com diferenciação de maiúscula-minúscula ou de acento)

-- Então eu refleti: será que existe o tipo "Perturbação do sossego"?
-- Logo, chequei todos os tipos presentes
SELECT DISTINCT tipo
FROM `datario.adm_central_atendimento_1746.chamado`
ORDER BY tipo
-- Sim, esse tipo existe! Vamos analisar em que datas foram feitos chamados deste tipo

-- Checando em quais datas houveram chamados do tipo "Perturbação do sossego" (435,18 MB)
SELECT tipo, DATE(data_inicio) AS data, COUNT(id_chamado) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE tipo = 'Perturbação do sossego'
GROUP BY tipo, data
ORDER BY data
-- Ahh, agora sim! Olhando a tabela retornada por essa consulta, vemos que chamados do TIPO "Perturbação do sossego" ocorrem com certa consistência desde
-- 01/01/2021 até hoje! Trocando subtipo por tipo, podemos responder às perguntas dessa seção.

-- Agrupando por tipo para vermos os chamados por tipo no período especificado, filtrando para o tipo "Perturbação do sossego" (435,18 MB)
SELECT tipo, COUNT(id_chamado) AS total_chamados
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE tipo = 'Perturbação do sossego'
AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
GROUP BY tipo
ORDER BY tipo
-- Aqui verificamos que houveram 66078 chamados abertos com o tipo "Perturbação do sossego" no período especificado.

-- /// EXPLICAR MELHOR O QUE DEVE TER ACONTECIDO NESSA TROCA TIPO VS SUBTIPO, LEVANDO EM CONTA OS PERÍODOS \\\
-- /// FAZER ANÁLISE TIPO VS SUBTIPO ("Perturbação do sossego") \\\

-- Resposta Questão 6: nenhum chamado com o subtipo "Perturbação do sossego" foi aberto desde 01/01/2022 até 31/12/2023 (incluindo extremidades),
-- porém, neste período, foram abertos 66078 chamados com o TIPO "Perturbação do sossego".

-- Questão 7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio)

-- Quando eu fui olhar a tabela de eventos, percebi que haviam alguns problemas que dificultariam minha análise:
    -- Eventos sem data_inicial ou data-final
    -- Linhas sem dado relevante, apenas NULL, "nan" e NaN (desnecessárias)
    -- Discrepância entre a representação da ausência de valor (NULL, "nan" como texto e NaN)
    -- Falta de ID para diferenciar mais facilmente eventos com o mesmo nome, mas que ocorreram em datas diferentes (edições diferentes do mesmo evento)

-- Por isso, decidi criar uma tabela no meu conjunto de dados local do BigQuery que fosse uma versão mais limpa e completa dessa tabela de eventos.

-- Para isso, usei o comando "CREATE OR REPLACE TABLE", na intenção de criar essa tabela local sem as linhas com eventos nulos ou inválidos
-- e padronizando os NULL, "nan" e NaN apenas como NULL (636 B)
CREATE OR REPLACE TABLE `processo-seletivo-pcrj.meu_dataset.eventos_numerados` AS
WITH eventos_limpos AS (
    SELECT 
        ano,
        data_inicial,
        data_final,
        evento,
        -- Converter valores inválidos para NULL
        CASE 
            WHEN LOWER(CAST(taxa_ocupacao AS STRING)) IN ('nan', '') THEN NULL
            ELSE taxa_ocupacao 
        END AS taxa_ocupacao
    FROM `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`
    WHERE evento IS NOT NULL
      AND evento NOT IN ('', 'nan')
)
SELECT * FROM eventos_limpos
ORDER BY data_inicial, evento;

-- Depois, coloquei data_inicial e data_final nos eventos que não tinham (todas constavam na coluna ano),
-- e separei o Rock in Rio 2024 em 2 eventos, já que ele aconteceu em 2 períodos não contíguos de tempo. (1,13 KB)

-- Colocando data de início e fim na primeira parte do Rock in Rio 2024
UPDATE `processo-seletivo-pcrj.meu_dataset.eventos_numerados`
SET
    ano = '13/09 a 15/09 de 2024',
    data_inicial = '2024-09-13',
    data_final = '2024-09-15'
WHERE evento = 'Rock in Rio'
AND ano = '13/09 a 15/09 / 19/09 a 22/09 de 2024';

-- Colocando data de início e fim no Reveillón 2024-2025
UPDATE `processo-seletivo-pcrj.meu_dataset.eventos_numerados`
SET
    data_inicial = '2024-12-29',
    data_final = '2025-01-01'
WHERE evento = 'Réveillon'
AND ano = '29-31/12 e 01/01 (2024-2025)';

-- Colocando uma linha para a segunda parte do Rock in Rio 2024
INSERT INTO `processo-seletivo-pcrj.meu_dataset.eventos_numerados` (ano, data_inicial, data_final, evento, taxa_ocupacao)
VALUES
  ('19/09 a 22/09 de 2024', '2024-09-19', '2024-09-22', 'Rock in Rio', NULL);

-- Então, para facilitar a identificação de cada evento, incorporei um id (evento_id) e ordenei a tabela, assim como os ids
-- pela data de início do evento, e depois pelo nome do evento.
CREATE OR REPLACE TABLE `processo-seletivo-pcrj.meu_dataset.eventos_numerados` AS
WITH eventos_numerados AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY data_inicial, evento) AS evento_id,
        ano,
        data_inicial,
        data_final,
        evento,
        taxa_ocupacao
    FROM `processo-seletivo-pcrj.meu_dataset.eventos_numerados`
    ORDER BY evento_id
)
SELECT * FROM eventos_numerados
ORDER BY data_inicial, evento;

-- PLUS: MUDAR A COLUNA ANO PARA FICAR CERTINHA SEM SER MANUAL

-- Agora sim posso analisar os dados com mais confiança!

-- Selecionando os chamados com subtipo "Perturbação do sossego" em dias de eventos da tabela de eventos:
SELECT e.evento_id, e.evento, e.data_inicial, e.data_final, c.id_chamado
FROM `processo-seletivo-pcrj.meu_dataset.eventos_numerados` e
INNER JOIN `datario.adm_central_atendimento_1746.chamado` c
    ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    AND c.subtipo = 'Perturbação do sossego'
ORDER BY e.evento_id, c.id_chamado;
-- Como esperado, o retorno foi vazio, pois o subtipo "Perturbação do sossego" praticamente não foi utilizado a partir de 2021,
-- e os eventos são todos posteriores a esse ano.

-- Vamos fazer a mesma coisa com o TIPO "Perturbação do sossego":
-- Selecionando os chamados com tipo "Perturbação do sossego" em dias de eventos da tabela de eventos:
SELECT e.evento_id, e.evento, e.data_inicial, e.data_final, c.id_chamado
FROM `processo-seletivo-pcrj.meu_dataset.eventos_numerados` e
INNER JOIN `datario.adm_central_atendimento_1746.chamado` c
    ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    AND c.tipo = 'Perturbação do sossego'
ORDER BY e.evento_id, c.id_chamado;
-- Ahh, agora sim! 1889 registros.

-- Resposta Questão 7: não temos nenhum chamado com o subtipo "Perturbação do sossego" aberto durante os eventos
-- contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio), porém temos 1889 chamados com o subtipo "Perturbação do sossego"
-- abertos durante esses períodos.

-- A tabela dos eventos tratada está no arquivo "tabelas/7.1_eventos_tratados.csv"
-- e a tabela com os chamados de tipo "Perturbação do sossego" abertos durante os eventos selecionados pelo id_chamado,
-- juntamente com o evento a qual estão associados (caracterizado pelo evento_id),
-- está no arquivo "tabelas/7.2_chamados_tipo_perturb_sossego_dias_de_evento.csv".
-- Coloquei também nesse arquivo as datas de início e fim dos eventos para diferenciar os de mesmo nome sem ter que consultar duas tabelas.

-- Questão 8. Quantos chamados desse subtipo foram abertos em cada evento?

-- Consultando a quantidade de chamados com subtipo "Perturbação do sossego" nos dias de cada evento da tabela de eventos:
SELECT e.evento_id, e.evento, e.data_inicial, e.data_final, COALESCE(COUNT(c.id_chamado), 0) AS total_chamados
FROM `processo-seletivo-pcrj.meu_dataset.eventos_numerados` e
LEFT JOIN `datario.adm_central_atendimento_1746.chamado` c
    ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    AND c.subtipo = 'Perturbação do sossego'
GROUP BY e.evento_id, e.evento, e.data_inicial, e.data_final
ORDER BY e.evento_id;
-- Aqui temos 0 para todos os eventos, como esperado.

-- Consultando agora a quantidade de chamados com TIPO "Perturbação do sossego" nos dias de cada evento da tabela de eventos:
SELECT e.evento_id, e.evento, e.data_inicial, e.data_final, COALESCE(COUNT(c.id_chamado), 0) AS total_chamados
FROM `processo-seletivo-pcrj.meu_dataset.eventos_numerados` e
LEFT JOIN `datario.adm_central_atendimento_1746.chamado` c
    ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    AND c.tipo = 'Perturbação do sossego'
GROUP BY e.evento_id, e.evento, e.data_inicial, e.data_final
ORDER BY e.evento_id;

-- Resposta Questão 8: 0 chamados com o subtipo "Perturbação do sossego" foram abertos nos dias dos eventos da tabela de eventos,
-- mas 1889 chamados com o TIPO "Perturbação do sossego" foram abertos nesses dias. Para ver quantos chamados foram abertos nos dias de cada evento,
-- consulte o arquivo "tabelas/8.2_num_chamados_tipo_perturb_sossego_por_evento"

-- Questão 9. Qual evento teve a maior média diária de chamados abertos desse subtipo?

-- A partir daqui eu vou olhar apenas os chamados pelo tipo, já que vimos que não há nenhum chamado do subtipo "Perturbação do sossego" nos períodos desejados.
-- Primeiro vamos agrupar pelos eventos e por cada dia de evento, para vermos quantos chamados houveram em cada dia de cada evento (435,18 MB):
SELECT e.evento_id, e.evento, e.data_inicial, e.data_final, DATE(c.data_inicio) as data_chamado, COUNT(c.id_chamado) AS total_chamados,
FROM `teste-big-query-454013.meu_dataset.eventos_numerados` e
LEFT JOIN `datario.adm_central_atendimento_1746.chamado` c
    ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
    AND c.tipo = 'Perturbação do sossego'
    AND c.id_chamado IS NOT NULL
GROUP BY e.evento_id, e.evento, e.data_inicial, e.data_final, data_chamado
ORDER BY evento_id, data_chamado

-- Agora vamos aninhar essa consulta em outra para termos a média de chamado entre os dias de cada evento (435,18 MB):
WITH chamados_por_dia_e_evento AS (
    SELECT 
        e.evento_id,
        e.evento,
        e.data_inicial,
        e.data_final,
        DATE(c.data_inicio) as data_chamado,
        COUNT(c.id_chamado) AS total_chamados,
    FROM `teste-big-query-454013.meu_dataset.eventos_numerados` e
    LEFT JOIN `datario.adm_central_atendimento_1746.chamado` c
        ON DATE(c.data_inicio) BETWEEN e.data_inicial AND e.data_final
        AND c.tipo = 'Perturbação do sossego'
        AND c.id_chamado IS NOT NULL
    GROUP BY e.evento_id, e.evento, e.data_inicial, e.data_final, data_chamado
    ORDER BY evento_id, data_chamado
)
SELECT evento_id, evento, data_inicial, data_final, ROUND(AVG(total_chamados), 2) AS media_diaria_chamados
FROM chamados_por_dia_e_evento
GROUP BY evento_id, evento, data_inicial, data_final
ORDER BY media_diaria_chamados DESC;
-- Podemos ver, pela tabela gerada por essa consulta, as médias diárias de todos os eventos.

-- Resposta Questão 9: o evento com a maior média diária de chamados com o tipo "Perturbação do sossego" foi
-- a segunda parte do Rock in Rio 2022, compreendida entre os dias 08/09/2022 e 11/09/2022, com uma média de 142.25 chamados por dia de evento.

-- Questão 10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio)
-- e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.