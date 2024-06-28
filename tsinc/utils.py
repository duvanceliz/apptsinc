from django.urls import reverse
from .models import Tabs, Product
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
import functools
import time
import math
import openpyxl

# def get_breadcrumbs(request):
   
#     # unit = models.TabUnits.objects.get()
#     path = request.path.strip('/').split('/')
#     breadcrumbs = []
    
#     for i in range(len(path)):
#         breadcrumb_path = '/'.join(path[:i + 1])    
#         breadcrumb_name = path[i].replace('-', ' ').title()  # Puedes personalizar cómo se muestra el nombre
#         breadcrumbs.append((breadcrumb_name, '/' + breadcrumb_path))
#     return breadcrumbs
def closest_match(input_one,input_two):

    def generar_combinaciones(num_ui, num_co, bo, bi, ao):
        combinaciones = []
        # Combinaciones de UI (longitud num_ui)
        for ai_count in range(num_ui + 1):  # 0 to num_ui
            bi_count = num_ui - ai_count
            # Combinaciones de CO (longitud num_co)
            for ao_count in range(num_co + 1):  # 0 to num_co
                bo_count = num_co - ao_count
                combinacion = [ai_count, bi_count + bi, ao_count + ao, bo_count + bo]
                combinaciones.append(combinacion)
        return combinaciones


    # Paso 2: Calcular la distancia entre combinaciones
    def calcular_distancia(combinacion, entrada):
        distancia = 0
        for i in range(len(combinacion)):
            distancia += abs(combinacion[i] - entrada[i])
        return distancia

    # Paso 3: Encontrar la combinación más cercana
    def encontrar_combinacion_mas_cercana(combinaciones, entrada):
        mejor_combinacion = None
        menor_distancia = float('inf')
        for combinacion in combinaciones:
            distancia = calcular_distancia(combinacion, entrada)
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_combinacion = combinacion
        return mejor_combinacion


    # Generar combinaciones desde el arreglo con UI y CO
    num_ui = input_one[0]  # Total UI
    num_co = input_one[4]  # Total CO
    bo = input_one[3]  # Total BO
    bi = input_one[1]
    ao = input_one[2]

    combinaciones_posibles = generar_combinaciones(num_ui, num_co,bo,bi,ao)

    return encontrar_combinacion_mas_cercana(combinaciones_posibles, input_two)

def sort_list_point(points):
    point_list = [0]*5
    for point in points:
        if len(point) == 3:
            point = f"0{point}"   
        if point[2:4] == "AI" or point[2:4] == "UI":
            point_list[0] = int(point[:2])
        elif point[2:4] == "BI" or point[2:4] == "DI":
            point_list[1] = int(point[:2])
        elif point[2:4] == "AO":
            point_list[2] = int(point[:2])
        elif point[2:4] == "BO" or point[2:4] == "DO":
            point_list[3] = int(point[:2]) 
        elif point[2:4] == "CO":
            point_list[4] = int(point[:2]) 
    return point_list 

def clean_points(points):
    return [max(point,0) for point in points]

def subtract_points(a, b):
    return [x - y for x, y in zip(a, b)]

def add_points(*args):
    return [sum(values) for values in zip(*args)]

def find_expansion(total_points,controller_and_expansions,expansions):
    def calc_distance(input_one,input_two):
        distance = 0
        for i in range(len(input_one)):
            distance += abs(input_one[i] - input_two[i])
        return distance
    
    expansion_choice = None
    shoter_distance = float('inf')
    points = [ item['points'] for item in controller_and_expansions]
    add_p = add_points(*points)
    for expansion in expansions:
        cller_exp_point = add_points(expansion['points'],add_p) 
        # print(f"{expansion['points']}+{add_p} result:{cller_exp_point}")
        new_cller_exp_point = closest_match(cller_exp_point,total_points)
        expansion['ce_basic_points'] = new_cller_exp_point
        distance = calc_distance(new_cller_exp_point, total_points)
        #print(total_points, f"todo:{new_cller_exp_point}{expansion['model']}:{distance}")
        if distance < shoter_distance:
            shoter_distance = distance
            expansion_choice = expansion
    return expansion_choice
        

def calc_controllers(item_points, type_controller):
    
    def iterator_function(total_points,filtered_expansions):
        expansion = find_expansion(total_points,controller_and_expansions,filtered_expansions)
        controller_and_expansions.append(expansion)
        new_points = subtract_points(total_points, expansion['ce_basic_points'])
        return new_points
    
    def filter_expansions(total_points,expansions):
        # total_points = clean_points(total_points)
        prom = 15
        reduce_points = functools.reduce(lambda x,y:x+y,total_points)
        if reduce_points <= prom:
            filtered_expansions = [expansion for expansion in expansions if expansion['total_points'] <= prom]
        elif reduce_points > prom:
            filtered_expansions = [expansion for expansion in expansions if expansion['total_points'] > prom]
        return filtered_expansions
        
    
    def add_expansion_js(total_points,expansions):
        stop=0
        filtered_expansions = filter_expansions(total_points, expansions)
        new_points = iterator_function(total_points,filtered_expansions)
        while any( point > 0 for point in new_points):
            stop +=1
            filtered_expansions = filter_expansions(new_points, expansions)
            new_points = iterator_function(total_points,filtered_expansions)
            if stop > 10:
                print(new_points)
                break
                
     
            
    def add_expansion_controllers(new_points, expansions):
        for expansion in expansions:
            if expansion['model'] == 'VMQ-02D13':
                add_expansion(expansion, new_points, 3, 8)
            elif expansion['model'] == 'PJ-E08A1':
                add_expansion(expansion, new_points, 2, 8)
            elif expansion['model'] == 'VMQ-30U13':
                add_expansion_ui14(expansion, new_points, 0, 1, 14)
    

    def add_expansion(expansion, new_points, index, limit):
        while new_points[index] > 0:
            controller_and_expansions.append(expansion)
            new_points[index] -= limit

    def add_expansion_ui14(expansion, new_points, index1, index2, limit):
        new_points = clean_points(new_points)
        sum_bi_ai = new_points[index1] + new_points[index2]
        while sum_bi_ai > 0:
            controller_and_expansions.append(expansion)
            sum_bi_ai -= limit
            

    controller_and_expansions = []
    if type_controller == 'LG BECON CONTROLLER':
        controller = Product.objects.get(code='C-LG')
        expansions = Product.objects.filter(code__icontains='E-LG')
        controller_lg = {
            'is_controller':True,
            'model':controller.model,
            'points':sort_list_point(controller.point.split("-"))
        }
        expansions_lg = [{
            'is_controller':False,
            'model':expansion.model,
            'points':sort_list_point(expansion.point.split("-")) 
        }
        for expansion in expansions   
        ]

        point_quantity = functools.reduce(lambda x,y: x+y,item_points)

        if point_quantity > 0:
            controller_points = controller_lg['points']
            if all(item <= controller for item, controller in zip(item_points, controller_points)):
                controller_and_expansions.append(controller_lg)
            else:
                controller_and_expansions.append(controller_lg)
                new_points = subtract_points(item_points, controller_points)
                add_expansion_controllers(new_points, expansions_lg)
    
    elif type_controller == 'JCI FACILITY EXPLORER':
        controllers = Product.objects.filter(code="C-JS")
        expansions = Product.objects.filter(code='E-JS')
        # print(expansions)
        controllers_js = [{
            'is_controller':True,
            'model':controller.model,
            'points':sort_list_point(controller.point.split("-")) 
        }
        for controller in controllers   
        ]
        expansions_js = [{
            'is_controller':False,
            'model':expansion.model,
            'points':sort_list_point(expansion.point.split("-")),
            'total_points': functools.reduce(lambda x,y: x+y,sort_list_point(expansion.point.split("-")))
        }
        for expansion in expansions  
        ]
        

        point_quantity = functools.reduce(lambda x,y: x+y,item_points)
    
        if point_quantity > 0 and point_quantity < 18:
            controller = [controller for controller in controllers_js if controller['model']=="CGM04060"][0]  
            new_controller_point = closest_match(controller['points'],item_points)
            
            #print(f'puntos controlador:{new_controller_point}')
            if all(item <= controller for item, controller in zip(item_points, new_controller_point)):
                controller_and_expansions.append(controller)
            else:
                controller_and_expansions.append(controller)
                # new_points = subtract_points(item_points, new_controller_point)
                add_expansion_js(item_points,expansions_js)
        else:
            controller = [controller for controller in controllers_js if controller['model']=="CGM09090"][0]  
            new_controller_point = closest_match(controller['points'],item_points)
            
            # print(f'puntos controlador:{new_controller_point}')
            if all(item <= controller for item, controller in zip(item_points, new_controller_point)):
                controller_and_expansions.append(controller)
            else:
                controller_and_expansions.append(controller)
                # new_points = subtract_points(item_points, new_controller_point)
                add_expansion_js(item_points,expansions_js)
       
    # elif type_controller == 'JCI METASYS':
    #     pass

    return controller_and_expansions



def print_data(data,tab,sheet,project):
    
    
    
    thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
            )
    
     
    def print_title(title,coor,opt):
        if opt == 1:
            cell = sheet[coor]
            cell.value = title
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="DAD7D7", end_color="DAD7D7", fill_type="solid")
            cell.border = thin_border
        elif opt == 2:
            cell = sheet[coor]
            cell.value = title
            cell.font = Font(bold=True)
            cell.border = thin_border
        elif opt == 3:
            cell = sheet[coor]
            cell.value = title
            cell.font = Font(bold=True)


        
    print_title('PUNTOS DISPONIBLES EN CONTROLES',"H4",1)
    print_title('PUNTOS PROYECTADOS',"H5",1)
    print_title('PUNTOS SOBRANTES',"H6",1)

    print_title('<==',"G4",3)
    print_title('<==',"G5",3)
    print_title('<==',"G6",3)

    print_title('DESCRIPCIÓN',"B8",1)
    print_title('PROYECTO',"A2",1)
    print_title('SISTEMA',"A3",1)
    print_title('NOTAS TIPO DE SENSOR / ACTUADOR',"H8",1)
    print_title(f'{project.name.upper()}',"B2",2)
    print_title(f'{sheet.title}',"B3",2)

    points_header = ['EA','ED','SA','SD']
    points_header_cllers_exp = ['EU','ED','SA','SD','SC']
    cell_dimension = ['C','D','E','F']

    sheet.column_dimensions['B'].width = 50
    sheet.column_dimensions['A'].width = 10
    sheet.column_dimensions['H'].width = 50
    sheet.column_dimensions['G'].width = 4
    sheet.column_dimensions['L'].width = 25

    for cell in cell_dimension:
        sheet.column_dimensions[f'{cell}'].width = 5
        

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
    
    def print_leftover_point(data,row,start_column):
        for i in range(0,len(data)):
            element = data[i]
            cell = sheet.cell(row=row, column=i+start_column, value=element)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="90D473", end_color="90D473", fill_type="solid")
            cell.border = thin_border
            
        
    
    def print_column_header(data,row,start_column):
        for i in range(0,len(data)):
            element = data[i]
            cell = sheet.cell(row=row, column=i+start_column, value=element)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="DAD7D7", end_color="DAD7D7", fill_type="solid")
            cell.border = thin_border

    print_column_header(points_header,8,3)

    
    
    len_item = 0  
  

    for dict in units_per_tab:
        count = 0
        cell = sheet.cell(row=9+len_item, column=2, value=dict.get('unit_name'))
        cell.font = Font(bold=True)
        cell.border = thin_border
        for i,item in enumerate(dict['related_items'], start=10+len_item):
            count+=1
            if item.tag != 'None':
                cell_product_name = sheet.cell(row=i, column=2, value=item.tag)
            else:
                cell_product_name = sheet.cell(row=i, column=2, value=item.img.product.product_name)
            cell_description = sheet.cell(row=i, column=8, value= f'{item.img.product.model} - {item.img.product.brand}')
            points = item.img.product.point.split("-")
            for c,point in enumerate(sort_list_point(points)[0:4], start=3):
                if point != 0: 
                    cell = sheet.cell(row=i, column=c, value=point)
                    cell.font = Font(bold=True, color="FF0000")
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                    cell.border = thin_border
                     
            cell_index = sheet.cell(row=i, column=1, value=count)
            cell_product_name.border = thin_border
            cell_index.border = thin_border
            cell_description.border = thin_border
            cell_description.fill = PatternFill(start_color="FEFE7A", end_color="FEFE7A", fill_type="solid")
            cell_index.font = Font(bold=True)

        len_item += len(dict.get('related_items')) + 1 
            
    def count_point(col):
        sum = 0
        for cell in sheet[col]:
            if isinstance(cell.value, (int, float)):  # Asegurarse de que los valores sean numéricos
                sum += cell.value
        return sum
    def count_point_column(row, start, end):
        total_sum = 0
        for col in range(start, end):  # M es la columna 13 y Q es la columna 17
            cell = sheet.cell(row=row, column=col)
            if isinstance(cell.value, (int, float)):  # Asegurarse de que los valores sean numéricos
                total_sum += cell.value
        return total_sum


    points = [count_point("C"),
              count_point("D"),
              count_point("E"),
              count_point("F")]

    print_title(points[0],"C5",2)
    print_title(points[1],"D5",2)
    print_title(points[2],"E5",2)
    print_title(points[3],"F5",2)  
    print_title("CONTROLADOR/EXPANSIÓN","L8",1)
    print_column_header(points_header_cllers_exp,8,13)

    cllers = calc_controllers(points, tab.controller)

    if cllers:
        for i,controller in enumerate(cllers, start=9): 
            cell = sheet.cell(row=i, column=12, value=controller['model']) 
            cell.border = thin_border
            for y, point in enumerate(controller['points'],start=13):
                if point != 0:
                    cell = sheet.cell(row=i, column=y, value=point)
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                    cell.fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
                    cell.border = thin_border
          
        for i in range(9, 9+len(cllers)):
            sum_point = count_point_column(i,13,18)
            cell = sheet.cell(row=i, column=18, value=sum_point)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            

        points_cller_exp = [count_point("M"),
                    count_point("N"),
                    count_point("O"),
                    count_point("P"),
                    count_point("Q")]
        
        new_points_cller_exp = closest_match(points_cller_exp,points)
       
        print_title(new_points_cller_exp[0],"C4",2)
        print_title(new_points_cller_exp[1],"D4",2)
        print_title(new_points_cller_exp[2],"E4",2)
        print_title(new_points_cller_exp[3],"F4",2)  
                
        leftover_points = [ x-y for x,y in zip(new_points_cller_exp,points) ]

        print_leftover_point(leftover_points,6,3)
   
        
   