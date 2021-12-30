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

## Dados a serem adicionados
Temperatura de fusão do ferro: 1540 °C
Função trabalho do potássio: 2,29 eV
Função trabalho do zinco: 3,63 eV
Capacidade calorífica da água (l): 4,2 J/(K g) 
Entalpia de formação da glicose (s)
Entalpia de formação do cloreto de prata (s)
Entalpia de ligação Cl-Cl.
Calor de fusão do gelo: 80 cal/g
Calor específico do gelo: 0,5 cal/(g K)
Calor específico da água líquida: 1 cal/(g K)
Capacidade calorífica em pressão constante do O₂: 30 J/(K mol)
Entalpia de formação da ureia (s): -333,51 kJ/mol
Entalpia de formação do CO₂ (g): -393,51 kJ/mol
Entalpia de formação da água (l): -286 kJ/mol
Entalpia de combustão do metano (g): -890,5 kJ/mol
Energia de ligação C-C: 347 kJ/mol
Energia de ligação C-H: 413 kJ/mol
Energia de ligação C=O: 803 kJ/mol
Energia de ligação H-H: 436 kJ/mol
Energia de ligação O=O: 498 kJ/mol
Entalpia de vaporização do Br₂: 30 kJ/mol
Entalpia de vaporização CH₃CHBrCH₂Br: 35,61 kJ/mol
Energia de ligação C=C: 612 kJ/mol
Energia de ligação Br-Br: 193 kJ/mol
Entalpia padrão de sublimação da grafita: 720,0 kJ/mol
Energia de ligação C-O: 360 kJ/mol
Energia de ligação O-H: 463 kJ/mol



## Dados Termodinâmicos

| ID | Nome | Símbolo | Valor |
| -- | -- | -- | -- |
`Hf-CO2(g)` | Entalpia de formação do $\ce{CO2(g)}$ | $\Delta_\text{f} H_{\ce{CO2(g)}}$ | $\pu{-394 kJ.mol^{-1}}$ |