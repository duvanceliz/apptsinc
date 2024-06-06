from django.urls import reverse
from .models import TabUnits, Tabs, Offers, Product

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
          
def print_data(units,items,sheet,project):

    units_items = []
    models =[]
    points =[]
    points_quantity = []
    sheet.cell(row=2, column=2, value='DESCRIPCIÓN')
    points_hedader = ['BI','BO','AI','AO']
    points_hedader2 = ['DI','DO','UI','AO']
    sheet.column_dimensions['A'].width = 50
    sheet.column_dimensions['B'].width = 30

    def create_column_units_items(units, items, col):
        def format_unit(unit, col):
            if col == 1:
                return f'{unit.name} -- {unit.tab.tab_name}'
            return ' '
        
        def format_item(item, col):
            if col == 1:
                return item.img.product.product_name
            elif col == 2:
                return f'{item.img.product.model} -- {item.img.product.brand}'
            elif col == 3:
                return f'{item.img.product.point}'
            elif col == 4:
                return 1
            return ' '

        column = []
        for unit in units:
            column.append(format_unit(unit, col))
            for item in items:
                if unit.pk == item.dashboard.pk:
                    column.append(format_item(item, col))
            column.append(' ')

        return column


    def print_column(data,start_row,column): 
        for i in range(0,len(data)):
            element = data[i]
            sheet.cell(row=i+start_row, column=column, value=element)
    
    def print_row(data,row,start_column):
        for i in range(0,len(data)):
            element = data[i]
            sheet.cell(row=row, column=i+start_column, value=element)

    units_items = create_column_units_items(units,items,1)
    models = create_column_units_items(units,items,2)
    points = create_column_units_items(units,items,3)
    points_quantity = create_column_units_items(units,items,4)

    # print(units_items)
    
    print_column(units_items,3,1)
    print_column(models,3,2)
    print_row(points_hedader,2,3)
    print_row(points_hedader2,2,9)
    
    print(points)
    subtotal_point_units = [0]*4

    
    for i in range(0,len(points)):
        point = points[i]
        if point == 'BI':
            subtotal_point_units[0]+= points_quantity[i]
            sheet.cell(row=i+3, column=3, value=points_quantity[i])
        elif  point == 'BO':
            subtotal_point_units[1]+= points_quantity[i]
            sheet.cell(row=i+3, column=4, value=points_quantity[i])
        elif  point == 'AI':
            subtotal_point_units[2]+= points_quantity[i]
            sheet.cell(row=i+3, column=5, value=points_quantity[i])
        elif  point == 'AO':
            subtotal_point_units[3]+= points_quantity[i]
            sheet.cell(row=i+3, column=6, value=points_quantity[i])

    sub_points = [ sub_point for sub_point in subtotal_point_units]
    
    print_row(sub_points,1,3)
    
    cllers = calc_controllers(sub_points, project.controller)

    if cllers:
        subtotal_point_exp = [0]*4
        cller_points = [4,3,6,3]

        for i in range(0,len(cllers)):
            controller = cllers[i]
            sheet.cell(row=i+3, column=8, value=controller.model)           
            if controller.point == 'DI14':
                subtotal_point_exp[0] += 14             
                sheet.cell(row=i+3, column=9, value=14)
            elif  controller.point == 'DO8':
                subtotal_point_exp[1] += 8
                sheet.cell(row=i+3, column=10, value=8)
            elif  controller.point == 'UI14':
                subtotal_point_exp[2] +=14
                sheet.cell(row=i+3, column=11, value=14)
            elif  controller.point == 'AO8':
                subtotal_point_exp[3] += 8
                sheet.cell(row=i+3, column=12, value=8)
            else:
                print_row(cller_points,3,9)

                

        subtotal_point_cller_exp = [ x+y for x,y in zip(subtotal_point_exp,cller_points) ]
   
        print_row(subtotal_point_cller_exp,1,9)
   