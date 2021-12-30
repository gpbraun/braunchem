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

> **Assinale** a alternativa que mais se aproxima da entalpia de reação, $\Delta H/\pu{kJ mol-1 |.

a unidade é digitada utilizando a função `\unit{<valor>}` do pacote `siunitx`.

As alternativas são colocadas com a função:

```latex
\OptionsNum{ 100, 200, 300, 400, 500 }
```

### Proposições

O **comando** de questões 

=======

- Temperatura de fusão do ferro: 1540 °C
- Função trabalho do potássio: 2,29 eV
- Função trabalho do zinco: 3,63 eV
- Entalpia de formação da ureia (s): -333,51 kJ/mol
- Entalpia de combustão do metano (g): -890,5 kJ/mol
- Entalpia de vaporização do Br₂: 30 kJ/mol
- Entalpia de vaporização CH₃CHBrCH₂Br: 35,61 kJ/mol

# Dados Termodinâmicos

## Compostos inorgânicos

### Alumínio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Al(s)` | 0 | 0 | 24,35 | 28,33 | 
`Al^3+(aq)` | 524,7 | 481,2 |  | -321,7 | 
`Al2O3(s)` | -1675,7 | -1582,35 | 79,04 | 50,92 | 
`Al(OH)3(s)` | -1276 |  |  |  | 
`AlCl3(s)` | -704,2 | -628,8 | 91,84 | 110,67 | 

### Antimônio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Sb(s)` | 0 | 0 | 25,23 | 45,69 | 
`SbH3(g)` | 145,11 | 147,75 | 41,05 | 232,78 | 
`SbCl3(g)` | -313,8 | -301,2 | 76,69 | 337,8 | 
`SbCl5(g)` | -394,34 | -334,29 | 121,13 | 401,94 | 

### Arsênio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`As(s)` | 0 | 0 | 24,64 | 35,1 | 
`As2S3(s)` | -169 | -168,6 | 116,3 | 163,6 | 
`AsO4^3-(aq)` | -888,14 | -648,41 |  | -162,8 | 

### Bário

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Ba(s)` | 0 | 0 | 28,07 | 62,8 | 
`Ba+2(aq)` | -537,64 | -560,77 |  | 9,6 | 
`BaO(s)` | -553,5 | -525,1 | 47,78 | 70,42 | 
`BaCO3(s)` | -1216,3 | -1137,6 | 85,35 | 112,1 | 
`BaCO3(aq)` | -1214,78 | -1088,59 |  | -47,3 | 

### Boro

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`B(s)` | 0 | 0 | 11,09 | 5,86 | 
`B2O3(s)` | -1272,8 | -1193,7 | 62,93 | 53,97 | 
`BF3(g)` | -1137 | -1120,3 | 50,46 | 254,12 | 

### Bromo

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Br2(l)` | 0 | 0 | 75,69 | 152,23 | 
`Br2(g)` | 30,91 | 3,11 | 36,02 | 245,46 | 
`Br(g)` | 111,88 | 82,4 | 20,79 | 175,02 | 
`Br-(aq)` | -121,55 | -103,96 |  | 82,4 | 
`HBr(g)` | -36,4 | -53,45 | 29,14 | 198,7 | 

### Cálcio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Ca(s)` | 0 | 0 | 25,31 | 41,42 | 
`Ca(g)` | 178,2 | 144,3 | 20,79 | 154,88 | 
`Ca+2(aq)` | -542,83 | -553,58 |  | -53,1 | 
`CaO(s)` | -635,09 | -604,03 | 42,8 | 39,75 | 
`Ca(OH)2(s)` | -986,09 | -898,49 | 87,49 | 83,39 | 
`Ca(OH)2(aq)` | -1002,82 | -868,07 |  | -74,5 | 
`CaCO3(s)` | -1206,9 | -1128,8 | 81,88 | 92,9 | 
`CaCO3(aragonita)` | -1207,1 | -1127,8 | 81,25 | 88,7 | 
`CaCO3(aq)` | -1219,97 | -1081,39 |  | -110 | 
`CaF2(s)` | -1219,6 | -1167,3 | 67,03 | 68,87 | 
`CaF2(aq)` | -1208,09 | -1111,15 |  | -80,8 | 
`CaCl2(s)` | -795,8 | -748,1 | 72,59 | 104,6 | 
`CaCl2(aq)` | -877,1 | -816 |  | 59,8 | 
`CaBr2(s)` | -682,8 | -663,6 | 72,59 | 130 | 
`CaC2(s)` | -59,8 | -64,9 | 62,72 | 69,96 | 
`CaSO4(s)` | -1434,11 | -1321,79 | 99,66 | 106,7 | 
`CaSO4(aq)` | -1452,1 | -1298,1 |  | -33,1 | 

### Carbono

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`C(grafite)` | 0 | 0 | 8,53 | 5,74 | 
`C(diamante)` | 1,895 | 2,9 | 6,11 | 2,377 | 
`C(g)` | 716,68 | 671,26 | 20,84 | 158,1 | 
`CO(g)` | -110,53 | -137,17 | 29,14 | 197,67 | 
`CO2(g)` | -393,51 | -394,36 | 37,11 | 213,74 | 
`CO3^2-(aq)` | -677,14 | -527,81 |  | 56,9 | 
`CCl4(l)` | -135,44 | -65,21 | 131,75 | 216,4 | 
`CS2(l)` | 89,7 | 65,27 | 75,7 | 151,34 | 
`HCN(g)` | 135,1 | 124,7 | 35,86 | 201,78 | 
`HCN(l)` | 108,87 | 124,97 | 70,63 | 112,84 | 
`HCN(aq)` | 107,1 | 119,7 |  | 124,7 | 

### Cério

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Ce(s)` | 0 | 0 | 26,94 | 72 | 
`Ce^3+(aq)` | -696,2 | -672 |  | -205 | 
`Ce^4+(aq)` | -537,2 | -503,8 |  | -301 | 

### Cloro

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Cl2(g)` | 0 | 0 | 33,91 | 223,07 | 
`Cl(g)` | 121,68 | 105,68 | 21,84 | 165,2 | 
`Cl-(aq)` | -167,16 | -131,23 |  | 56,5 | 
`HCl(g)` | -92,31 | -95,3 | 29,12 | 186,91 | 
`HCl(aq)` | -167,16 | -131,23 |  | 56,5 | 

### Cobre

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Cu(s)` | 0 | 0 | 24,44 | 33,15 | 
`Cu+(aq)` | 71,67 | 49,98 |  | 40,6 | 
`Cu^2+(aq)` | 64,77 | 65,49 |  | -99,6 | 
`Cu2O(s)` | -168,6 | -146 | 63,64 | 93,14 | 
`CuO(s)` | -157,3 | -129,7 | 42,3 | 42,63 | 
`CuSO4(s)` | -771,36 | -661,8 | 100 | 109 | 
`CuSO4,5H2O(s)` | -2279,7 | -1879,7 | 280 | 300,4 | 

### Deutério ($\ce{^2H)

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`D2(g)` | 0 | 0 | 29,2 | 144,96 | 
`D2O(g)` | -249,2 | -234,54 | 34,27 | 198,34 | 
`D2O(l)` | -294,6 | -243,44 | 34,27 | 75,94 | 

### Flúor

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`F2(g)` | 0 | 0 | 31,3 | 202,78 | 
`F-(aq)` | -332,63 | -278,79 |  | -13,8 | 
`HF(g)` | -271,1 | -273,2 | 29,13 | 173,78 | 
`HF(aq)` | -330,08 | -296,82 |  | 88,7 | 

### Hidrogênio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`H2(g)` | 0 | 0 | 28,82 | 130,68 | 
`H(g)` | 217,97 | 203,25 | 20,78 | 114,71 | 
`H+(aq)` | 0 | 0 | 0 | 0 | 
`H2O(l)` | -285,83 | -237,13 | 75,29 | 69,91 | 
`H2O(g)` | -241,82 | -228,57 | 33,58 | 188,83 | 
`H2O2(l)` | -187,78 | -120,35 | 89,1 | 109,6 | 
`H2O2(aq)` | -191,17 | -134,03 |  | 143,9 | 
`H3O(aq)` | -285,83 | -237,13 | 75,29 | 69,91 | 

### Iodo

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`I2(s)` | 0 | 0 | 54,44 | 116,14 | 
`I2(g)` | -62,44 | -19,33 | 36,9 | 260,69 | 
`I(aq)` | -55,19 | -51,57 |  | 111,3 | 
`HI(g)` | -26,48 | -1,7 | 29,16 | 206,59 | 

### Ferro

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Fe(s)` | 0 | 0 | 25,1 | 27,28 | 
`Fe^2+(aq)` | -89,1 | -78,9 |  | -137,7 | 
`Fe^3+(aq)` | -48,5 | -4,7 |  | -315,9 | 
`Fe3O4(s)` | -1118,4 | -1015,4 | 143,43 | 146,4 | 
`FeO(s)` | -824,2 | -742,2 | 103,85 | 87,4 | 
`Fe2O3(s)` | 0 | 0 |  |  | 
`FeS(s)` | -100 | -100,4 | 50,54 | 60,29 | 
`FeS(aq)` |  | -6,9 |  |  | 
`FeS2(s)` | -178,2 | -166,9 | 62,17 | 52,93 | 

### Chumbo

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Pb(s)` | 0 | 0 | 26,44 | 64,81 | 
`Pb^2+(aq)` | -1,7 | -24,43 |  | 10,5 | 
`PbO2(s)` | -277,4 | -217,33 | 64,64 | 68,6 | 
`PbSO4(s)` | -919,94 | -813,14 | 103,21 | 148,57 | 
`PbBr2(s)` | -278,7 | -261,92 | 80,12 | 161,5 | 
`PbBr2(aq)` | -244,8 | -232,34 |  | 175,3 | 

### Magnésio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Mg(s)` | 0 | 0 | 24,89 | 32,68 | 
`Mg(g)` | 147,7 | -113,1 | 20,79 | 148,65 | 
`Mg^2+(aq)` | -466,85 | -454,8 |  | -138,1 | 
`MgO(s)` | -601,7 | -569,43 | 37,15 | 26,94 | 
`MgCO3(s)` | -1095,8 | -1012,1 | 75,52 | 65,7 | 
`MgBr2(s)` | -524,3 | -503,8 |  | 117,2 | 

### Mercúrio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Hg(l)` | 0 | 0 | 27,98 | 76,02 | 
`Hg(g)` | 61,32 | 31,82 | 20,79 | 174,96 | 
`HgO(s)` | -90,83 | -58,54 | 44,06 | 70,29 | 
`Hg2Cl2(s)` | -265,22 | -210,75 | 102 | 192,5 | 

### Nitrogênio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`N2(g)` | 0 | 0 | 29,12 | 191,61 | 
`NO(g)` | 90,25 | 86,55 | 29,84 | 210,76 | 
`N2O(g)` | 82,05 | 104,2 | 38,45 | 219,85 | 
`NO2(g)` | 33,18 | 51,31 | 37,2 | 240,06 | 
`N2O4(g)` | 9,16 | 97,89 | 77,28 | 304,29 | 
`HNO3(l)` | -174,1 | -80,71 | 109,87 | 155,6 | 
`HNO3(aq)` | -207,36 | -111,25 |  | 146,4 | 
`NO3(aq)` | -205 | -108,74 |  | 146,4 | 
`NH3(g)` | -46,11 | -16,45 | 35,06 | 192,45 | 
`NH3(aq)` | -80,29 | -26,5 |  | 111,3 | 
`NH4(aq)` | -132,51 | -79,31 |  | 113,4 | 
`NH2OH(s)` | -114,2 |  |  |  | 
`HN3(g)` | 294,1 | 328,1 | 98,87 | 238,97 | 
`N2H4(l)` | 50,63 | 149,34 | 139,3 | 121,21 | 
`NH4NO3(s)` | -365,56 | -183,87 | 84,1 | 151,08 | 
`NH4Cl(s)` | -314,43 | -202,87 |  | 94,6 | 
`NH4ClO4(s)` | -295,31 | -88,75 |  | 186,2 | 

### Oxigênio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`O2(g)` | 0 | 0 | 29,36 | 205,14 | 
`O3(g)` | 142,7 | 163,2 | 39,29 | 238,93 | 
`OH-(aq)` | -229,99 | -157,24 |  | -10,75 | 

### Fósforo

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`P(s)` | 0 | 0 | 23,84 | 41,09 | 
`P4(g)` | 58,91 | 24,44 | 67,15 | 279,98 | 
`PH3(g)` | 5,4 | 13,4 | 37,11 | 210,23 | 
`P4O6(s)` | -1640 | 0 |  |  | 
`P4O10(s)` | -2984 | -2697 |  | 228,86 | 
`H3PO3(aq)` | -964,8 |  |  |  | 
`H3PO4(l)` | -1266,9 |  |  |  | 
`H3PO4(aq)` | -1288,34 | -1142,54 |  | 158,2 | 
`PCl3(l)` | -319,7 | -272,3 |  | 217,18 | 
`PCl3(g)` | -287 | -267,8 | 71,84 | 311,78 | 
`PCl5(g)` | -374,9 | -305 | 112,8 | 364,6 | 
`PCl5(s)` | -443,5 |  |  |  | 

### Potássio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`K(s)` | 0 | 0 | 29,58 | 64,18 | 
`K(g)` | 89,24 | 60,59 | 20,79 | 160,34 | 
`K+(aq)` | -252,38 | -283,27 |  | 102,5 | 
`KOH(s)` | -424,76 | -379,08 | 64,9 | 78,9 | 
`KOH(aq)` | -482,37 | -440,5 |  | 91,6 | 
`KF(s)` | -567,27 | -537,75 | 49,04 | 66,57 | 
`KCl(s)` | -436,75 | -409,14 | 51,3 | 82,59 | 
`KBr(s)` | -393,8 | -380,66 | 52,3 | 95,9 | 
`KI(s)` | -327,9 | -324,89 | 52,93 | 106,32 | 
`KClO3(s)` | -397,73 | -296,25 | 100,25 | 143,1 | 
`KClO4(s)` | -432,75 | -303,09 | 112,38 | 151 | 
`K2S(s)` | -380,7 | -364 |  | 105 | 
`K2S(aq)` | -471,5 | -480,7 |  | 190,4 | 

### Silício

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Si(s)` | 0 | 0 | 20 | 18,83 | 
`SiO2(s)` | -910,94 | -856,64 | 44,43 | 41,84 | 

### Prata

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Ag(s)` | 0 | 0 | 25,35 | 42,55 | 
`Ag+(aq)` | 105,58 | 77,11 |  | 72,68 | 
`Ag2O(s)` | -31,05 | -11,2 | 65,86 | 121,3 | 
`AgBr(s)` | -100,03 | -96,9 | 52,38 | 107,1 | 
`AgBr(aq)` | -15,98 | -26,86 |  | 155,2 | 
`AgCl(s)` | -127,07 | -109,79 | 50,79 | 96,2 | 
`AgCl(aq)` | -61,58 | -54,12 |  | 129,3 | 
`AgI(s)` | -61,84 | -66,19 | 56,82 | 115,5 | 
`AgI(aq)` | 50,38 | 25,52 |  | 184,1 | 
`AgNO3(s)` | -124,39 | -33,41 | 93,05 | 140,9 | 

### Sódio

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Na(s)` | 0 | 0 | 28,24 | 51,21 | 
`Na(g)` | 107,32 | 76,76 | 20,79 | 153,71 | 
`Na+(aq)` | -240,12 | -261,91 |  | 59 | 
`NaOH(s)` | -425,61 | -379,49 | 59,54 | 64,46 | 
`NaOH(aq)` | -470,11 | -419,15 |  | 48,1 | 
`NaCl(s)` | -411,15 | -384,14 | 50,5 | 72,13 | 
`NaBr(s)` | -361,06 | -348,98 | 51,38 | 86,82 | 
`NaI(s)` | -287,78 | -286,06 | 52,09 | 98,53 | 

### Enxofre

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`S(rômbico)` | 0 | 0 | 22,64 | 31,8 | 
`S(monoclinico)` | 0,33 | 0,1 | 23,6 | 32,6 | 
`S^2-(aq)` | 33,1 | 85,8 |  | -14,6 | 
`SO2(g)` | -296,83 | -300,19 | 39,87 | 248,22 | 
`SO3(g)` | -395,72 | -371,06 | 50,67 | 256,76 | 
`H2SO4(l)` | -813,99 | -690 | 138,9 | 156,9 | 
`SO4-2(aq)` | -909,27 | -744,53 |  | 20,1 | 
`HSO4-(aq)` | -997,34 | -755,91 |  | 131,8 | 
`H2S(g)` | -20,63 | -33,56 | 34,23 | 205,79 | 
`H2S(aq)` | -39,7 | -27,83 |  | 121 | 

### Estanho

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`SF6(g)` | -1209 | -1105,3 | 97,28 | 291,82 | 
`Sn(branco)` | 0 | 0 | 26,99 | 51,55 | 
`Sn(cinza)` | -2,09 | 0,13 | 25,77 | 44,14 | 
`SnO(s)` | -285,8 | -256,9 | 44,31 | 56,5 | 
`SnO2(s)` | -580,7 | -519,6 | 52,59 | 52,3 | 

### Zinco

`id` | Entalpia de formação `Hf` | Entalpia livre de formação `Gf` | Capacidade Calorífica `Cp` | Entropia `S` |
:-- | --: | --: | --: | --: |
`Zn(s)` | 0 | 0 | 25,4 | 41,63 | 
`Zn^2+(aq)` | -153,8 | -147,06 |  | -112,1 | 
`ZnO(s)` | -348,28 | -318,3 | 40,25 | 43,64 | 
>>>>>>> d83bf92cd20804d26061f3a76ccb39563ddd2716


## Entalpia de Ligação

`id` | Entalpia de Ligação `HL` |
:-- | --: |
`H2`   |  436 | 
`N2`   |  944 |
`O2`   |  496 |
`CO`   | 1074 |
`F2`   |  158 |
`Cl2`  |  242 |
`Br2`  |  193 |
`I2`   |  151 |
`HF`   |  565 |
`HCl`  |  431 |
`HBr`  |  366 |
`HI`   |  299 |
`C-H`  |  412 |
`C-C`  |  348 |
`C=C`  |  612 |
`C#C`  |  837 |
`C-O`  |  360 |
`C=O`  |  743 |
`C-N`  |  305 |
`C-F`  |  484 |
`C-Cl` |  338 |
`C-Br` |  276 |
`C-I`  |  238 |
`N-H`  |  388 |
`N-N`  |  163 |
`N=N`  |  409 |
`N-O`  |  210 |
`N=O`  |  630 |
`N-F`  |  270 |
`N-Cl` |  200 |
`O-H`  |  463 |
`O-O`  |  157 |
`benzeno` | 299 |