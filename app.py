from flask import Flask, jsonify, request, render_template, redirect, send_file
from models import Warehouse

app=Flask(__name__) #створюємо веб додаток
#Ініціалізація та меню
my_warehouse=Warehouse()

# 1. Головна сторінка з інструкцією
@app.route('/')
def index():
    # Сортування
    sort_by=request.args.get('sort', 'name')
    print(f"DEBUG: Отримано запит на сортування: {sort_by}")
    items_to_display=list(my_warehouse.items)
    
    if sort_by=='price':
        items_to_display.sort(key=lambda x: x.price)
    else:
        items_to_display.sort(key=lambda x: x.name.lower())
        
    # Загальна сума
    total_val=sum(item.get_total_price() for item in items_to_display)
    return render_template('index.html', items=items_to_display, total=total_val, current_sort=sort_by)

# 2.Додати товар
@app.route('/add', methods=['POST'])
def add():
    try:
        name=request.form.get('name')
        price=float(request.form.get('price'))
        qty=int(request.form.get('quantity'))
        my_warehouse.add_product(name, price, qty)
    except(ValueError, TypeError):
        pass
    return redirect('/')

@app.route('/search')
def search():
    query=request.args.get('query', '')
    result=my_warehouse.find_product(query)

    item_to_show=[result] if result else []
    total_val = sum(item.get_total_price() for item in item_to_show)
    return render_template('index.html', items=item_to_show, total=total_val)

@app.route('/update/<name>', methods=['POST'])
def update(name):
    new_qty=int(request.form.get('quantity'))
    my_warehouse.update_quantity(name, new_qty)
    return redirect('/')

@app.route('/delete/<name>')
def delete(name):
    my_warehouse.delete_item(name)
    return redirect('/')

@app.route('/report')
def report():
    my_warehouse.generate_txt_report()
    return send_file(my_warehouse.report_path, as_attachment=True)

if __name__=='__main__':
    app.run(debug=True)