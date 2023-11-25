"""Loan Calculator
   This script acquires loan details and then computes the required monthly
   payment as well as the corresponding payment schedule."""

import tkinter as tk

class LoanCalc:
    # Initializer / Constructor
    def __init__( self ):
        window = tk.Tk()
        window.title( "Loan Calculator" )
        window.geometry("500x300+300+450")  # Width, Height, X position, Y position
        window.config( bg='#f0e6c2' )       # set the background color - light yellow

        # Setup the labels for the input fields
        tk.Label( window, text="Annual Interest Rate (ie: 0.04):", font=('Arial,14,bold)'), bg='#f0e6c2' 
                 ).place( x=10, y=10 )
        tk.Label( window, text="Number of Years:", font=('Arial,14,bold)'), bg='#f0e6c2' 
                 ).place( x=10, y=50 )
        tk.Label( window, text="Loan Amount:", font=('Arial,14,bold'), bg='#f0e6c2'
                 ).place(x=10,y=90)
        tk.Label(window, text="Monthly Payment:", font=('Arial,14,bold'), bg='#f0e6c2',
                 fg='blue' ).place(x=10,y=150)
        tk.Label(window, text="Total Payment:", font=('Arial,14,bold'), bg='#f0e6c2',
                 fg='blue' ).place(x=10,y=190)

        # Define the actual input fields and their corresponding variables
        self.annualinterestVar = tk.StringVar()
        tk.Entry( window, textvariable=self.annualinterestVar, font=('Arial,14,bold')
                 ).place(x=230,y=10)
        
        self.numberofyearsVar = tk.StringVar()
        tk.Entry( window, textvariable=self.numberofyearsVar, font=('Arial,14,bold') 
                 ).place(x=230,y=50)
        
        self.loanamountVar=tk.StringVar()
        tk.Entry( window, textvariable=self.loanamountVar, font=('Arial,14,bold') 
                 ).place(x=230,y=90)

        # Define the output fields and their corresponding variables
        self.monthlypaymentVar = tk.StringVar()
        tk.Label( window, textvariable=self.monthlypaymentVar, font=('Arial,14,bold'),
                 bg='#f0e6c2' ).place(x=230,y=150)
        
        self.totalpaymentVar=tk.StringVar()
        tk.Label( window, textvariable=self.totalpaymentVar, font=('Arial,15,bold'),
                 bg='#f0e6c2' ).place(x=230,y=190)

        # Finally define the activation/go button to invoke the action
        tk.Button( window, text="Calculate", font=('Arial,14,bold'), command=self.calculate_loan 
                  ).place(x=180,y=240)

        # Start the 'event' loop
        window.mainloop()



    # Compute the total loan repayment amount.
    def calculate_loan( self ):
        monthlypayment = self.get_monthly_payment( float(self.loanamountVar.get()),
            float(self.annualinterestVar.get()) / 12, int(self.numberofyearsVar.get()))

        self.monthlypaymentVar.set(format(monthlypayment, '10.2f'))
        totalpayment = float(self.monthlypaymentVar.get()) * 12 * int(self.numberofyearsVar.get())

        self.totalpaymentVar.set(format(totalpayment, '10.2f'))



    # Determine the required monthly payment amount.
    def get_monthly_payment( self, loan_amount, monthly_interest_rate, num_years ):
        monthly_payment = loan_amount * monthly_interest_rate / ( 1.0 - 1.0 / ( 1.0 + 
                          monthly_interest_rate )**(num_years*12))
        return monthly_payment



################################################################################################
# Invoke the loan calculator

loan = LoanCalc()
