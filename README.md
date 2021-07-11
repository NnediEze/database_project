# database_proj
Angel and Nnedi's database, modeling a clothing brand called Aline 

PostgreSQL account: nme2117

url of web application: http://35.196.160.128:8111/

Description: we implented all parts of our original proposal. Please note the following changes we made:
- We should probably include a trigger that adds a certain amount to the total paid on an order after the shipping type is inserted into shipping_info. For instance +5.99 for standard shipping, +12.99 for express shipping, and +19.99 for international shipping
- Billing info is a weak entity of card rather than payment
- In order to keep track of the referral system (who used someone’s code, how much money did they get off, and how many points does the referrer get from that person), we will add the following to payment: “discount_applied” which will be in a dollar amount and  “member_code” which comes from the customer whose member discount code that person used 
- Create a trigger that adds the discount_applied amount to the referrer’s referral_points. The member_code’s in this tuple will be from the member_code’s in the “referral” entity and can be null if no discount was applied
- Create trigger that adds the customer ID of any person who uses the referrer’s discount code to the referrer’s “referee” list (referees are the customers that were referred by the referrer)
- We need a check where before someone can use a discount code (from a member), we check that they have 0 previous orders—> meaning that only new customers can use a discount referral codes
- Emails are unique to customer— when a customer makes an order, they have to put their email address, so this way we know if a customer is a repeat or not
- Make member_code an attribute of customer, and the relationship will reference member_code (foreign key)

Implementations from Part 1: 
We implemented the analytical components for the datbase such that yhe use of the site would be to derive analytics information about total sales and total orders. You can also compare compare sales in store versus online and register new employees.

Two web pages:
The inventory webpage is interesting because it functions very similiar because it required us to categorize each of the products, and also group products by the stores they are available in, and how much of each product category is available at each store. This would be very useful informaiton for inventory plannnig such as scheduling a restock for certain products and seeing what is selling out at each store. We also have financial statements which collects info on how much money we've made and how, as well we can search for customers by location to see where the store is most popular. This can help us compare if the popularity of the online store versus some the of the physical locations.
