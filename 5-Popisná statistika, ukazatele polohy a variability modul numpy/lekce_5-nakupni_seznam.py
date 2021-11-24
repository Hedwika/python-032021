import itertools
import pandas

shopping_lists = [
  "Potatoes;Spirits and liqueurs;Other bakery products;Confectionery products;Frozen fish;Chocolate;Cheese and curd;Margarine and other vegetable fats;Poultry;Fortified wines;Yoghurt;Fresh whole milk;Fresh or chilled fruit;Preserved milk;Other cereal products;Dried, smoked or salted fish and seafood;Sugar;Eggs;Cigarettes",
  "Rice;Margarine and other vegetable fats;Ready-made meals;Jams, marmalades and honey;Sugar;Other bakery products;Dried fruit and nuts;Other alcoholic beer;Cheese and curd;Other edible oils;Preserved milk"
]
shopping_list_pairs_df = pandas.DataFrame()
for item in shopping_lists:
  shopping_list = item.split(";")
  shopping_list_pairs = list(itertools.combinations(shopping_list, 2))
  shopping_list_pairs_df = pandas.concat([shopping_list_pairs_df,
                                          pandas.DataFrame(shopping_list_pairs)])

shopping_list_pairs_df_grouped = shopping_list_pairs_df.groupby([0,1]).size()
shopping_list_pairs_df_grouped = pandas.DataFrame(shopping_list_pairs_df_grouped)
print(shopping_list_pairs_df_grouped[shopping_list_pairs_df_grouped[0] > 1])