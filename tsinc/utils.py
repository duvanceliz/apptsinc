from django.urls import reverse
from .models import TabUnits, Tabs, Offers, Product

def get_breadcrumbs(request):
   
    # unit = models.TabUnits.objects.get()
    path = request.path.strip('/').split('/')
    breadcrumbs = []
    
    for i in range(len(path)):
        breadcrumb_path = '/'.join(path[:i + 1])    
        breadcrumb_name = path[i].replace('-', ' ').title()  # Puedes personalizar cómo se muestra el nombre
        breadcrumbs.append((breadcrumb_name, '/' + breadcrumb_path))
    return breadcrumbs



# def calc_controllers(item_points,type_controller):
#         controllers = []
#         if type_controller == 'LG CONTROLLER':
#             controller = Product.objects.get(code='CLG')           
#             expansions = Product.objects.filter(code__icontains='ELG')
#             controller_points = controller.point.split(",")
#             controller_points_sort = [0]*4
            
#             for point in controller_points:
#                 if point == '4DI':
#                     controller_points_sort[0] = 4
#                 elif point == '3DO':
#                     controller_points_sort[1] = 3
#                 elif point == '6UI':
#                     controller_points_sort[2] = 6
#                 elif point == '3AO':
#                     controller_points_sort[3] = 3
#             if (item_points[0] <= controller_points_sort[0]) and (item_points[1] <= controller_points_sort[1]) and (item_points[2] <= controller_points_sort[2]) and (item_points[3] <= controller_points_sort[3]):
#                 controllers.append(controller) 
#                 return controllers  
#             else:
#                 controllers.append(controller)
#                 new_point = list(map(lambda x,y: x-y,item_points,controller_points_sort))
#                 # print(new_point)
#                 # print('son mayores')
                
#                 for expansion in expansions:
#                     if expansion.point == 'DO8':
#                         if new_point[1] <= 8 and new_point[3]>0:
#                             controllers.append(expansion)
#                         else:
#                             while(new_point[1] > 0):
#                                 new_point[1] = new_point[1] - 8
#                                 controllers.append(expansion)

#                     if expansion.point == 'AO8':
#                         if new_point[3] <= 8 and new_point[3]>0:
#                             controllers.append(expansion)
#                         else:
#                             while(new_point[3] > 0):
#                                 new_point[3] = new_point[3] - 8
#                                 controllers.append(expansion)

#                     if expansion.point == 'UI14':
#                         sum_bi_ai = item_points[0] + item_points[2]
#                         if sum_bi_ai <= 14:
#                             controllers.append(expansion)
#                         else:
#                             while(new_point[2] > 0):
#                                 new_point[2] = new_point[2] - 14
#                                 controllers.append(expansion)
            
#                             while(new_point[0] > 0):
#                                 new_point[0] = new_point[0] - 14
#                                 controllers.append(Product.objects.get(point='DI14'))    
#                 return controllers  

def calc_controllers(item_points, type_controller):
    def extract_and_sort_points(controller):
        points = controller.point.split(",")
    # Diccionario para mapear los sufijos a su posición en la lista ordenada
        position_map = {'4DI': 0, '3DO': 1, '6UI': 2, '3AO': 3}
        # Inicializar la lista ordenada con ceros
        ordered_points = [0] * 4
        
        for point in points:
            # Extraer el número y el sufijo
            num = int(''.join(filter(str.isdigit, point)))
            suffix = ''.join(filter(str.isalpha, point))
            # Crear la clave completa para mapear la posición
            key = f"{num}{suffix}"
            # Asignar el número en la posición correcta
            if key in position_map:
                ordered_points[position_map[key]] = num
    
        return ordered_points


    def subtract_points(a, b):
        return [x - y for x, y in zip(a, b)]

    def add_expansion_controllers(new_points, expansions):
        for expansion in expansions:
            if expansion.point == 'DO8':
                add_expansion(expansion, new_points, 1, 8)
            elif expansion.point == 'AO8':
                add_expansion(expansion, new_points, 3, 8)
            elif expansion.point == 'UI14':
                add_expansion_ui14(expansion, new_points)
        return controllers

    def add_expansion(expansion, new_points, index, limit):
        while new_points[index] > 0:
            controllers.append(expansion)
            new_points[index] -= limit

    def add_expansion_ui14(expansion, new_points):
        sum_bi_ai = item_points[0] + item_points[2]
        if sum_bi_ai <= 14+6:
            controllers.append(expansion)
        else:
            while new_points[2] > 0:
                controllers.append(expansion)
                new_points[2] -= 14
            while new_points[0] > 0:
                controllers.append(Product.objects.get(point='DI14'))
                new_points[0] -= 14

    controllers = []
    if type_controller == 'LG CONTROLLER':
        controller = Product.objects.get(code='CLG')
        expansions = Product.objects.filter(code__icontains='ELG')
        controller_points = extract_and_sort_points(controller)
        print(controller_points)

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
    count = 0
    count2 = 0
    sheet.cell(row=2, column=2, value='DESCRIPCIÓN')
    points_hedader = ['BI','BO','AI','AO']
    points_hedader2 = ['DI','DO','UI','AO']
    sheet.column_dimensions['A'].width = 50
    sheet.column_dimensions['B'].width = 30

    for unit in units:
        units_items.append(f'{unit.quantity}*{unit.name} -- {unit.tab.tab_name}')
        for item in items:
            if unit.pk == item.dashboard.pk:
                units_items.append(item.img.product.product_name)
        units_items.append(' ')

    for unit_item in units_items:
        count+=1
        sheet.cell(row=count+2, column=1, value=unit_item)

    for unit in units:
        models.append(' ')
        for item in items:
            if unit.pk == item.dashboard.pk:
                models.append(f'{item.img.product.model} -- {item.img.product.brand}')
        models.append(' ')
    
    for model in models:
        count2+=1
        sheet.cell(row=count2+2, column=2, value=model)

    for i in range(1,len(points_hedader)+1):
        sheet.cell(row=2, column=i+2, value=points_hedader[i-1])

    for i in range(1,len(points_hedader2)+1):
        sheet.cell(row=2, column=i+8, value=points_hedader2[i-1])    

    for unit in units:
        points.append(' ')
        points_quantity.append(' ')
        for item in items:
            if unit.pk == item.dashboard.pk:
                points.append(f'{item.img.product.point}')
                points_quantity.append(unit.quantity)
        points.append(' ')
        points_quantity.append(' ')

    subtotal_point_bi = 0
    subtotal_point_bo = 0
    subtotal_point_ai = 0
    subtotal_point_ao = 0
    for i in range(1,len(points)+1):
        point = points[i-1]
        if point == 'BI':
            subtotal_point_bi+= points_quantity[i-1]
            sheet.cell(row=i+2, column=3, value=points_quantity[i-1])
        elif  point == 'BO':
            subtotal_point_bo+= points_quantity[i-1]
            sheet.cell(row=i+2, column=4, value=points_quantity[i-1])
        elif  point == 'AI':
            subtotal_point_ai+= points_quantity[i-1]
            sheet.cell(row=i+2, column=5, value=points_quantity[i-1])
        elif  point == 'AO':
            subtotal_point_ao+= points_quantity[i-1]
            sheet.cell(row=i+2, column=6, value=points_quantity[i-1])

    sheet.cell(row=1, column=3, value=subtotal_point_bi)
    sheet.cell(row=1, column=4, value=subtotal_point_bo)
    sheet.cell(row=1, column=5, value=subtotal_point_ai)
    sheet.cell(row=1, column=6, value=subtotal_point_ao)
    points = [subtotal_point_bi,subtotal_point_bo,subtotal_point_ai,subtotal_point_ao]
    
    cllers = calc_controllers(points, project.controller)
    # print(cllers)

    
    subtotal_point_di = 0
    subtotal_point_do = 0
    subtotal_point_ui = 0
    subtotal_point_a_o = 0

    cller_points = [4,3,6,3]
    for i in range(0,len(cllers)):
        controller = cllers[i]
        sheet.cell(row=i+3, column=8, value=controller.model)
        if controller.model == 'VDQ-00QA2':
            for i in range(0,len(cller_points)):
                sheet.cell(row=3, column=i+9, value=cller_points[i])
        if controller.point == 'DI14':
            subtotal_point_di += 14             
            sheet.cell(row=i+3, column=9, value=14)
        elif  controller.point == 'DO8':
            subtotal_point_do += 8
            sheet.cell(row=i+3, column=10, value=8)
        elif  controller.point == 'UI14':
            subtotal_point_ui +=14
            sheet.cell(row=i+3, column=11, value=14)
        elif  controller.point == 'AO8':
            subtotal_point_a_o += 8
            subtotal_point_ao+= points_quantity[i-1]
    sheet.cell(row=1, column=9, value=subtotal_point_di+cller_points[0])
    sheet.cell(row=1, column=10, value=subtotal_point_do+cller_points[1])
    sheet.cell(row=1, column=11, value=subtotal_point_ui+cller_points[2])
    sheet.cell(row=1, column=12, value= subtotal_point_a_o+cller_points[3])