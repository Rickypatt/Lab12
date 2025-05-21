from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getCountry():
        conn = DBConnect.get_connection()

        res = []
        cursor = conn.cursor(dictionary = True)
        query = """select distinct Country
                    from go_retailers gr """

        cursor.execute(query)

        for row in cursor:
            res.append(row["Country"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(`Date`) as year
                        from go_daily_sales gds  """

        cursor.execute(query)

        for row in cursor:
            res.append(row["year"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getRetailers(country):
        conn = DBConnect.get_connection()

        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr 
                    where Country = %s """

        cursor.execute(query, (country,))

        for row in cursor:
            res.append(Retailer(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getArchi(country, anno):
        conn = DBConnect.get_connection()

        res = []
        cursor = conn.cursor(dictionary=True)
        query = """select gds1.Retailer_code as r1,gds2.Retailer_code as r2, count(distinct gds1.Product_number) as peso
                    from go_daily_sales gds1, go_daily_sales gds2, go_retailers gr1, go_retailers gr2
                    where gds1.Product_number = gds2.Product_number
                    and  gds1.Retailer_code < gds2.Retailer_code
                    and gds1.Retailer_code = gr1.Retailer_code
                    and gds2.Retailer_code = gr2.Retailer_code 
                    and gr1.Country = %s
                    and gr2.Country = %s
                    and year(gds1.`Date`) = year(gds2.`Date`)
                    and year(gds1.`Date`) = %s
                    group by gds1.Retailer_code, gds2.Retailer_code """

        cursor.execute(query, (country,country, anno))

        for row in cursor:
            res.append((row["r1"], row["r2"], row["peso"]))

        cursor.close()
        conn.close()
        return res


