import xlrd
print('hello')
loc='C:/Users/Rishabh/waterbudgeting/Coordinates_Shastrinagar.xlsx'
print('hello2')
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
uz=sheet.cell_value(1,1)
i=2
capacity_nale=0
capacity_pond=0
capacity_talav=0
capacity=0
while(i!=123):
    area=sheet.cell_value(i,1)
    structure_type=sheet.cell_value(i,4).strip()
    if(structure_type=='Nala Bund' or structure_type=='KT Weir'):
        capacity_nale=capacity_nale+(((area*2)/1000)*2)
    elif(structure_type=='Village Pond' or structure_type=='Farm Pond'):
        capacity_pond=capacity_pond+((area*3)/1000)
    elif(structure_type=='Pazhar Talav'):
        capacity_talav=capacity_talav+(((area*3)/1000)*2)
    #elif(structure_type=='Konambe dam'):
    #    capacity=1500
    i=i+1
print(capacity_talav+capacity_pond+capacity_nale+capacity)

