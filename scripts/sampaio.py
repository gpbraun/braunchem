import psycopg2

from topic import links2topic, topic2pdf


#
# MAIN
#


def main():
    conn = psycopg2.connect(
        host='192.168.0.15',
        port=5432,
        database='codimd',
        user='codimd',
        password='change_password'
    )
    cur = conn.cursor()

    p = links2topic(
        cur,
        '2-DIS-QUI',
        ['s4NezMWTSrSntqe9Hcgz2w'],
        area='Simulados 2022',
        template='IME',
        answers=False,
    )

    topic2pdf(p)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
