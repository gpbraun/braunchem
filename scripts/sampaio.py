import psycopg2

from simulado import create_simulado


#
# MAIN
#


def main():
    conn = psycopg2.connect(
        host='192.168.0.182',
        port=5432,
        database='codimd',
        user='codimd',
        password='change_password'
    )
    cur = conn.cursor()

    p = create_simulado(cur, ['s4NezMWTSrSntqe9Hcgz2w'])

    cur.close()
    conn.close()

    print(p)
    print(p.astex())


if __name__ == "__main__":
    main()
