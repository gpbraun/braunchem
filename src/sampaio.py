import psycopg2

from topic import links2topic


#
# MAIN
#

simulados = {
    '0-MAT': {
        'title': 'Ciclo Diagnóstico - Matemática',
        'template': 'IME',
        'problems': {
            'Matemática': [
                    '9fu8EHZuTxitSuJdfK5psQ',
                    'HNL1t7AlTgqZR31AVqw9ag',
                    'ttJiAAHzSWSRjRDnHyC9Dw',
                    'sV_V7sDiTZepDo9MTU0oag',
                    'vTrRcaEfQNeo0ZbGfHbuCg'
            ]
        }
    },
    '0-FIS': {
        'title': 'Ciclo Diagnóstico - Física',
        'template': 'IME',
        'problems': {
            'Física': [
                'jslFnKpvTGWqkXVuGNJ_FA',
                'WcI78jOjTo2VqTFyZ9JEMQ',
                '1byU8AU-Q-OcX7qCgBjgcQ',
                'akRrouPMR2CI4OQjUVkI0w',
                'iCLe2iilTNWG13h5Abry3A',
            ]
        }
    },
    '0-QUI': {
        'title': 'Ciclo Diagnóstico - Química',
        'template': 'IME',
        'problems': {
            'Química': [
                'SEQuMruCRWSYmUiTD9DNYw',
                'Y4lkaGudS1uqIhlVQBOddg',
                'WhiwTX6AR7-qv6rZZ5HIyQ',
                'FTI9ci8qSNe37AyqYr5XoQ',
                '42p9IjEZTx-qAoW6Y-wFtg',
            ],
        }
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
            data['problems'],
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
