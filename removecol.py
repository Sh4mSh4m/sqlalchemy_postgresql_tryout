import pandas as pd

f = pd.read_csv("products.csv",sep='\t')
keep_col = ['url','product_name', 'generic_name', 'quantity', 'brands', 'categories_fr', 'main_category_fr', 'image_url', 'image_small_url', 'nutrition-score-fr_100g']
new_f = f[keep_col]
new_f.to_csv("new_product.csv",sep=';', index = False)
