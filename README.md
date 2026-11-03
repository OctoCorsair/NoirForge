<div align="center">

# 🕵️ NoirForge

**Gerador de casos de ficção policial com sabor de noir paulistano.**
Vítima, suspeitos, álibis, pistas verdadeiras, falsas pistas e uma reviravolta, tudo salvo em SQLite.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Dependências](https://img.shields.io/badge/depend%C3%AAncias-zero-7f1d1d?style=for-the-badge)
[![CI](https://github.com/OctoCorsair/NoirForge/actions/workflows/ci.yml/badge.svg)](https://github.com/OctoCorsair/NoirForge/actions)
![License](https://img.shields.io/badge/license-MIT-1f2937?style=for-the-badge)

*Um projeto do **OctoCorsair Labs***

</div>

---

## 🎯 Para quem é

- **Escritores** travados no enredo: gere um caso completo e use como ponto de partida.
- **Mestres de RPG** que precisam de um mistério para a mesa de hoje à noite.
- **Devs curiosos** que querem ver geração procedural determinística, SQLite e CLI em Python puro.

## 🚀 Instalação

```bash
git clone https://github.com/OctoCorsair/NoirForge.git
cd NoirForge
pip install -e .
```

Não há dependências externas, só a biblioteca padrão do Python.

## 🔦 Uso

```bash
noirforge new                         # caso aleatório, sem revelar o culpado
noirforge new --seed 7                # o mesmo caso toda vez que usar a seed 7
noirforge new --suspects 6 --save     # 6 suspeitos e salva no banco
noirforge new --seed 7 --solution     # revela culpado, falsas pistas e reviravolta

noirforge list                        # casos salvos
noirforge show 1 --solution           # reabre um caso salvo
noirforge export 1 --out caso.md      # exporta em Markdown
noirforge stats                       # estatísticas (consultas SQL com GROUP BY)
noirforge delete 1                    # apaga um caso
```

O banco fica em `noirforge.db` por padrão. Para mudar: `--db caminho.db` ou a variável `NOIRFORGE_DB`.

### Exemplo de saída

```text
# Fumaça e Chantagem
*São Paulo, 1947 · seed 7*

**Vítima:** Fausto Falcão, cantor de cabaré.
**Cena do crime:** o corpo foi encontrado no sótão, num hotel decadente da Santa Ifigênia.
**Arma:** um castiçal de bronze.

## Suspeitos
- **Januário Camargo** (irmão): motivo, uma vingança antiga; conta que esperava um trem na Estação da Luz.
- **Aurélio Guedes** (vizinho): motivo, uma herança prestes a ser alterada; garante que ajudava a fechar o caixa de uma padaria.
- **Euclides Albuquerque** (afilhado): motivo, chantagem que o levaria à ruína; diz que jogava cartas nos fundos de um bar.
- **Berenice Barcellos** (sócia): motivo, ciúme doentio; alega ter ido ao cinema na Avenida São João.

## Evidências
1. Só Januário Camargo tinha a chave do cadeado do sótão.
2. Aurélio Guedes sumiu da cidade no dia seguinte.
3. Dinheiro vivo foi encontrado escondido na casa de Euclides Albuquerque.
4. Testemunhas viram Berenice Barcellos discutindo com a vítima poucas horas antes do crime.
5. O castiçal de bronze que sumiu da sala apareceu lavado às pressas na casa de Januário Camargo.
6. Ninguém ouviu Januário Camargo perguntar como a vítima morreu.

> 🔎 Quem fez isso? Revele com `--solution` quando estiver pronto.
```

## 🧠 Como funciona

Todo caso nasce de uma **seed**. A mesma seed com o mesmo número de suspeitos gera sempre o mesmo caso, então dá para compartilhar mistérios só com um número.

O gerador garante que cada caso seja **resolvível**:

1. Sorteia a vítima e os suspeitos, com nomes únicos e concordância de gênero.
2. Escolhe **um culpado**, cujo álibi é falso.
3. Cria **3 pistas verdadeiras** ligadas ao culpado: uma pela arma, uma pelo local e uma geral.
4. Cria até **3 falsas pistas** contra inocentes, cada uma com uma explicação (o segredo que fez aquele suspeito parecer culpado).
5. Embaralha as evidências e adiciona uma reviravolta.

## 🗄️ Banco de dados

Três tabelas relacionadas, com `FOREIGN KEY ... ON DELETE CASCADE`:

```text
cases ──< suspects
  └─────< clues
```

Salvar o mesmo caso duas vezes não duplica (`UNIQUE (seed, num_suspects)`).

## 🗂️ Estrutura

```text
NoirForge/
├── src/noirforge/
│   ├── data.py        # ingredientes narrativos (edite à vontade!)
│   ├── generator.py   # geração determinística do caso
│   ├── render.py      # saída em Markdown
│   ├── db.py          # SQLite: salvar, carregar, listar, stats
│   └── cli.py         # interface de linha de comando
├── tests/
└── .github/workflows/ci.yml
```

## 🧪 Testes

```bash
python -m unittest discover -s tests -v
```

Cobrem determinismo, unicidade do culpado, estrutura de pistas, nomes únicos, ida e volta no banco e exclusão em cascata.

## ✍️ Personalize

Quer outra cidade, outra época ou um clima mais sombrio? Tudo está em `src/noirforge/data.py`: nomes, armas, locais, motivos, álibis, segredos e reviravoltas. É só editar as listas.

## 🛣️ Roadmap

- [ ] Opção `--lang en` com banco de dados em inglês
- [ ] Mais cenários (Rio de Janeiro, Recife, Porto Alegre)
- [ ] Exportar o caso em PDF
- [ ] Modo "interrogatório": perguntas e respostas dos suspeitos
- [ ] Interface web simples

## 📄 Licença

MIT. Veja [LICENSE](LICENSE).

---

<div align="center">

*Código limpo. Enredo sujo.* 🚬

Feito por [OctoCorsair](https://github.com/OctoCorsair)

</div>
