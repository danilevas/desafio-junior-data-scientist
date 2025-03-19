-- Tentando entender porque tem registro com id_bairro nulo
SELECT DISTINCT nome_unidade_organizacional
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01' AND id_bairro IS NULL
ORDER BY nome_unidade_organizacional;

SELECT DISTINCT nome_unidade_organizacional
FROM `datario.adm_central_atendimento_1746.chamado`
WHERE DATE(data_inicio) = '2023-04-01' AND id_bairro IS NOT NULL
ORDER BY nome_unidade_organizacional;
-- ORDER BY tipo, subtipo