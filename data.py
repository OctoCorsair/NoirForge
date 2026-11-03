"""Banco de ingredientes narrativos (noir paulistano)."""

FIRST_NAMES = {
    "m": ["Aurélio", "Benedito", "Caetano", "Duarte", "Euclides", "Fausto",
          "Gumercindo", "Horácio", "Ivo", "Januário"],
    "f": ["Adalgisa", "Berenice", "Cecília", "Dulce", "Eugênia", "Fabíola",
          "Glória", "Hortência", "Iracema", "Josefina"],
}

SURNAMES = ["Albuquerque", "Barcellos", "Camargo", "Dantas", "Esteves",
            "Falcão", "Guedes", "Hollanda", "Itapuã", "Junqueira",
            "Lacerda", "Menezes"]

# (masculino, feminino)
OCCUPATIONS = [
    ("empresário", "empresária"),
    ("juiz", "juíza"),
    ("jornalista", "jornalista"),
    ("cantor de cabaré", "cantora de cabaré"),
    ("dono de tipografia", "dona de tipografia"),
    ("banqueiro", "banqueira"),
    ("médico", "médica"),
    ("comerciante", "comerciante"),
]

RELATIONS = [
    ("sócio", "sócia"),
    ("irmão", "irmã"),
    ("amante", "amante"),
    ("empregado", "empregada"),
    ("advogado", "advogada"),
    ("rival de negócios", "rival de negócios"),
    ("afilhado", "afilhada"),
    ("médico da família", "médica da família"),
    ("vizinho", "vizinha"),
    ("herdeiro", "herdeira"),
]

MOTIVES = [
    "uma herança prestes a ser alterada",
    "chantagem que o levaria à ruína",
    "ciúme doentio",
    "uma dívida de jogo impagável",
    "uma vingança antiga",
    "ambição de poder",
]

ALIBIS = [
    "diz que jogava cartas nos fundos de um bar",
    "afirma ter passado a noite na missa da meia-noite",
    "jura que dormia no quarto de uma pensão",
    "alega ter ido ao cinema na Avenida São João",
    "garante que ajudava a fechar o caixa de uma padaria",
    "conta que esperava um trem na Estação da Luz",
    "diz que estava numa roda de samba até de madrugada",
]

SECRETS = [
    "mantinha um caso amoroso escondido",
    "negociava em segredo a venda do próprio negócio",
    "frequentava uma casa de jogo clandestina",
    "abrigava um irmão foragido da polícia",
    "escrevia cartas anônimas para a imprensa",
]

CULPRIT_SECRET = "planejou o crime com semanas de antecedência"

# (descrição da arma, pista que liga a arma ao culpado)
WEAPONS = [
    ("uma navalha de cabo de madeira",
     "Um barbeiro jura ter afiado uma navalha idêntica para {culprit} na semana passada."),
    ("um castiçal de bronze",
     "O castiçal de bronze que sumiu da sala apareceu lavado às pressas na casa de {culprit}."),
    ("veneno no café",
     "O frasco de veneno foi comprado com nome falso, mas a letra no recibo é a de {culprit}."),
    ("uma corda de piano",
     "O afinador notou que faltava uma corda no piano de {culprit}."),
    ("um abridor de cartas",
     "O abridor de cartas com monograma sumiu da mesa de {culprit} no dia do crime."),
    ("uma chave inglesa",
     "Graxa de uma chave inglesa foi encontrada nas luvas de {culprit}."),
]

# (onde o corpo foi achado, pista que liga o local ao culpado)
LOCATIONS = [
    ("no escritório dos fundos",
     "Só se entrava no escritório dos fundos com chave, e {culprit} mandou fazer uma cópia semanas antes."),
    ("no porão",
     "Barro do porão foi encontrado na barra do casaco de {culprit}."),
    ("no sótão",
     "Só {culprit} tinha a chave do cadeado do sótão."),
    ("na cozinha",
     "Um empregado viu {culprit} saindo pela porta da cozinha fora de hora."),
    ("no corredor dos fundos",
     "O corredor foi limpo às pressas, e o pano sujo estava no armário de {culprit}."),
    ("na sala trancada",
     "A sala só tinha duas chaves: a da vítima e a que {culprit} jura ter perdido."),
]

CULPRIT_CLUES = [
    "Um lenço bordado com as iniciais de {culprit} foi achado sob o sofá.",
    "O álibi de {culprit} desmorona: o bilhete que apresentou é de outro dia.",
    "Uma testemunha viu {culprit} lavando as mãos num chafariz de madrugada.",
    "Ninguém ouviu {culprit} perguntar como a vítima morreu.",
    "Restos de um bilhete queimado na lareira trazem a caligrafia de {culprit}.",
]

RED_HERRINGS = [
    "Testemunhas viram {suspect} discutindo com a vítima poucas horas antes do crime.",
    "{suspect} sumiu da cidade no dia seguinte.",
    "Dinheiro vivo foi encontrado escondido na casa de {suspect}.",
    "{suspect} mentiu à polícia sobre onde estava naquela noite.",
]

TWISTS = [
    "A vítima havia escrito, dias antes, um testamento secreto que mudava tudo.",
    "O crime foi montado desde o início para incriminar outra pessoa.",
    "A vítima sabia que seria morta e deixou uma pista escondida de propósito.",
    "Alguém da delegacia protegia o culpado.",
    "O relógio da cena foi adiantado para forjar a hora da morte.",
]

PLACES = [
    "num sobrado da Mooca",
    "num cabaré da Lapa",
    "no Edifício Copan",
    "num hotel decadente da Santa Ifigênia",
    "numa tipografia do Brás",
    "num casarão da Avenida Paulista",
    "num armazém do Cambuci",
]

ERAS = ["São Paulo, 1938", "São Paulo, 1947", "São Paulo, 1953",
        "São Paulo, 1962", "São Paulo, 1974"]

TITLES = [
    "O Caso {surname}",
    "A Última Noite de {first}",
    "Sombras sobre {surname}",
    "Ninguém Chora por {first}",
    "Fumaça e Chantagem",
]
