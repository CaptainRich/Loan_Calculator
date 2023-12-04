"""Loan Calculator
   This script acquires loan details and then computes the required monthly
   payment as well as the corresponding payment schedule."""

import datetime                         # Used to time-stamp the output file
import pathlib                          # Used for file I/O
import tkinter as tk                    # Used for GUI display
from   tkinter import filedialog as fd  # Used for the fileopen dialog
import sys                              # For try/except error processing


####################################################################################################
####################################################################################################
"""The 'LoanCalc' class acquires the loan parameters and determines the monthly payment amount."""

class LoanCalc:
    """ Initializer / Constructor"""
    def __init__( self ):
        window = tk.Tk()
        window.title( "Loan Calculator" )
        window.geometry("650x350+300+450")  # Width, Height, X position, Y position
        window.config( bg='#ebebad' )       # set the background color - light yellow

        # Setup the labels for the input fields
        tk.Label( window, text="Loan Amount:", font=('Arial,14,bold'), bg='#ebebad'
                 ).place(x=10,y=10)
        tk.Label( window, text="Annual Interest Rate (ie: 0.04):", font=('Arial,14,bold)'), bg='#ebebad' 
                 ).place( x=10, y=50 )
        tk.Label( window, text="Number of Years:", font=('Arial,14,bold)'), bg='#ebebad' 
                 ).place( x=10, y=90 )

        
        tk.Button( window, text="Output File (optional):", font=('Arial,14,bold'), 
                  command=self.select_file ).place(x=10,y=130)
        
        tk.Label(window, text="Monthly Payment:", font=('Arial,14,bold'), bg='#ebebad',
                 fg='blue' ).place(x=10,y=190)
        tk.Label(window, text="Total Payment:", font=('Arial,14,bold'), bg='#ebebad',
                 fg='blue' ).place(x=10,y=230)

        # Define the actual input fields and their corresponding variables
                
        self.loanamountVar=tk.StringVar()
        tk.Entry( window, textvariable=self.loanamountVar, font=('Arial,14,bold') 
                 ).place(x=230,y=10)
        
        self.annualinterestVar = tk.StringVar()
        tk.Entry( window, textvariable=self.annualinterestVar, font=('Arial,14,bold')
                 ).place(x=230,y=50)
        
        self.numberofyearsVar = tk.StringVar()
        tk.Entry( window, textvariable=self.numberofyearsVar, font=('Arial,14,bold') 
                 ).place(x=230,y=90)

        
        # Acquire the output file path names.  The output will bet to a text file as well as
        # to a CSV file, both in the same directory.  The default directory is the current
        # working directory where the script is invoked.
        self.outpathVar = tk.StringVar()
        tk.Entry( window, textvariable= self.outpathVar, font=('Arial,14,bold'), width=40,
                 ).place(x=230,y=130) 

        # Define the output fields and their corresponding variables
        self.monthlypaymentVar = tk.StringVar()
        tk.Label( window, textvariable=self.monthlypaymentVar, font=('Arial,14,bold'),
                 bg='#ebebad' ).place(x=230,y=190)
        
        self.totalpaymentVar=tk.StringVar()
        tk.Label( window, textvariable=self.totalpaymentVar, font=('Arial,15,bold'),
                 bg='#ebebad' ).place(x=230,y=230)

        # Finally define the activation/go button to invoke the action
        tk.Button( window, text="Calculate", font=('Arial,14,bold'), command=self.calculate_loan 
                  ).place(x=230,y=270)
        
        self.monthly_payment = 0.0        # Default value


        # Start the 'event' loop
        window.mainloop()



    ##############################################################################################
    def calculate_loan( self ):
        """Compute the monthly payment and the total loan repayment amount.  Also,
           verify there is sufficient input data defined before attempting the
           computations. """
        try:
            loan_amount = float(self.loanamountVar.get())
        except ValueError:
            self.loanamountVar.set( f"Invalid loan amount!" )

        try:
            monthly_interest_rate = float(self.annualinterestVar.get()) / 12.
        except ValueError:
            self.annualinterestVar.set( f"Invalid interest rate!" )

        # Make sure the interest rate is a decimal value less than 1.0
        if( monthly_interest_rate >= 1.0/12. ):
            print( "Invalid interest rate specified, must be less than 1.0." )
            exit()

        try:
            num_years = int(self.numberofyearsVar.get())
        except ValueError:
            self.numberofyearsVar.set( f"Invalid number of years!" )

        # Now verify the data makes sense
        test_value = loan_amount * monthly_interest_rate * num_years
        if( test_value < 1.0 ):
            self.annualinterestVar.set( f"Illogical data entered" )
            self.numberofyearsVar.set( f"for one or more of these" )
            self.loanamountVar.set( f"three values!" )
            return 0

        # Perform the computations for the monthly payment.
        self.monthly_payment = self.get_monthly_payment( loan_amount, monthly_interest_rate, 
                                                    num_years )
        self.monthlypaymentVar.set( f"${self.monthly_payment:,.2f}" )

        total_payment = float( self.monthly_payment * 12 * num_years )
        self.totalpaymentVar.set( f"${total_payment:,.2f}" )



    ############################################################################################## 
    def get_monthly_payment( self, loan_amount, monthly_interest_rate, num_years ):
        """Determine the required monthly payment amount.  See reference noted in 'readme.md'"""
        num_periods = num_years * 12
        present_value = ( 1.0 - 1.0 / ( 1.0 + monthly_interest_rate )**(num_periods) )
        present_value = present_value / monthly_interest_rate
        monthly_payment = loan_amount / present_value

        return monthly_payment
    

    ############################################################################################## 
    def select_file( self ):
        """ Allow the user to select the output (file) pathname. """

        # Build the path to the current working directory to seed the fileopen dialog
        current_path = pathlib.Path.cwd()

        template = ( ("text files", "*.txt"), )
        file = fd.asksaveasfile( title='Define Output File', mode='w',
                      initialdir = current_path, filetypes = template )
        
        self.outpathVar.set( f"{file.name}" )
       



####################################################################################################
###################################################################################################
"""The 'LoanCalc' class uses the loan payment details to computes the monthly payment schedule."""

class PaymentSchedule:
    """Initializer / Constructor """
    def __init__( self, monthly_payment, loan_amount, interest_rate, number_of_years,
                 o_file ):
        
        self.monthly_payment = monthly_payment
        self.loan_amount     = loan_amount
        self.interest_rate   = interest_rate
        self.number_of_years = number_of_years
        self.o_file          = o_file


    ############################################################################################## 
    def file_headers( self ):
        """Write the loan specifics to the start of the file (header)."""

        title = '\n' + 'Loan repayment schedule' + '\n'
        o_file.write( title )

        date = datetime.datetime.now()
        title = 'Schedule created on ' + date.strftime("%A") + ' ' + date.strftime("%x") + '\n'
        o_file.write( title )

        title = 'by: Richard Ay, November 2023' + '\n\n'
        o_file.write( title )
  
        title = ' Loan Amount    : ' + ( f"${ self.loan_amount:,.2f}" ) + '\n'
        o_file.write( title )
        title = ' Interest Rate  : ' + ( f"{ interest_rate:,.2f}" ) + '\n'
        o_file.write( title )
        title = ' Period (years) : ' + ( f"{ self.number_of_years:,.2f}" ) + '\n'
        o_file.write( title )
        title = ' Monthly Payment: ' + ( f"${ self.monthly_payment:,.2f}" ) + '\n\n'
        o_file.write( title )

        # Write the column headings for the payment schedule
        title = '  Month' + '\t' + 'Begin_Balance' + '\t' + 'Payment' '\t\t' + 'Interest'  
        title = title + '\t' + 'Principal' + '\t' + 'End_Balance' '\n'
        o_file.write( title )


    ############################################################################################## 
    def payments( self ):
        """Compute and output the monthly payment schedule."""
        months = int( self.number_of_years * 12 )
        monthly_interest = self.interest_rate / 12.
        monthly_payment  = self.monthly_payment

        begin_balance = self.loan_amount          # Starting amount (balance)

        for i in range( 0, months ):
            interest            = begin_balance * monthly_interest
            principal_repayment = monthly_payment - interest
            end_balance         = begin_balance - principal_repayment

            title = (f"  {i+1}\t{begin_balance:9,.2f}\t{monthly_payment:9,.2f}")
            title = title + (f"\t{interest:9,.2f}\t{principal_repayment:9,.2f}\t")
            title = title + (f"{end_balance:9,.2f}\n")

            o_file.write( title )

            begin_balance = end_balance           # Update for next period


################################################################################################
""" Main body of the loan calculator program. """

# Invoke the loan calculator
loan = LoanCalc()

# Acquire the required loan parameters (from the LoanCalc class) to compute the payment schedule
monthly_payment = loan.monthly_payment 
if( monthly_payment < 1.0 ):
    exit()                            # In case the user aborted with no data

loan_amount     = float( loan.loanamountVar.get() )
interest_rate   = float( loan.annualinterestVar.get() )
number_of_years = float( loan.numberofyearsVar.get() )
output_file_txt = loan.outpathVar.get()


# Open the text output file and generate the payment schedule - if and only if the 
# output file was specified.

if( len(output_file_txt) > 7 ):   # 'c:\a.txt' is 8 characters
    print( "Output file name: ", output_file_txt )

    out_path = pathlib.Path( output_file_txt )
    with out_path.open( mode='w', encoding='utf-8' ) as o_file:

        # Compute and output the payment schedule
        schedule = PaymentSchedule( monthly_payment, loan_amount, interest_rate, 
                                   number_of_years, o_file )
    
        # Write the loan parameters to the output file headers.
        schedule.file_headers()
        schedule.payments()



