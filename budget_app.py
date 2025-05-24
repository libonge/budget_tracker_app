import sqlite3
import datetime

class Expense: # initialize the amount of the expense self.category = category # initialize the category of the expens
    def __init__(self, amount, category):
        self.amount = amount
        self.category = category

class Income: # initialize the amount of the income self.category = category # initialize the category of the income

    def __init__(self, amount, category):
        self.amount = amount
        self.category = category

class BudgetApp:
    def __init__(self):
        # Connect to the SQLite database
        self.conn = sqlite3.connect("budget_app.db")
        # Create necessary tables if they don't exist
        self.create_tables()
        # Initialize lists and dictionaries to hold expenses, income, budgets, and financial goals
        self.expenses = []
        self.income = []
        self.budgets = {}
        self.load_budgets()
        self.financial_goals = {}
        self.load_financial_goals()

    def create_tables(self):
         # Similar CREATE TABLE statements for income, budgets, and financial_goals
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT,
                description TEXT,
                date DATE 
           )
       ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT,
                description TEXT,
                date DATE 
                )
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                amount REAL
               ) 
           ''')
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS financial_goals (
              description TEXT PRIMARY KEY,
              target_amount REAL
             ) 
         ''')
        self.conn.commit() 
        # Similar CREATE TABLE statements for income, budgets, and financial_goals
    

    def add_expense(self):
        # Function to add a new expense
        # Get user input for expense details: amount, description, category
        # Insert the expense into the expenses table in the database
        while True:
            amount_input = input("Enter expense amount: ")
            if not amount_input.replace('.', '', 1).isdigit():
                print("Invalid input. Please enter a valid amount.")
            else:
                amount = float(amount_input)
                description = input("Enter description of the expense: ")
                date = datetime.date.today().strftime("%Y-%m-%d")

                cur = self.conn.cursor()
                cur.execute("SELECT DISTINCT category FROM expenses")
                categories = cur.fetchall()

                print("Select a category by number:")
                for idx, category in enumerate(categories):
                    print(f"{idx+1}. {category[0]}")
                print(f"{len(categories) + 1}. Create a new category ")

                while True:
                    category_choice = input("Enter the number of the category or create a new one: ")
                    if category_choice.isdigit():
                        category_choice = int(category_choice)
                        if 1 <= category_choice <= len(categories):
                            category = categories[category_choice - 1][0]
                            break
                        elif category_choice == len(categories) + 1:
                            category = input("Enter the new category name: ")
                            break
                    print("Invalid input. Please enter a valid category number.")
               
                cur.execute("INSERT INTO expenses (date, description, category, amount) VALUES (?, ?, ?, ?)",
                            (date, description, category, amount))
                self.conn.commit()
                print("Expense successfully added.")
                break

    def view_expenses(self):
        # Function to view all expenses or a specific expense by ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, amount, category FROM expenses")
        expenses = cursor.fetchall()
        if not expenses:
          print("No expenses found.")
          return

        while True:
        # Display current expenses for reference
          print("Current Expenses:")
          for expense in expenses:
            print("Amount:", expense[1])
            print("Category:", expense[2])
            print()

          break # Exit the loop if a valid expense ID is provided

    def view_expenses_by_category(self):
        # Function to view expenses grouped by category
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        expenses_by_category = cursor.fetchall()
        if not expenses_by_category:
            print("No expenses found.")
            return
        
        print("Select a category to view expenses:")
        for idx, category in enumerate(expenses_by_category):
            print(f"{idx+1}. {category[0]}")

        while True:
            category_choice = input("Enter the number of the category to view expenses: ")
            if category_choice.isdigit():
                category_choice = int(category_choice)
                if 1 <= category_choice <= len(expenses_by_category):
                    category = expenses_by_category[category_choice - 1][0]
                    break
            print("Invalid input. Please enter a valid category number.")
        
        cursor.execute("SELECT id, amount, description, date FROM expenses WHERE category = ?", (category,))
        expenses = cursor.fetchall()
        
        for expense in expenses:
            print("Amount:", expense[1])
            print("Description:", expense[2])
            print("Date:", expense[3])
            print()

    def check_expense_id_exists(self, expense_id):
        # Helper function to check if an expense ID exists in the database
        cursor = self.conn.execute("SELECT COUNT(*) FROM expenses WHERE id = ?", (expense_id,))
        count = cursor.fetchone()[0]
        return count > 0

    def update_expense(self):
        # Helper function to check if an expense ID exists in the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM expenses")
        categories = cursor.fetchall()

        if not categories:
         print("No expense categories found.")
         return

        print("Select the category of the expense you want to update:")
        for idx, category in enumerate(categories):
         print(f"{idx+1}. {category[0]}")

        while True:
         category_choice = input("Enter the number of the category: ")
         if category_choice.isdigit():
            category_choice = int(category_choice)
            if 1 <= category_choice <= len(categories):
                category = categories[category_choice - 1][0]
                break
        print("Invalid input. Please enter a valid category number.")

        while True:
         new_amount_input = input("Enter the new expense amount: ")
         if not new_amount_input.replace('.', '', 1).isdigit():
            print("Invalid input. Please enter a valid amount.")
            continue
         break

        new_amount = float(new_amount_input)
        self.conn.execute("UPDATE expenses SET amount = ? WHERE category = ?", (new_amount, category))
        self.conn.commit()
        print("Expense updated successfully.") 

    def delete_expense_category(self):
        # Function to delete all expenses under a specific category
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM expenses")
        categories = [row[0] for row in cursor.fetchall()]

        if not categories:
          print("No categories found.")
          return

        while True:
         print("Available categories:")
         for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

         category_index_input = input("Enter the index of the category to delete: ")
         if not category_index_input.isdigit():
            print("Invalid input. Please enter a valid category index.")
            continue

         category_index = int(category_index_input)
         if category_index < 1 or category_index > len(categories):
            print("Invalid category index. Please enter a valid index.")
            continue

         category_to_delete = categories[category_index - 1]

         deletion_completed = False
         while not deletion_completed:
            confirm_delete = input(f"Are you sure you want to delete category '{category_to_delete}'? (yes/no): ").lower()
            if confirm_delete == "yes":
                self.conn.execute("DELETE FROM expenses WHERE category = ?", (category_to_delete,))
                self.conn.commit()
                print("Category deleted successfully.")
                deletion_completed = True
            elif confirm_delete == "no":
                print("Category deletion canceled.")
                return
            else:
                print("Invalid input. Please enter either 'yes' or 'no'.")
                continue

         break  # Exit the loop after successful deletion or cancellation 

    
    
    def add_income(self):
        # function to add income
        #Insert the income into the income table in the database
        while True:
            amount_input = input("Enter income amount: ")
            if not amount_input.replace('.', '', 1).isdigit(): # Check if input is a valid float
             print("Invalid input. Please enter a valid amount.")
             continue
            amount = float(amount_input)
            break # Break the loop if a valid amount is entered

        description = input("Enter description of the income: ")
        date = datetime.date.today().strftime("%Y-%m-%d")
        current_datetime = datetime.datetime.now()
        income_date = current_datetime.strftime("%Y-%m-%d")

        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT category FROM income")
        categories = cur.fetchall()

        print("Select a category by number:")
        for idx, category in enumerate(categories):
          print(f"{idx+1}. {category[0]}")
        print(f"{len(categories) + 1}. Create a new category ")

        while True:
           category_choice = input("Enter the number of the category or create a new one: ")
           if category_choice.isdigit():
               category_choice = int(category_choice)
               if 1 <= category_choice <= len(categories):
                category = categories[category_choice - 1][0]
                break
               elif category_choice == len(categories) + 1:
                  category = input("Enter the new category name: ")
                  break
               else:
                print("Invalid input. Please enter a valid category number.")
           else:
            print("Invalid input. Please enter a valid category number.")

        self.conn.execute("INSERT INTO income (date, description, category, amount) VALUES (?, ?, ?, ?)",
                      (income_date, description, category, amount))
        self.conn.commit()
        print("Income successfully added.") 

    def view_income(self):
        # function to view all income
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, amount, category, description, date FROM income")
        income = cursor.fetchall()
        if not income:
         print("No income found.")
         return

        while True:
         print("Current Income:")
         for entry in income:
            print("Amount:", entry[1])
            print("Category:", entry[2])
            print("Description:", entry[3])
            print("Date:", entry[4])
            print()
         break
    def view_income_by_category(self):
        # function to view income by category
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM income GROUP BY category")
        income_by_category = cursor.fetchall()
        if not income_by_category:
         print("No income found.")
         return

        print("Select a category to view income:")
        for idx, category in enumerate(income_by_category):
         print(f"{idx+1}. {category[0]}")

        while True:
            category_choice = input("Enter the number of the category to view income: ")
            if category_choice.isdigit():
             category_choice = int(category_choice)
             if 1 <= category_choice <= len(income_by_category):
                category = income_by_category[category_choice - 1][0]
                break
            else:
                print("Invalid input. Please enter a valid category number.")
            
        cursor.execute("SELECT amount, description, date FROM income WHERE category = ?", (category,))
        income = cursor.fetchall()
        for idx, record in enumerate(income):
            amount = record[0]
            description = record[1]
            date = record[2]
            print(f"Amount: R{amount}")
            print(f"Description: {description}")
            print(f"Date: {date}")
            
    def delete_income_category(self):
       #function to delete income by specific category
       cursor = self.conn.cursor()
       cursor.execute("SELECT DISTINCT category FROM income")
       categories = [row[0] for row in cursor.fetchall()]

       if not categories:
        print("No categories found.")
        return

       while True:
        print("Available categories:")
        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

        category_index_input = input("Enter the index of the category to delete: ")
        if not category_index_input.isdigit():
            print("Invalid input. Please enter a valid category index.")
            continue

        category_index = int(category_index_input)
        if category_index < 1 or category_index > len(categories):
            print("Invalid category index. Please enter a valid index.")
            continue
        category_to_delete = categories[category_index - 1]

        deletion_completed = False
        while not deletion_completed:
            confirm_delete = input(f"Are you sure you want to delete category '{category_to_delete}'? (yes/no): ").lower()
            if confirm_delete == "yes":
                self.conn.execute("DELETE FROM income WHERE category = ?", (category_to_delete,))
                self.conn.commit()
                print("Category deleted successfully.")
                deletion_completed = True
            elif confirm_delete == "no":
                print("Category deletion canceled.")
                return
            else:
                print("Invalid input. Please enter either 'yes' or 'no'.")
                continue

        break  # Exit the loop after successful deletion or cancellation 

    
    def load_budgets(self):
          # Load budgets from the database and store them in the budgets dictionary
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, amount FROM budgets")
        rows = cursor.fetchall()
        for category, amount in rows:
            self.budgets[category] = amount

    def set_budget_for_category(self):
        # Function to set a budget for a specific category
        category = input("Enter category: ")
        amount_input = input("Enter budget amount: ")
        if not amount_input.replace('.', '', 1).isdigit():  # Check if input is a valid float
            print("Invalid input. Please enter a valid amount.")
            return
        amount = float(amount_input)
        self.budgets[category] = amount
        self.save_budget(category, amount)
        print("Budget set successfully.")

    def save_budget(self, category, amount):
         # Helper function to save a budget to the database
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO budgets (category, amount) VALUES (?, ?)", (category, amount))
        self.conn.commit()

    def view_budget_for_category(self):
        if not self.budgets:
         print("No budgets set.")
         return
    
        print("Available categories:")
        for index, category in enumerate(self.budgets.keys(), start=1):
         print(f"{index}. {category}")
    
        while True:
         category_index_input = input("Enter the index of the category to view the budget: ")
         if not category_index_input.isdigit():
            print("Invalid input. Please enter a valid category index.")
            continue
        
         category_index = int(category_index_input)
         if category_index < 1 or category_index > len(self.budgets):
            print("Invalid category index. Please enter a valid index.")
            continue
        
         category = list(self.budgets.keys())[category_index - 1]
         amount = self.budgets[category]
         print(f"Budget for category '{category}': R{amount:.2f}")
         break

    def load_financial_goals(self):
         # Load financial goals from the database and store them in the financial_goals dictionary
        cursor = self.conn.cursor()
        cursor.execute("SELECT description, target_amount FROM financial_goals")
        rows = cursor.fetchall()
        for description, target_amount in rows:
            self.financial_goals[description] = target_amount

    def load_expenses_as_objects(self):
        # Load financial goals from the database and store them in the financial_goals dictionary
        cursor = self.conn.cursor()
        cursor.execute("SELECT amount, category FROM expenses")
        rows = cursor.fetchall()
        self.expenses = [Expense(amount, category) for amount, category in rows]   
    

    def set_financial_goals(self):
        # Function to set financial goals
        target_amount_input = input("Enter target amount: ")
        if not target_amount_input.replace('.', '', 1).isdigit():  # Check if input is a valid float
            print("Invalid input. Please enter a valid amount.")
            return
        target_amount = float(target_amount_input)
        goal_description = input("Enter goal description: ")
        self.financial_goals[goal_description] = target_amount
        self.save_financial_goal(goal_description, target_amount)  # Save the goal to the database

    def save_financial_goal(self, description, target_amount):
         # Helper function to save a financial goal to the database
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO financial_goals (description, target_amount) VALUES (?, ?)", (description, target_amount))
        self.conn.commit()


    def view_progress_towards_goals(self):
       # Function to view progress towards financial goals
       self.load_expenses_as_objects()  # Load expenses from the database
       progress_by_goal = {}
       for goal, target_amount in self.financial_goals.items():
           progress = 0
           for expense in self.expenses:
            if expense.category in self.budgets:
                progress += expense.amount
            progress_by_goal[goal] = progress
       for goal, progress in progress_by_goal.items():
        print("Goal:", goal)
        print("Progress:", progress) 

    def calculate_budget(self):
         # Function to calculate total income, total expenses, and available budget
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM income")
        total_income = cursor.fetchone()[0]
        if total_income is None:
         total_income = 0
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0]
        if total_expenses is None:
         total_expenses = 0
        budget = total_income - total_expenses
        print("Total Income:", total_income)
        print("Total Expenses:", total_expenses)
        print("Budget:", budget)

    def close_connection(self):
         # Function to close the database connection
        self.conn.close()


def main():
# Create an instance of BudgetApp
    budget_app = BudgetApp()

    while True:
        print("\nMenu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Expenses by Category")
        print("4. Add Income")
        print("5. View Income")
        print("6. View Income by Category")
        print("7. Set Budget for a Category")
        print("8. View Budget for a Category")
        print("9. Set Financial Goals")
        print("10. View Progress Towards Financial Goals")
        print("11. Update Expense")
        print("12. Delete expense from database")
        print("13. Delete income expense from database")
        print("14. Calculate Budget")
        print("15. Quit")
       
        choice = input("Enter your choice (1-15): ")

        if choice == '1':
            budget_app.add_expense()
        elif choice == '2':
            budget_app.view_expenses()
        elif choice == '3':
            budget_app.view_expenses_by_category()
        elif choice == '4':
            budget_app.add_income()
        elif choice == '5':
            budget_app.view_income()
        elif choice == '6':
            budget_app.view_income_by_category()
        elif choice == '7':
            budget_app.set_budget_for_category()
        elif choice == '8':
            budget_app.view_budget_for_category()
        elif choice == '9':
            budget_app.set_financial_goals()
        elif choice == '10':
            budget_app.view_progress_towards_goals()
        elif choice == '11':
            budget_app.update_expense()
        elif choice == '12':
            budget_app.delete_expense_category()
        elif choice == '13':
            budget_app.delete_income_category()
        elif choice == '14':
            budget_app.calculate_budget()
        elif choice == '15':
            budget_app.close_connection()
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 15.")

        while True:
            another_action = input("Would you like to perform another action? (yes/no): ").lower()
            if another_action == 'yes':
                break
            elif another_action == 'no':
                print("Exiting the program. Goodbye!")
                budget_app.close_connection()
                return
            else:
                print("Invalid input. Please enter either 'yes' or 'no'.") 
if __name__ == "__main__":
    main() 


