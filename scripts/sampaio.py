import psycopg2

from topic import links2topic, topic2pdf


#
# MAIN
#

simulados = {
    '0-MAT': {
        'name': 'Ciclo Diagnóstico - Matemática',
        'template': 'IME',
        'links': [
            's4NezMWTSrSntqe9Hcgz2w'
        ]
    },
    '0-FIS': {
        'name': 'Ciclo Diagnóstico - Física',
        'template': 'IME',
    },
    '0-QUI': {
        'name': 'Ciclo Diagnóstico - Química',
        'template': 'IME',
    },
}


def main():
    conn = psycopg2.connect(
        host='192.168.0.15',
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
            ['s4NezMWTSrSntqe9Hcgz2w'],
            area='Pensi2022',
            template=data['template'],
        )

        topic2pdf(p, name)
        topic2pdf(p, name+'-S', answers=True, solutions=True)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
