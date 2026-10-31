from django.shortcuts import render,redirect,get_object_or_404
from django.core.files.base import ContentFile
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import Mobiles
from.models import Laptops
from .models import Shoes,Furniture,Kitchen,Shirt,Television,Jeans,Formal_Shoes,Rice_cookers,Table,Beauty,AddToCart,Whishlist
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# # # # Create your views he

models={
    'mobiles': (Mobiles, 'mobile_price', 'mobile_name','mobile_image'),
    'laptops': (Laptops, 'laptop_price', 'laptop_name','laptop_image'),
    'casual_shoes': (Shoes, 'shoe_price', 'shoe_name','shoe_image'),
    'formal_shoes': (Formal_Shoes, 'shoe_price', 'shoe_name','shoe_image'),
    'shirt': (Shirt, 'shirt_price', 'shirt_name','shirt_image'),
    'television': (Television, 'television_price', 'television_name','television_image'),
    'jeans': (Jeans, 'jeans_price', 'jeans_name','jeans_image'),
    'grinders': (Kitchen, 'kitchen_price', 'kitchen_name','kitchen_image'),
    'rice_cooker': (Rice_cookers, 'rice_cooker_price', 'rice_cooker_name','rice_cooker_image'),
    'furniture': (Furniture, 'furniture_price', 'furniture_name','furniture_image'),
    'table': (Table, 'furniture_price', 'furniture_name','furniture_image'),
    'beauty': (Beauty, 'furniture_price', 'furniture_name','furniture_image'),

}

@login_required
def add_to_wishlist(request, product_type, product_id):
    Whishlist.objects.get_or_create(
        user=request.user,
        product_type=product_type,
        product_id=product_id
    )

    return redirect('view_wishlist')


@login_required
def view_wishlist(request):
    wishlist_items = Whishlist.objects.filter(user=request.user)
    data = []

    for item in wishlist_items:
        model_info = models.get(item.product_type)

        if model_info:
            model,price_field,name_field,image_field = model_info
            product = model.objects.filter(id=item.product_id).first()

            if product:
                data.append({
                    'wishlist_id': item.id,
                    'product': product,
                    'product_name': getattr(product, name_field),
                    'product_price':getattr(product,price_field),
                    'product_image':getattr(product,image_field),
                    'product_type': item.product_type,
                })

    return render(request, 'wishlist.html', {'data': data})

@login_required
def remove_from_wishlist(request, wishlist_id):
    item = get_object_or_404(
        Whishlist,
        id=wishlist_id,
        user=request.user
    )
    item.delete()

    return redirect('view_wishlist')


















@login_required
def add_cart(request,product_id,product_type):

    cart_data=AddToCart.objects.filter(user=request.user,product_id=product_id,product_type=product_type).first()

    if cart_data:
        cart_data.product_quantity+=1
        cart_data.save()
    else:
        AddToCart.objects.create(user=request.user,product_id=product_id,product_type=product_type,product_quantity=1)

    return redirect('view_cart')




@login_required

def view_cart(request):
    data=[]
    total=0
    customer_data=AddToCart.objects.filter(user=request.user)

    for i in customer_data:
        model,price_field,name_field,image_field= models[i.product_type]

        cx_product_obj=get_object_or_404(model,id=i.product_id)   #cx product object


        name=getattr(cx_product_obj,name_field)               # cx product name
        price=getattr(cx_product_obj,price_field)             #cx product price
        image=getattr(cx_product_obj,image_field)             #cx product image

        subtotal=price*i.product_quantity
        total+=subtotal

        data.append({'name':name,'price':price,'image':image,'subtotal':subtotal,'id':i.id,'quantity':i.product_quantity})
    return render(request,'cart.html',{'data':data,'total':total})



@login_required
def increase_quantity(request,cart_id):
    item=get_object_or_404(AddToCart,id=cart_id,user=request.user)
    item.product_quantity+=1
    item.save()
    return redirect('view_cart')


@login_required
def decrease_quantity(request,cart_id):
    item=get_object_or_404(AddToCart,id=cart_id,user=request.user)

    if item.product_quantity>1:
        item.product_quantity -=1
        item.save()
    return redirect('view_cart')

@login_required
def remove_cart(request,cart_id):
    item=get_object_or_404(AddToCart,id=cart_id,user=request.user)
    item.delete()
    return redirect('view_cart')


def success(request):
     return render(request,'success.html')
    


#search functionality

def search_product(request):
    # mobiles=Mobiles.objects.all()
    # laptops=Laptops.objects.all()
    query=request.GET.get('q','').strip().lower()

    if query in ['mobile','mobiles']:
        return redirect(store_mobiles)
    elif query in ['laptop','laptops']:
        return redirect(store_laptops)
    elif query in ['beauty','beauti']:
            return redirect(store_beauty)
    elif query in ['shoes','casual shoes','casualshoes']:
            return redirect(store_shoe)
    elif query in ['formalshoes','formal shoes']:
            return redirect(store_formal_shoe)
    elif query in ['furniture','furnitures']:
            return redirect(store_furniture)
    elif query in ['grinders','grinder']:
            return redirect(store_kitchen)
    elif query in ['jeans','jean']:
            return redirect(store_jean)
    elif query in ['rice cooker','rice cookers']:
            return redirect(store_rice_cooker)
    elif query in ['shirt','shirts']:
            return redirect(store_shirt)
    elif query in ['table','tabless']:
            return redirect(store_table)
    elif query in ['televisions','television','tv','tvs']:
            return redirect(store_television)
    else:
         return redirect(home)
         























def register(request):
    if request.method=='POST':
         username=request.POST.get('username')
         email=request.POST.get('email')
         password=request.POST.get('password')

         if User.objects.filter(username=username).exists():
              messages.error(request,'username already exists')
              return redirect('register')
         else:
              User.objects.create_user(username=username,email=email,password=password)
              messages.success(request,'Registration success')
              return redirect('login')
    return render(request,'register.html')


def user_login(request):
    if request.method=='POST':

         username=request.POST.get('username')
         password=request.POST.get('password')

         user=authenticate(request,username=username,password=password)
         if user is not None:
              login(request,user)
              return redirect('home')
         else:
              messages.error(request,'Invalid username or password')
              return render(request,'login.html')
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')
              







    return render(request,'register.html')



def home(request):
    return render(request,'home.html')



def store_mobiles(request):
    data=Mobiles.objects.all()
    return render(request,'mobiles.html',{'data':data})


def store_laptops(request):
    data=Laptops.objects.all()
    return render(request,'laptops.html',{'data':data})

def store_furniture(request):
    return render(request,'furniture.html')


def store_television(request):
    data=Television.objects.all()
    return render(request,'television.html',{'data':data})

def store_shirt(request):
    data=Shirt.objects.all()
    return render(request,'shirt.html',{'data':data})

def store_jean(request):
    data=Jeans.objects.all()
    return render(request,'jeans.html',{'data':data})

def store_beauty(request):
    data=Beauty.objects.all()
    return render(request,'beauty.html',{'data':data})


def store_shoe(request):
    data=Shoes.objects.all()
    return render(request,'casual_shoes.html',{'data':data})


def store_formal_shoe(request):
    data=Formal_Shoes.objects.all()
    return render(request,'formal_shoes.html',{'data':data})


def store_furniture(request):
    data=Furniture.objects.all()
    return render(request,'furniture.html',{'data':data})



def store_table(request):
    data=Table.objects.all()
    return render(request,'table.html',{'data':data})





def store_kitchen(request):
    data=Kitchen.objects.all()
    return render(request,'grinders.html',{'data':data})



def store_rice_cooker(request):
    data=Rice_cookers.objects.all()
    return render(request,'rice_cooker.html',{'data':data})


# ##mobiles data
# response=requests.get('https://www.flipkart.com/search?q=mobiless&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')

# data=BeautifulSoup(response.content,'html.parser')

# mobiles_names=[]
# mobiles_descriptions=[]
# mobiles_prices=[]
# filtered_prices=[]
# mobiles_reviews=[]
# mobiles_images=[]




# #names
# names=data.find_all('div',class_='RG5Slk')

# for i in names[:20]:
#     a=i.get_text()
#     mobiles_names.append(a)
# print(mobiles_names)


# # #description
# names=data.find_all('div',class_='CMXw7N')

# for i in names[:20]:
#     a=i.get_text()
#     mobiles_descriptions.append(a)
# print(mobiles_descriptions)


# # #prices
# names=data.find_all('div',class_='hZ3P6w DeU9vF')
# for i in names[:20]:
#     a=i.get_text()
#     mobiles_prices.append(a)
# for i in mobiles_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # #reviews
# names=data.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     mobiles_reviews.append(a)
# print(mobiles_reviews)




# # #images 
# names=data.find_all('img',class_='UCc1lI')
# for i in names[:20]:
#     a=i['src']
#     mobiles_images.append(a)
# print(mobiles_images)




# def store_mobiless(request):
#     for n,d,p,r,i in zip(mobiles_names,mobiles_descriptions,filtered_prices,mobiles_reviews,mobiles_images):
#         mobiles=Mobiles.objects.create(mobiles_name=n,mobiles_description=d,mobiles_price=p,mobiles_rating=r)
#         response=requests.get(i)
#         mobiles.mobiles_image.save(f'{mobiles.pk}.jpg',ContentFile(response.content),save=True)


# def store_mobiles(request):
#     data=Mobiles.objects.all()
#     return render(request,'mobiles.html',{'data':data})


















# # laptop data


# response=requests.get('https://www.flipkart.com/laptops/laptops~buybackguaranteeonlaptops/pr?sid=6bo,b5g')

# data=BeautifulSoup(response.content,'html.parser')

# laptop_names=[]
# laptop_descriptions=[]
# laptop_prices=[]
# filtered_prices=[]
# laptop_reviews=[]
# laptop_images=[]




# # # #names
# names=data.find_all('div',class_='RG5Slk')

# for i in names[:20]:
#     a=i.get_text()
#     laptop_names.append(a)
# print(laptop_names)


# # # #description
# names=data.find_all('div',class_='CMXw7N')

# for i in names[:20]:
#     a=i.get_text()
#     laptop_descriptions.append(a)
# print(laptop_descriptions)


# # # #prices
# names=data.find_all('div',class_='hZ3P6w DeU9vF')
# for i in names[:20]:
#     a=i.get_text()
#     laptop_prices.append(a)
# for i in laptop_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # # # #reviews
# names=data.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     laptop_reviews.append(a)
# print(laptop_reviews)




# # #images 
# names=data.find_all('img',class_='UCc1lI')
# for i in names[:20]:
#     a=i['src']
#     laptop_images.append(a)
# print(laptop_images)


# def store_laptop(request):
#     for n,d,p,r,i in zip(laptop_names,laptop_descriptions,filtered_prices,laptop_reviews,laptop_images):
#         laptop=Laptops.objects.create(laptop_name=n,laptop_description=d,laptop_price=p,laptop_rating=r)
#         response=requests.get(i)
#         laptop.mobiles_image.save(f'{laptop.pk}.jpg',ContentFile(response.content),save=True)



# # ## shoe data 

# response=requests.get('https://www.flipkart.com/q/shoes?p%5B%5D=facets.brand%255B%255D%3DPUMA&p%5B%5D=facets.brand%255B%255D%3DNIKE&p%5B%5D=facets.brand%255B%255D%3DADIDAS&p%5B%5D=facets.brand%255B%255D%3DREEBOK&p%5B%5D=facets.brand%255B%255D%3DRED%2BTAPE&p%5B%5D=facets.brand%255B%255D%3DCAMPUS')
# # print(response)

# review=requests.get('https://www.flipkart.com/beauty-and-grooming/hair-care-and-accessory/hair-care/shampoo/pr?sid=g9b,lcf,qqm,t36')

# rdata=BeautifulSoup(review.content,'html.parser')
# data=BeautifulSoup(response.content,'html.parser')

# shoe_names=[]
# shoe_descriptions=[]
# shoe_prices=[]
# filtered_prices=[]
# shoe_reviews=[]
# shoe_images=[]




# # #names
# names=data.find_all('div',class_='Fo1I0b')

# for i in names[:20]:
#     a=i.get_text()
#     shoe_names.append(a)
# print(shoe_names)


# # # #description
# names=data.find_all('a',class_='atJtCj')

# for i in names[:20]:
#     a=i.get_text()
#     shoe_descriptions.append(a)
# print(shoe_descriptions)


# # #prices
# names=data.find_all('div',class_='hZ3P6w')
# for i in names[:20]:
#     a=i.get_text()
#     shoe_prices.append(a)
# for i in shoe_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)



# # #reviews 
# names=rdata.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     shoe_reviews.append(a)
# print(shoe_reviews)


# # 0


# # #images 
# names=data.find_all('img',class_='MZeksS')
# for i in names[:20]:
#     a=i['src']
#     shoe_images.append(a)
# print(shoe_images)


# def store_shoe(request):
#     for n,d,p,r,i in zip(shoe_names,shoe_descriptions,filtered_prices,shoe_reviews,shoe_images):
#         shoe=Shoes.objects.create(shoe_name=n,shoe_description=d,shoe_price=p,shoe_rating=r)
#         response=requests.get(i)
#         shoe.shoe_image.save(f'{shoe.pk}.jpg',ContentFile(response.content),save=True)
    # return HttpResponse('SUCCESS')





# #furniture data

# response=requests.get('https://www.flipkart.com/search?q=furniture+home+bed&sid=wwe%2C7p7%2C4yf&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_7_sc_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_7_sc_na_na&as-pos=2&as-type=RECENT&suggestionId=furniture+home+bed%7CBeds&requestId=7773c94d-a9d7-4a1c-8fd8-94c79161ad92&as-searchtext=furnuti&page=2')
# print(response)
# data=BeautifulSoup(response.content,'html.parser')

# furniture_names=[]
# furniture_descriptions=[]
# furniture_prices=[]
# filtered_prices=[]
# furniture_reviews=[]
# furniture_images=[]




# # # #names
# names=data.find_all('a',class_='pIpigb')

# for i in names[:20]:
#     a=i.get_text()
#     furniture_names.append(a)
# print(furniture_names)


# # # #description
# names=data.find_all('div',class_='U_GKRr')

# for i in names[:20]:
#     a=i.get_text()
#     furniture_descriptions.append(a)
# print(furniture_descriptions)


# # # #prices
# names=data.find_all('div',class_='hZ3P6w')
# for i in names[:20]:
#     a=i.get_text()
#     furniture_prices.append(a)
# for i in furniture_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # # # #reviews
# names=data.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     furniture_reviews.append(a)
# print(furniture_reviews)




# # #images 
# names=data.find_all('img',class_='UCc1lI')
# for i in names[:20]:
#     a=i['src']
#     furniture_images.append(a)
# print(furniture_images)


# def store_furniture(request):
#     for n,d,p,r,i in zip(furniture_names,furniture_descriptions,filtered_prices,furniture_reviews,furniture_images):
#         furniture=Furniture.objects.create(furniture_name=n,furniture_description=d,furniture_price=p,furniture_rating=r)
#         response=requests.get(i)
#         furniture.furniture_image.save(f'{furniture.pk}.jpg',ContentFile(response.content),save=True)
#     return HttpResponse('SUCCESS')


# response=requests.get('https://www.flipkart.com/mixerjuicergrinders/pr?sid=j9e,m38,7ek')
# # print(response)
# data=BeautifulSoup(response.content,'html.parser')

# kitchen_names=[]
# kitchen_descriptions=[]
# kitchen_prices=[]
# filtered_prices=[]
# kitchen_reviews=[]
# kitchen_images=[]




# # # #names
# names=data.find_all('div',class_='RG5Slk')

# for i in names[:20]:
#     a=i.get_text()
#     kitchen_names.append(a)
# print(kitchen_names)


# # # #description
# names=data.find_all('div',class_='CMXw7N')

# for i in names[:20]:
#     a=i.get_text()
#     kitchen_descriptions.append(a)
# print(kitchen_descriptions)


# # # #prices
# names=data.find_all('div',class_='hZ3P6w DeU9vF')
# for i in names[:20]:
#     a=i.get_text()
#     kitchen_prices.append(a)
# for i in kitchen_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # # # #reviews
# names=data.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     kitchen_reviews.append(a)
# print(kitchen_reviews)




# # #images 
# names=data.find_all('img',class_='UCc1lI')
# for i in names[:20]:
#     a=i['src']
#     kitchen_images.append(a)
# print(kitchen_images)


# def store_shirt(request):
#     for n,d,p,r,i in zip(kitchen_names,kitchen_descriptions,filtered_prices,kitchen_reviews,kitchen_images):
#         kitchen=Kitchen.objects.create(kitchen_name=n,kitchen_description=d,kitchen_price=p,kitchen_rating=r)
#         response=requests.get(i)
#         kitchen.kitchen_image.save(f'{kitchen.pk}.jpg',ContentFile(response.content),save=True)
#     return HttpResponse('SUCCESS')




# response=requests.get('https://www.flipkart.com/search?q=shirts%20for%20men%20with%20ratings&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')
# # print(response)
# data=BeautifulSoup(response.content,'html.parser')

# shirt_names=[]
# shirt_descriptions=[]
# shirt_prices=[]
# filtered_prices=[]
# # shirt_size=[]
# shirt_images=[]




# # #names
# names=data.find_all('div',class_='Fo1I0b')

# for i in names[:20]:
#     a=i.get_text()
#     shirt_names.append(a)
# print(shirt_names)


# # # #description
# names=data.find_all('a',class_='atJtCj')

# for i in names[:20]:
#     a=i.get_text()
#     shirt_descriptions.append(a)
# print(shirt_descriptions)


# # # #prices
# names=data.find_all('div',class_='hZ3P6w')
# for i in names[:20]:
#     a=i.get_text()
#     shirt_prices.append(a)
# for i in shirt_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # # # #reviews
# # names=data.find_all('span',class_='g_3iVf')

# # for i in names[:20]:
# #     a=i.get_text()
# #     shirt_size.append(a)
# # print(shirt_size)




# # #images 
# names=data.find_all('img',class_='MZeksS')
# for i in names[:20]:
#     a=i['src']
#     shirt_images.append(a)
# print(shirt_images)


# def store_shirt(request):
#     for n,d,p,i in zip(shirt_names,shirt_descriptions,filtered_prices,shirt_images):
#         shirt=Shirt.objects.create(shirt_name=n,shirt_description=d,shirt_price=p)
#         response=requests.get(i)
#         shirt.shirt_image.save(f'{shirt.pk}.jpg',ContentFile(response.content),save=True)
#     return HttpResponse('SUCCESS')

# response=requests.get('https://www.flipkart.com/search?q=television&sid=ckf%2Cczl&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_5_na_na_na&as-pos=1&as-type=RECENT&suggestionId=television%7CTelevisions&requestId=77cc3db7-21cf-4f71-9e24-fa2b5f5f9b0b&as-searchtext=telev')
# print(response)
# data=BeautifulSoup(response.content,'html.parser')

# television_names=[]
# television_descriptions=[]
# television_prices=[]
# filtered_prices=[]
# television_reviews=[]
# television_images=[]




# # # #names
# names=data.find_all('div',class_='RG5Slk')

# for i in names[:20]:
#     a=i.get_text()
#     television_names.append(a)
# print(television_names)


# # # #description
# names=data.find_all('div',class_='CMXw7N')

# for i in names[:20]:
#     a=i.get_text()
#     television_descriptions.append(a)
# print(television_descriptions)


# # # #prices
# names=data.find_all('div',class_='hZ3P6w DeU9vF')
# for i in names[:20]:
#     a=i.get_text()
#     television_prices.append(a)
# for i in television_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # # # #reviews
# names=data.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     television_reviews.append(a)
# print(television_reviews)




# # #images 
# names=data.find_all('img',class_='UCc1lI')
# for i in names[:20]:
#     a=i['src']
#     television_images.append(a)
# print(television_images)


# def store_television(request):
#     for n,d,p,r,i in zip(television_names,television_descriptions,filtered_prices,television_reviews,television_images):
#         television=Television.objects.create(television_name=n,television_description=d,television_price=p,television_rating=r)
#         response=requests.get(i)
#         television.television_image.save(f'{television.pk}.jpg',ContentFile(response.content),save=True)
#     return HttpResponse('SUCCESS')





# response=requests.get('https://www.flipkart.com/search?q=jeans&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')
# print(response)
# data=BeautifulSoup(response.content,'html.parser')

# jeans_names=[]
# jeans_descriptions=[]
# jeans_prices=[]
# filtered_prices=[]
# # shirt_size=[]
# jeans_images=[]




# # #names
# names=data.find_all('div',class_='Fo1I0b')

# for i in names[:20]:
#     a=i.get_text()
#     jeans_names.append(a)
# print(jeans_names)


# # # #description
# names=data.find_all('a',class_='atJtCj Qum9aC')

# for i in names[:20]:
#     a=i.get_text()
#     jeans_descriptions.append(a)
# print(jeans_descriptions)


# # # #prices
# names=data.find_all('div',class_='hZ3P6w')
# for i in names[:20]:
#     a=i.get_text()
#     jeans_prices.append(a)
# for i in jeans_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # # # #reviews
# # names=data.find_all('span',class_='g_3iVf')

# # for i in names[:20]:
# #     a=i.get_text()
# #     shirt_size.append(a)
# # print(shirt_size)




# # #images 
# names=data.find_all('img',class_='MZeksS')
# for i in names[:20]:
#     a=i['src']
#     jeans_images.append(a)
# print(jeans_images)


# def store_jeans(request):
#     for n,d,p,i in zip(jeans_names,jeans_descriptions,filtered_prices,jeans_images):
#         jeans=Jeans.objects.create(jeans_name=n,jeans_description=d,jeans_price=p)
#         response=requests.get(i)
#         jeans.jeans_image.save(f'{jeans.pk}.jpg',ContentFile(response.content),save=True)
#     return HttpResponse('SUCCESS')





# response=requests.get('https://www.flipkart.com/search?q=formal%20shoes&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')
# # print(response)

# review=requests.get('https://www.flipkart.com/beauty-and-grooming/hair-care-and-accessory/hair-care/shampoo/pr?sid=g9b,lcf,qqm,t36')

# rdata=BeautifulSoup(review.content,'html.parser')
# data=BeautifulSoup(response.content,'html.parser')

# shoe_names=[]
# shoe_descriptions=[]
# shoe_prices=[]
# filtered_prices=[]
# shoe_reviews=[]
# shoe_images=[]




# # #names
# names=data.find_all('div',class_='Fo1I0b')

# for i in names[:20]:
#     a=i.get_text()
#     shoe_names.append(a)
# print(shoe_names)


# # # #description
# names=data.find_all('a',class_='atJtCj')

# for i in names[:20]:
#     a=i.get_text()
#     shoe_descriptions.append(a)
# print(shoe_descriptions)


# # #prices
# names=data.find_all('div',class_='hZ3P6w')
# for i in names[:20]:
#     a=i.get_text()
#     shoe_prices.append(a)
# for i in shoe_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)



# # #reviews 
# names=rdata.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     shoe_reviews.append(a)
# print(shoe_reviews)


# # 0


# # #images 
# names=data.find_all('img',class_='MZeksS')
# for i in names[:20]:
#     a=i['src']
#     shoe_images.append(a)
# print(shoe_images)


# def store_formal_shoe(request):
#     for n,d,p,r,i in zip(shoe_names,shoe_descriptions,filtered_prices,shoe_reviews,shoe_images):
#         shoe=Formal_Shoes.objects.create(shoe_name=n,shoe_description=d,shoe_price=p,shoe_rating=r)
#         response=requests.get(i)
#         shoe.shoe_image.save(f'{shoe.pk}.jpg',ContentFile(response.content),save=True)
#     return HttpResponse('SUCCESS')





# response=requests.get('https://www.flipkart.com/search?q=rice+cooker&sid=j9e%2Cm38%2C9m9&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-type=RECENT&suggestionId=rice+cooker%7CElectric+Cookers&requestId=079ce0db-ddf3-40ad-8bb3-e887159d16b2&as-searchtext=rice%20co')
# # print(response)
# data=BeautifulSoup(response.content,'html.parser')

# rice_cooker_names=[]
# rice_cooker_descriptions=[]
# rice_cooker_prices=[]
# filtered_prices=[]
# rice_cooker_reviews=[]
# rice_cooker_images=[]




# # # #names
# names=data.find_all('a',class_='pIpigb')

# for i in names[:20]:
#     a=i.get_text()
#     rice_cooker_names.append(a)
# print(rice_cooker_names)


# # # #description
# names=data.find_all('div',class_='U_GKRr')

# for i in names[:20]:
#     a=i.get_text()
#     rice_cooker_descriptions.append(a)
# print(rice_cooker_descriptions)


# # # #prices
# names=data.find_all('div',class_='hZ3P6w')
# for i in names[:20]:
#     a=i.get_text()
#     rice_cooker_prices.append(a)
# for i in rice_cooker_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # # # #reviews
# names=data.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     rice_cooker_reviews.append(a)
# print(rice_cooker_reviews)




# # #images 
# names=data.find_all('img',class_='UCc1lI')
# for i in names[:20]:
#     a=i['src']
#     rice_cooker_images.append(a)
# print(rice_cooker_images)


# def store_rice_cooker(request):
#     for n,d,p,r,i in zip(rice_cooker_names,rice_cooker_descriptions,filtered_prices,rice_cooker_reviews,rice_cooker_images):
#         rice_cooker=Rice_cookers.objects.create(rice_cooker_name=n,rice_cooker_description=d,rice_cooker_price=p,rice_cooker_rating=r)
#         response=requests.get(i)
#         rice_cooker.rice_cooker_image.save(f'{rice_cooker.pk}.jpg',ContentFile(response.content),save=True)
#     return HttpResponse('SUCCESS')



# #beauty data 

# response=requests.get('https://www.flipkart.com/search?q=beauty&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')
# # print(response)
# data=BeautifulSoup(response.content,'html.parser')

# furniture_names=[]
# furniture_descriptions=[]
# furniture_prices=[]
# filtered_prices=[]
# furniture_reviews=[]
# furniture_images=[]




# # # #names
# names=data.find_all('a',class_='pIpigb')

# for i in names[:20]:
#     a=i.get_text()
#     furniture_names.append(a)
# print(furniture_names)


# # # #description
# names=data.find_all('div',class_='U_GKRr')

# for i in names[:20]:
#     a=i.get_text()
#     furniture_descriptions.append(a)
# print(furniture_descriptions)


# # # #prices
# names=data.find_all('div',class_='hZ3P6w')
# for i in names[:20]:
#     a=i.get_text()
#     furniture_prices.append(a)
# for i in furniture_prices:
#     catch=i.replace('₹','').replace(',','')
#     filtered_prices.append(catch)
# print(filtered_prices)





# # # # #reviews
# names=data.find_all('div',class_='MKiFS6')

# for i in names[:20]:
#     a=i.get_text()
#     furniture_reviews.append(a)
# print(furniture_reviews)




# # #images 
# names=data.find_all('img',class_='UCc1lI')
# for i in names[:20]: 
#     a=i['src']
#     furniture_images.append(a)
# print(furniture_images)


# def store_beauty(request):
#     for n,d,p,r,i in zip(furniture_names,furniture_descriptions,filtered_prices,furniture_reviews,furniture_images):
#         furniture=Beauty.objects.create(furniture_name=n,furniture_description=d,furniture_price=p,furniture_rating=r)
#         response=requests.get(i)
#         furniture.furniture_image.save(f'{furniture.pk}.jpg',ContentFile(response.content),save=True)
#     return HttpResponse('SUCCESS')
