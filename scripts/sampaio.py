import psycopg2

from topic import links2topic


#
# MAIN
#

simulados = {
    '0-MAT': {
        'title': 'Ciclo Diagnóstico - Matemática',
        'template': 'IME',
        'links': [
            '9fu8EHZuTxitSuJdfK5psQ',
            'HNL1t7AlTgqZR31AVqw9ag',
            'ttJiAAHzSWSRjRDnHyC9Dw',
            'sV_V7sDiTZepDo9MTU0oag',
            'vTrRcaEfQNeo0ZbGfHbuCg'
        ]
    },
    '0-FIS': {
        'title': 'Ciclo Diagnóstico - Física',
        'template': 'IME',
        'links': [
            'jslFnKpvTGWqkXVuGNJ_FA',
            '1byU8AU-Q-OcX7qCgBjgcQ',
            'akRrouPMR2CI4OQjUVkI0w',
            'iCLe2iilTNWG13h5Abry3A',
            'WcI78jOjTo2VqTFyZ9JEMQ'
        ]
    },
    '0-QUI': {
        'title': 'Ciclo Diagnóstico - Química',
        'template': 'IME',
        'links': [],
    },
}


def main():
    conn = psycopg2.connect(
        host='editor.painelcupula.com',
        port=5432,
        database='codimd',
        user='codimd',
        password='change_password'
    )
    cur = conn.cursor()

    for name, data in simulados.items():
        p = links2topic(
            cur,
            name,
            data['links'],
            area='Pensi2022',
            title=data['title'],
            template=data['template'],
        )
        # caderno de questões
        p.generate_pdf(name, print_level=0)
        # gabarito
        p.generate_pdf(name+'-S', print_level=2)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
