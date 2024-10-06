import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import mysql.connector

class Bank:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="username",
            password="password",
            database="bank"
        )
        self.cursor = self.db.cursor()

    def register(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)", (username, password, 0.0))
        self.db.commit()

    def login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = self.cursor.fetchone()
        return user is not None

    def deposit(self, username, amount):
        self.cursor.execute("UPDATE users SET balance = balance + %s WHERE username = %s", (amount, username))
        self.db.commit()
        self.cursor.execute("INSERT INTO transactions (username, amount, type) VALUES (%s, %s, %s)", (username, amount, 'deposit'))
        self.db.commit()

    def withdraw(self, username, amount):
        self.cursor.execute("UPDATE users SET balance = balance - %s WHERE username = %s", (amount, username))
        self.db.commit()
        self.cursor.execute("INSERT INTO transactions (username, amount, type) VALUES (%s, %s, %s)", (username, amount, 'withdrawal'))
        self.db.commit()

    def get_balance(self, username):
        self.cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))
        balance = self.cursor.fetchone()[0]
        return balance

    def predict_balance(self, username, amount):
        # Create a simple linear regression model to predict future balance
        X = np.array([self.get_balance(username)]).reshape(-1, 1)
        y = np.array([amount])
        model = LinearRegression()
        model.fit(X, y)
        return model.predict(np.array([[self.get_balance(username)]]))[0]

    def train_model(self):
        # Train a linear regression model on transaction data
        self.cursor.execute("SELECT amount, type FROM transactions")
        transactions = self.cursor.fetchall()
        X = np.array([transaction[0] for transaction in transactions]).reshape(-1, 1)
        y = np.array([transaction[1] == 'deposit' for transaction in transactions])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        return model
