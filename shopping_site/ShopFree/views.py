# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.db import connections
conn = connections['default'].cursor()
def index(request):
    
    conn.execute("SELECT * from temp")
    rows = conn.fetchall()
    return HttpResponse(str(rows))

def login(request):
	if 'logout' in request.POST:
		print "****logout"
		conn.execute("delete from user where user_id='%s'" % request.session['user_id'])
		del request.session['user_id']
	return render(request, 'login.html')

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

def products(request):
	if 'login' in request.POST:
		conn.execute("select * from user where user_id='%s'" % request.POST['user_id'])
		rows=conn.fetchall()
		if len(rows)>0:
			return HttpResponse("User Already logged In")
		else:
			request.session['user_id']=request.POST['user_id']
			conn.execute("insert into user(user_id) values(%s)" % request.session['user_id'])
			
	if 'product_id' in request.POST:
		product_id=request.POST['product_id']
		curtime=str(datetime.now())
		conn.execute("select * from products where product_id='%s' and quantity >0" %product_id)
		rows=conn.fetchall()
		if len(rows)>0:
			conn.execute("insert into Product_Cart(user_id,product_id,add_time) values('%s','%s','%s')" % (request.session['user_id'],product_id,curtime))
		else:
			return HttpResponse("Sorry!! Product Sold Out")

	conn.execute("select * from products where quantity>0")
	product_list=dictfetchall(conn)
	for product in product_list:
		curtime=str(datetime.now())
		conn.execute("select * from Product_Cart where product_id='%s' and user_id='%s' " % (product['product_id'],request.session['user_id']))
		rows=conn.fetchall()
		if len(rows)>0:
			product[b'incart']=1
		else:
			product[b'incart']=0
	conn.execute("select * from Product_Cart where user_id='%s'" % request.session['user_id'])
	return render(request, 'products.html' ,{"products":product_list,"cart_count":len(conn.fetchall())})

def cart_products(request):
	if 'buy' in request.POST:
		conn.execute("select product_id from Product_Cart where user_id='%s' and product_id in(select product_id from products where ishot=0)" % request.session['user_id'])
		rows=conn.fetchall()
		print '*******', str(len(rows))
		if len(rows)>2:
			return HttpResponse("Sorry!! You are not allowed to take more than two non hot product deals")
		else:
			conn.execute("select * from Product_Cart where user_id='%s' and product_id in (select product_id from products where quantity=0)" % request.session['user_id'])
			rows=conn.fetchall()
			if len(rows) >0:
				return HttpResponse("One or more product sold out.")
			else:
				conn.execute("update products set quantity=quantity-1 where product_id in (select product_id from Product_Cart where user_id='%s')" % request.session['user_id'])
				conn.execute("delete from Product_Cart where user_id='%s'" % request.session['user_id'])
				return HttpResponse(" Transaction Successful!! 	Thanks for purchasing")
	if 'remove' in request.POST:
		product_id=request.POST['remove']
		conn.execute("delete from Product_Cart where product_id='%s' and user_id='%s'" % (product_id,request.session['user_id']))
	curtime=str(datetime.now())
	conn.execute("delete from Product_Cart where user_id='%s' and product_id in (select product_id from products where ishot=0) and timediff('%s',add_time) > '00:03:00'" % (request.session['user_id'],curtime))
	conn.execute("delete from Product_Cart where user_id='%s' and product_id in (select product_id from products where ishot=1) and timediff('%s',add_time) > '00:05:00'" % (request.session['user_id'],curtime))
	conn.execute("select * from products where quantity>0 and product_id in (select product_id from Product_Cart where user_id='%s' )" % request.session['user_id'])
	product_list=dictfetchall(conn)
	conn.execute("select sum(discount) as total_amount from products where product_id in (select product_id from Product_Cart where user_id='%s')" % request.session['user_id'])
	total_amount=conn.fetchone()[0]
	conn.execute("select * from Product_Cart where user_id='%s'" % request.session['user_id'])
	return render(request, 'cart.html' ,{"products":product_list,"cart_count":len(conn.fetchall()),"total_amount":total_amount})












