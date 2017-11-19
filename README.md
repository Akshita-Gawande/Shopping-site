**Objective:**

a2z e-commerce services want to launch its portal with a new look and feel. The system is to be designed with the expectation that, the number of visitors to the site per day will be around 10000+ during the upcoming bigoffersales week. The portal will have all the products (5000+ products) listed with their sale price and discounted(offer) price so that users can buy the best deals of their choosing. it is assumed that multiple users will be vying to buy the same product (whose stock is fixed), so the following constraints are placed in the system:





1. once a user shortlists/selects a deal to buy, the product is reserved for him/her for the duration of 3 minutes. 
2. if the user did not buy the selected item within 3 minutes, it is again pooled back into available deals
3. no user is allowed to buy more than 2 deals during the entire bigoffersales week
4. no user is allowed to avail more than 1000 rupees in discounted savings during the entire bigoffersales week
5. there are some "hot products" and special discounts on the "hot products" over which above rules 3 and 4 will not apply.
6. for "hot products" category, there are no restrictions in buying as well as volume of discount availed by the user
7. if a user buys any products listed in "hot products", the timeout for selected items for him/her is (Rule 1) changed to 5 minutes
8. a user is allowed to shortlist a particular product only for a maximum of 3 times (during the entire week) so that other users are not deprived of buying it.






**To run the project:**

1. First import the sql file in mysql.

2. Then make the connection changes in settings.py.

3. start the server using command- python manage.py runserver

4. Finally, open the url http://127.0.0.1:8000/shopfree/login


