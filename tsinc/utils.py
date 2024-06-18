from django.urls import reverse
from .models import Tabs, Product
from openpyxl.styles import Font, PatternFill, Border, Side

# def get_breadcrumbs(request):
   
#     # unit = models.TabUnits.objects.get()
#     path = request.path.strip('/').split('/')
#     breadcrumbs = []
    
#     for i in range(len(path)):
#         breadcrumb_path = '/'.join(path[:i + 1])    
#         breadcrumb_name = path[i].replace('-', ' ').title()  # Puedes personalizar cómo se muestra el nombre
#         breadcrumbs.append((breadcrumb_name, '/' + breadcrumb_path))
#     return breadcrumbs


def calc_controllers(item_points, type_controller):

    controllers_dict = {
        'VDQ-00QA2': [4,3,6,3],
    }

    def subtract_points(a, b):
        return [x - y for x, y in zip(a, b)]

    def add_expansion_controllers(new_points, expansions):
        for expansion in expansions:
            if expansion.point == 'DO8':
                add_expansion(expansion, new_points, 1, 8)
            elif expansion.point == 'AO8':
                add_expansion(expansion, new_points, 3, 8)
            elif expansion.point == 'UI14':
                add_expansion_ui14(expansion, new_points, 0, 2, 14)
        return controllers

    def add_expansion(expansion, new_points, index, limit):
        while new_points[index] > 0:
            controllers.append(expansion)
            new_points[index] -= limit

    def add_expansion_ui14(expansion, new_points, index1, index2, limit):
        sum_bi_ai = item_points[index1] + item_points[index2]
        if sum_bi_ai <= 14+6:
            controllers.append(expansion)
        else:
            while new_points[index2] > 0:
                controllers.append(expansion)
                new_points[index2] -= limit
            while new_points[index1] > 0:
                controllers.append(Product.objects.get(point='DI14'))
                new_points[index1] -= limit

    controllers = []
    if type_controller == 'LG CONTROLLER':
        controller = Product.objects.get(code='CLG')
        expansions = Product.objects.filter(code__icontains='ELG')
        controller_points = controllers_dict.get(controller.model,0)
        

        if all(item <= controller for item, controller in zip(item_points, controller_points)):
            if any(item_points):
                controllers.append(controller)
           
        else:
            controllers.append(controller)
            new_points = subtract_points(item_points, controller_points)
            controllers = add_expansion_controllers(new_points, expansions)

    return controllers
          
def print_data(data,tabs,sheet,project):
    
    
    
    thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
            )
    
     
    def print_title(title,row,col,fill):
        if fill:
            cell = sheet.cell(row=row, column=col, value=title)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="DAD7D7", end_color="DAD7D7", fill_type="solid")
            cell.border = thin_border
        else:
            cell = sheet.cell(row=row, column=col, value=title)
            cell.font = Font(bold=True)
            cell.border = thin_border
        
        
 
    print_title('DESCRIPCIÓN',7,2,True)

    print_title('PROYECTO',2,1,True)

    print_title('SISTEMA',3,1,True)
    
    print_title('NOTAS TIPO DE SENSOR / ACTUADOR',7,11,True)

    print_title(f'{project.name.upper()}',2,2,False)


    print_title(f'{sheet.title}',3,2,False)

   
    points_hedader = ['RO','EU','ED','SA','SC','SD','SR','COMM']
    points_hedader2 = ['DI','DO','UI','AO']
    cell_dimension = ['C','D','E','F','G','H','I','J']

    sheet.column_dimensions['B'].width = 50
    # sheet.column_dimensions['C'].width = 30
    sheet.column_dimensions['A'].width = 10
    sheet.column_dimensions['K'].width = 50


    for cell in cell_dimension:
        sheet.column_dimensions[f'{cell}'].width = 7
        

    units_per_tab = list(filter(lambda dict: dict['tab_name'] == f'{sheet.title}',data))

    # print(units_tab)

    def print_row(data,start_row,column): 
        for i in range(0,len(data)):
            element = data[i]
            sheet.cell(row=i+start_row, column=column, value=element)
    
    def print_column(data,row,start_column):
        for i in range(0,len(data)):
            element = data[i]
            cell = sheet.cell(row=row, column=i+start_column, value=element)
        
    
    def print_column_header(data,row,start_column):
        for i in range(0,len(data)):
            element = data[i]
            cell = sheet.cell(row=row, column=i+start_column, value=element)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="DAD7D7", end_color="DAD7D7", fill_type="solid")
            cell.border = thin_border

    print_column_header(points_hedader,7,3)

    def create_column(data):
        column = []
        for dict in data:
            for key in dict:
                if key == 'unit_name':
                    column.append(dict[key])
            for item in dict['related_items']:
                    column.append(item.img.product.product_name)
        return column
    
    len_item = 0   

    for dict in units_per_tab:
        count = 0
        cell = sheet.cell(row=9+len_item, column=2, value=dict.get('unit_name'))
        cell.font = Font(bold=True)
        cell.border = thin_border
        for i,item in enumerate(dict['related_items'], start=10+len_item):
            count+=1
            cell_product_name = sheet.cell(row=i, column=2, value=item.img.product.product_name)
            cell_description = sheet.cell(row=i, column=11, value= f'{item.img.product.model} - {item.img.product.brand}')
            cell_index = sheet.cell(row=i, column=1, value=count)
            cell_product_name.border = thin_border
            cell_index.border = thin_border
            cell_description.border = thin_border
            cell_description.fill = PatternFill(start_color="FEFE7A", end_color="FEFE7A", fill_type="solid")
            cell_index.font = Font(bold=True)

        len_item += len(dict.get('related_items')) + 1 
            

   
        
    

            
            
        

        
                
       
            
            
        
      


    # units_items = create_column_units_items(units,items,1)
    # models = create_column_units_items(units,items,2)
    # points = create_column_units_items(units,items,3)
    # points_quantity = create_column_units_items(units,items,4)

    # # print(units_items)
    
    # print_column(units_items,3,1)
    # print_column(models,3,2)
    # print_row(points_hedader,2,3)
    # print_row(points_hedader2,2,9)
    
    # # print(points)
    # subtotal_point_units = [0]*4

    
    # for i in range(0,len(points)):
    #     point = points[i]
    #     if point == 'BI':
    #         subtotal_point_units[0]+= points_quantity[i]
    #         sheet.cell(row=i+3, column=3, value=points_quantity[i])
    #     elif  point == 'BO':
    #         subtotal_point_units[1]+= points_quantity[i]
    #         sheet.cell(row=i+3, column=4, value=points_quantity[i])
    #     elif  point == 'AI':
    #         subtotal_point_units[2]+= points_quantity[i]
    #         sheet.cell(row=i+3, column=5, value=points_quantity[i])
    #     elif  point == 'AO':
    #         subtotal_point_units[3]+= points_quantity[i]
    #         sheet.cell(row=i+3, column=6, value=points_quantity[i])

    # sub_points = [ sub_point for sub_point in subtotal_point_units]
    
    # print_row(sub_points,1,3)
    
    # cllers = calc_controllers(sub_points, project.controller)

    # if cllers:
    #     subtotal_point_exp = [0]*4
    #     cller_points = [4,3,6,3]

    #     for i in range(0,len(cllers)):
    #         controller = cllers[i]
    #         sheet.cell(row=i+3, column=8, value=controller.model)           
    #         if controller.point == 'DI14':
    #             subtotal_point_exp[0] += 14             
    #             sheet.cell(row=i+3, column=9, value=14)
    #         elif  controller.point == 'DO8':
    #             subtotal_point_exp[1] += 8
    #             sheet.cell(row=i+3, column=10, value=8)
    #         elif  controller.point == 'UI14':
    #             subtotal_point_exp[2] +=14
    #             sheet.cell(row=i+3, column=11, value=14)
    #         elif  controller.point == 'AO8':
    #             subtotal_point_exp[3] += 8
    #             sheet.cell(row=i+3, column=12, value=8)
    #         else:
    #             print_row(cller_points,3,9)

                

    #     subtotal_point_cller_exp = [ x+y for x,y in zip(subtotal_point_exp,cller_points) ]
   
    #     print_row(subtotal_point_cller_exp,1,9)
   