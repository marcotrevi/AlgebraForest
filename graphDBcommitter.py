from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_equivalence_relation(self, expression1, expression2):
        # two expressions are equivalent if their difference = 0 modulo variable permutation
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_equivalence_relation, expression1, expression2)
            #for row in result:
            #    print("expressions: {expr1}, {expr2} are equivalent".format(expr1=row['expr1'], expr2=row['expr2']))

    @staticmethod
    def _create_and_return_equivalence_relation(tx, expression1, expression2):
        query = (
            "MATCH (expr1:Expression { name: $expression1 }) "
            "MATCH (expr2:Expression { name: $expression2 }) "
            "CREATE (expr1)-[:EQUALS]->(expr2) "
            "CREATE (expr2)-[:EQUALS]->(expr1) "
            "RETURN expr1, expr2"
        )
        result = tx.run(query, expression1=expression1, expression2=expression2)
        # "tx" is a transaction
        try:
            return [{"expr1": row["expr1"]["name"], "expr2": row["expr2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_dependency(self, expr, type):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_dependency, expr, type)
            #for row in result:
            #    print("expression: {expr} is of type {node}, connection created".format(expr=row['expr'], node=row['node']))

    @staticmethod
    def _create_and_return_dependency(tx, exprName, type):
        query = (
            "MATCH (expr:Expression), (node:Node)"
            "WHERE (expr.name=$exprName) AND (node.type=$type)"
            "CREATE (expr)-[:IS]->(node)"
            "RETURN expr,node"
        )
        result = tx.run(query, exprName=exprName, type=type)
        # "tx" is a transaction
        try:
            return [{"expr": row["expr"]["name"], "node": row["node"]["type"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createOperationNode(self, nodeType):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_OperationNode, nodeType)
            for row in result:
                print("node of type: {nodeType} created".format(nodeType=row['node']))

    @staticmethod
    def _create_and_return_OperationNode(tx, nodeType):
        query = (
            "CREATE (node:Node { type: $nodeType }) "
            "RETURN node"
        )
        result = tx.run(query, nodeType=nodeType)
        # "tx" is a transaction
        try:
            return [{"node": row["node"]["type"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def createExpressionNode(self, exprName):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_ExpressionNode, exprName)
            #for row in result:
            #    print("expression: {exprName} created".format(exprName=row['expr']))

    @staticmethod
    def _create_and_return_ExpressionNode(tx, exprName):
        query = (
            "CREATE (expr:Expression { name: $exprName }) "
            "RETURN expr"
        )
        result = tx.run(query, exprName=exprName)
        # "tx" is a transaction
        try:
            return [{"expr": row["expr"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]

    def getAllExpressions(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._returnExpressions)
        return result

    @staticmethod
    def _returnExpressions(tx):
        query = (
            "MATCH (e:Expression) "
            "RETURN e.name AS name"
        )
        result = tx.run(query)
        return [row["name"] for row in result]

    def checkIfLinked(self, expr1Name, expr2Name):
        with self.driver.session() as session:
            result = session.read_transaction(self._returnEquivalentRelationships, expr1Name, expr2Name)
        return result

    @staticmethod
    def _returnEquivalentRelationships(tx, expr1Name, expr2Name):
        query = (
            "MATCH (expr1:Expression)-[r:EQUALS]->(expr2:Expression)"
            "WHERE (expr1.name=$expr1Name) AND (expr2.name=$expr2Name)"
            "RETURN r"
        )
        result = tx.run(query,expr1Name=expr1Name,expr2Name=expr2Name)
        return [row for row in result]

if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://cb231e56.databases.neo4j.io"
    user = "neo4j"
    password = "5631ZHUiFDJ1kLH96wfoVdCzdF4kAqKCwPiXgFwucKI"
    app = App(uri, user, password)
#    app.createOperationNode("POW")
#    app.createExpressionNode("a+b")
#    app.create_dependency("x**2","POW")
#    app.create_equivalence_relation("A", "B")
#    r = app.checkIfLinked("A","B")
#    print(len(r))
#    app.find_person("Alice")
    app.close()