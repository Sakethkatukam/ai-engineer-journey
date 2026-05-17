import argparse
import json
from pathlib import Path
from datetime import date
from typing import Optional

#--------File path--------------
DATA_FILE=Path(__file__).parent / "expenses.json"

#------Data Layer---------------

def load_expenses() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    
def save_expenses(expenses: list[dict])->None:
    DATA_FILE.write_text(json.dumps(expenses, indent=2) , encoding="utf-8")

#-------OOP Layer----------------
class ExpenseTracker:
    def __init__(self)->None:
        self.expenses:list[dict]=load_expenses()

    def _next_id(self)->int:
        if not self.expenses:
            return 1
        return max(e["id"] for e in self.expenses)+1

    def add(self,description:str, amount:int,category:str="general")->None:
        if amount<=0:
            print("Amount must be greater than 0")
            return

        expense={
            "id":self._next_id(),
            "date":str(date.today()),
            "description":description,
            "amount":round(amount,2),
            "category":category.lower()
        }
        self.expenses.append(expense)
        save_expenses(self.expenses)
        print(f"Added:[{expense['id']}] {description} - Rs.{amount:.2f}({category})")

    def remove(self,expense_id:int)->None:
        original_count=len(self.expenses)
        self.expenses=[e for e in self.expenses if e["id"]!=expense_id]
        if len(self.expenses)==original_count:
            print(f"No expense found with ID {expense_id}")
            return
        save_expenses(self.expenses)
        print(f"Removed expense with ID {expense_id}")

    def list(self,category:Optional[str]=None)->None:
        filtered=self.expenses
        if category:
            filtered=[e for e in self.expenses if e["category"]==category.lower()]
        
        if not filtered:
            print("No expenses found.")
            return
        
        print(f"\n{'ID':<5} {'Date':<12} {'Category':<12} {'Amount':>7}  {'Description':>15}")
        print("-" * 60)
        for e in filtered:
            print(f"{e['id']:<5} {e['date']:<12} {e['category']:<12} {e['amount']:>7.2f} {e['description']:>15}")
            print()
        
    def summary(self,month:Optional[str]=None)->None:
        filtered=self.expenses
        label ="all time"

        if month:
            filtered=[e for e in self.expenses if e["date"].startswith(month)]
            label=f"month {month}"

        if not filtered:
            print(f"No expenses found for {label}.")
            return

        total=sum(e["amount"] for e in filtered)

        by_category:dict[str,float]={}
        for e in filtered:
            by_category[e["category"]]=by_category.get(e["category"],0)+e["amount"]
        print(f"\nSummary for {label}:")
        print("-"*30)
        for cat,amt in by_category.items():
            print(f" {cat:<15} Rs.{amt:>7.2f}")
        print("-"*30)
        print(f" {'Total':<15} Rs.{total:>7.2f}\n")


#-----CLI Inteface---------
def build_parser()->argparse.ArgumentParser:
    parser=argparse.ArgumentParser(
        prog="expense_tracker",
        description="Personal Expense Tracker CLI"
    )
    subparsers=parser.add_subparsers(dest="command",required=True)
    
    #add
    add_p=subparsers.add_parser("add", help="Add a new expense")
    add_p.add_argument("--description","-d",required=True)
    add_p.add_argument("--amount","-a",required=True,type=float)
    add_p.add_argument("--category","-c",default="General")

    #remove
    remove_p=subparsers.add_parser("remove",help="Remove expense by ID")
    remove_p.add_argument("--id",required=True,type=int)

    #list
    list_p=subparsers.add_parser("list",help="Liast all expenses")
    list_p.add_argument("--category","-c",help="Filter by category")

    #summary
    summary_p=subparsers.add_parser("summary",help="Spending summary")
    summary_p.add_argument("--month","-m",help="Filter by YYYY-MM")

    return parser

def main()->None:
    parser=build_parser()
    args=parser.parse_args()
    tracker=ExpenseTracker()

    if args.command=="add":
        tracker.add(args.description, args.amount, args.category)
    elif args.command=="remove":
        tracker.remove(args.id)
    elif args.command=="list":
        tracker.list(args.category)
    elif args.command=="summary":
        tracker.summary(args.month)

if __name__=="__main__":
    main()