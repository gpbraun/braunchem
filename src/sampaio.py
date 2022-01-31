import psycopg2

from topic import links2topic

import json


#
# MAIN
#

def main():
    conn = psycopg2.connect(
        host='editor.painelcupula.com',
        port=5432,
        database='codimd',
        user='codimd',
        password='change_password'
    )
    cur = conn.cursor()

    with open('src/simulados.json', 'r') as json_file:
        simulados = json.load(json_file)

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
