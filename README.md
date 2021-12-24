# ChemProblems

## Texto

### Matemática

### Unidades

Valores com unidade devem ser colocadas utilizando a função `\qty{<valor>}{<unidade>}` do pacote `siunitx`. Todos os valores numéricos devem ser colocados utilizando a função `\unit{<valor>}` do pacote `siunitx`.

### Química

Fórmulas químicas devem ser colocadas utilizando a função  `\ch{<fórmula>}`.

## Problemas Discursivos

## Problemas Objetivos

### Resposta Numérica

O **comando** de questões objetivas com resposta numérica deve ser da seguinte forma:

> **Assinale** a alternativa que mais se aproxima da entalpia de reação, $\Delta H/\pu{kJ mol-1}$.

a unidade é digitada utilizando a função `\unit{<valor>}` do pacote `siunitx`.

As alternativas são colocadas com a função:

```latex
\OptionsNum{ 100, 200, 300, 400, 500 }
```

### Proposições

O **comando** de questões 

## Dados Termodinâmicos

| Código | Nome | Valor |
| -- | -- | -- |
| `Hf-CO2(g)` | Entalpia de formação do CO2(g) | $-394$ | 