#!/usr/bin/env python3
# Author: GreatBahram
import sqlite3
import time

class DBHelper:
    def __init__(self):
        self.create_schema()

    def connect(self, database="database.db"):
        try:
            conn = sqlite3.connect(database)
            return  conn
        except Exception as e:
            print(e)
        return None

    def create_schema(self):
        conncection = self.connect()
        sql = ("""create table if not exists person(
        id integer not null primary key autoincrement,
        forename text,
        surname text );
        create table if not exists payment(
                id integer not null primary key autoincrement,
                date text,
                buyer integer not null REFERENCES person(id),
                debtor integer not null REFERENCES person(id),
                price integer not null,
                description text,
                sale integer not null
                );
        """)
        try:
            with conncection as con:
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            conncection.commit()

    def execute_something(self, query, parameters=()):
        conncection = self.connect()
        flag = None
        try:
            with conncection as con:
                cur = con.cursor()
                result = cur.execute(query, parameters)
            flag = True
        finally:
            conncection.commit()
        if flag:
            return result 
        return flag

    def payoff_debt(self, debtor, creditor, price, description="No description", sale=0):
        date = time.asctime()
        sql = """insert into payment values (null, ?, ?, ?, ?, ?, ?)"""
        parameters = (date, creditor, debtor, price, description, sale)
        flag = self.execute_something(sql, parameters)
        if not flag:
            raise Exception('Payoff failed.')

    def add_new_item(self, buyer, debtors, price, description="No description", sale=1):
        date = time.asctime()
        price_per_person = price / len(debtors)
        for debtor in debtors:
            if buyer != debtor:
                sql = """insert into payment values (null, ?, ?, ?, ?, ?, ?)"""
                parameters = (date, buyer, debtor, price_per_person, description, sale)
                flag = self.execute_something(sql, parameters)
                if not flag:
                    raise Exception('Insert failed.')

    def _sum_buys(self, _id):
        #query = "select sum(price) from payment where buyer=?"
        query = "select sum(price) from payment where buyer=? and sale=1 "
        result = self.execute_something(query, (_id,))
        return next(result)[0]

    def _sum_debts(self, _id):
        query = "select sum(price) from payment where debtor=? and sale=1"
        result = self.execute_something(query, (_id, ))
        return next(result)[0]

    def _sum_other_payoffs(self, _id):
# I payoff to others
        query = "select sum(price) from payment where debtor=? and sale=0"
        result = self.execute_something(query, (_id, ))
        return next(result)[0]

    def _sum_self_payoffs(self, _id):
# other payoff to me
        query = "select sum(price) from payment where buyer=? and sale=0"
        result = self.execute_something(query, (_id, ))
        return next(result)[0]
    def sum_sums(self, _id):
        try:
            buy_amount = int(self._sum_buys(_id))
        except Exception as err:
            print(err)
            buy_amount = 0

        try:
            debt_amount = int(self._sum_debts(_id))
        except:
            debt_amount = 0

        try:
            self_payoff_amount = int(self._sum_self_payoffs(_id))
        except Exception as err:
            print(err)
            self_payoff_amount = 0
        try:
            other_payoff_amount = int(self._sum_other_payoffs(_id))
        except Exception as err:
            print(err)
            other_payoff_amount = 0

        print("{} : Buy is {} Debt is {} Self_Payoff is {} other_Payoff".format(_id, buy_amount, \
                debt_amount, self_payoff_amount, other_payoff_amount))
        return buy_amount - self_payoff_amount- debt_amount + other_payoff_amount 
    
    def return_persons(self):
        sql = "select * from person"
        results = self.execute_something(sql)
        return results

    def sum_for_all(self):
        results = self.return_persons()
        output = []
        for result in results:
            fill = {}
            fill['id'] = result[0]
            fill['forename'] = result[1]
            fill['surname'] = result[2]
            fill['payment'] = self.sum_sums(result[0])
            output.append(fill)
        return output

    def shop_list(self):
        query = "select * from payment where sale=1 "
        results = self.execute_something(query)
        persons = self.return_persons().fetchall()
        return results.fetchall()

    def payoff_list(self):
        query = "select * from payment where sale=0 "
        results = self.execute_something(query)
        persons = self.return_persons().fetchall()
        return results.fetchall()

if __name__ == '__main__':
    dbhelper = DBHelper()
