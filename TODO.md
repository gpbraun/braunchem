# TO-DO

## Pedagógico

- [ ] Usa uma escala de cores (com intensidade relativa ao valor da propriedade) nas figuras com a tabela periódica.
- [ ] Colocar uns "problemas de revisão/fixação" antes dos problemas de cada tópico?
- [ ] Separar os problemas iniciais pela seção?
- [ ] Escrever a solução de todas as provas do IME e do ITA pro site.
- [ ] 3I: Reações controladas por difusão (Keeler)
- [ ] Resolver os problemas de pH tipo $\ce{NH4CN}$ e $\ce{NaHCO3}$ somando as reações.
- [ ] Usar M em vez de mol.L-1 (condensar as alternativas): $\pu{2 {\scriptsize M}}$

## Quality of life

- [ ] Gerar a lista de elementos envolvidos em cada problema.

## Diagramação das questões

- [ ] Algumas questões estão com os dados digitados de maneira forçada para caber em duas colunas. Mudar isso na versão v2.
- [ ] Usar o caractere µ como prefixo para micro: $\pu{1 µmol}$.

## Template

- [ ] Formatar (como o Atkins em inglês) as referências às figuras e tabelas. Tentar colocar hiperlinks no pdf e no site.
- [ ] Legenda de figuras pequenas aparecendo do lado (testar).

## Software

- [ ] Usar o módulo `pydantic` para verificar possíveis erros nos problemas e tópicos. Sempre retornar o ID referente ao tópico em que o erro ocorreu.
- [ ] Usar a biblioteca `externalize` do tikz para deixar a compilação mais rápida. (talvez gerar a figura no format do pdf seja mais eficiente pq já é feito para o site).
- [ ] Separar o repositório da engine com o repositório da base de dados. Fazer isso na atualização da versão que usa lua.
- [ ] Criar um repositório `braunchem-figures` para dar uma atenção especial às figuras.
- [ ] Usar o linter de markdown, desabilitando as regras adequadas.
- [ ] Na hora de colocar as questões de ordenação, colocar na ordem correta. O programa embaralha as opções na hora de colocar (fica mais bem distribuido e eu não preciso pensar na ordem).

## Interface com o site

- [ ] Criar um filtro do PANDOC para corrigir as cores que o KaTeX usa.

## Novas features

- [ ] Criar um template do beamer que simule um quadro de aula.

