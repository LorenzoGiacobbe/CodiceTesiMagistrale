# Correlations
to run the code: correlations.py <desired_name_of_spreadsheet>

Takes as input a log file and generates the Correlation table for the requested Simulation

Results saved on a Excel Spreadsheet saved at ./correlations/spreadsheets/


# Osservazioni
In presenza di delay sugli input esiste una correlazione se:
-> del_NAND > del_XOR
-> max(del_a, del_b) + del_NAND > del_XOR 
	-> se del_a + del_NAND > del_XOR e del_b + del_NAND < del_XOR (-> correlazione solo con b e viceversa)
	-> se del_a + del_NAND > del_XOR e del_b + del_NAND > del_XOR (-> correlazione con entrabi gli input come nel caso senza del_input)
-> max(del_a, del_b) + del_NAND - del_XOR >= del_XOR (-> per garantire la presenza di glitch)

=> PERCHÈ IN QUESTO MODO I GLITCH SONO CAUSATI DAL CAMBIAMENTO DEGLI INGRESSI DEL NAND E NON DAI RANDOM QUINDI RISULTA UNA CORRELAZIONE CON A E B