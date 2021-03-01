from config import keys
import scraper
import time
import neweggBot

start = time.perf_counter()

all_products = scraper.search_newegg(keys["search_term"])

filtered_products = []
count = 1
for product in all_products:
    print(f'{count}. {product[0]}')
    count += 1
    if scraper.filter_products(product[0]):
        filtered_products.append(product)


print(f'ALL PRODUCTS SIZE: {len(all_products)}')

filtered_products.sort(key=lambda x: x[1])

cheapest_product = filtered_products[0]

print(f'\nCheapest product found:')
print(cheapest_product[0])
print(cheapest_product[1])
print(cheapest_product[2])

print("Sorted Array: ")
scraper.print_list(filtered_products)

for item in filtered_products:
    if scraper.check_stock(item[2]):
        try:
            neweggBot.buy(item[2], keys)
            break
        except:
            print(f'Failed to buy {item[0]}')
            pass
    else:
        print(f'NOT IN STOCK: {item[0]}')

finish = time.perf_counter()
print(f'\nProgram finished in {round(finish, 2)} seconds.')
