import csv
#creation of the class
class Item:
    #create a list of instances that will hold all the instances of a class
    all_instanes_Item_class = []
    #creating a class attribute:
    pay_rate = 0.8 #pay rate after 20% discount

    def __init__(self, name : str, price: float, quantity=0):
        #run validations to the recieved arguments in the constructor
        assert price >=0, f"Price {price} is not greater than zero!"
        assert quantity >=0, f"Quantity {quantity} is not greater than zero!"
        #Assign to self object
        self.name_ = name
        self.price_ = price
        self.quantity_ = quantity

        #append the instance as soon as it's created
        #self is acutally instance itself every time that is being created.
        Item.all_instanes_Item_class.append(self)
    def calculate_total_price(self):
        return self.price_*self.quantity_
    def apply_discount(self):
        self.price_ = self.price_ * self.pay_rate

    @classmethod
    def instanciate_from_csv(cls):
        # write the code to read the csv file and instanciate some objects
        #use the context manager to read the item.csv file
        #with open('file_name.csv', 'permission')as f:
        #csv.DictReader(f) --> this will read our content f as a list of dictionary
        with open('items.csv', 'r')as f:
            #read the csv and convert it to a python dictionary
            reader = csv.DictReader(f)
            #convert this dictionary into a list
            items=list(reader)
        for item in items:
            print(item)
        #instantiate the object from csv
        for item in items:
            Item(
                name=item.get('name'),
                price=float(item.get('price')),
                quantity=int(item.get('quantity'))
            )
    @staticmethod
    def is_integer(num):
        #count out the float that have .0 example 5.0, 4.0
        if isinstance(num,float):
            return num.is_integer()
        elif isinstance(num,int):
            return True
        else:
            return False        
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name_}', '{self.price_}', '{self.quantity_}')"

#inherit from Item class
class phone(Item):
    all_phone_instances = []
    def __init__(self, name : str, price: float, quantity=0, broken_phones = 0):
        #call the super function to have all the attributes/methods of the parent class
        super().__init__(name, price, quantity)
        #run validations to the recieved arguments in the constructor
        assert broken_phones >=0, f"Broken Phones {broken_phones} is not greater than zero!"
        #Assign to self object
        self.broken_phones_ = broken_phones
        phone.all_phone_instances.append(self)
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name_}', '{self.price_}', '{self.quantity_}')"

#instanciating Item class
laptop1  = Item("lenovo yoga", 50000, 5)
print(f"name : {laptop1.name_} quantity : {laptop1.quantity_} price : {laptop1.calculate_total_price()}")
laptop2 = Item("jiobook", 17000, 7)
print(f"name : {laptop2.name_} quantity : {laptop2.quantity_} price : {laptop2.calculate_total_price()}")

print("\n")

#instanciating phone class
phone1_class_phone = phone("galaxy J", 14000, 5)
print(f"name : {phone1_class_phone.name_} quantity : {phone1_class_phone.quantity_} price : {phone1_class_phone.calculate_total_price()}")
phone2_class_phone = phone("iphone", 120000, 7)
print(f"name : {phone2_class_phone.name_} quantity : {phone2_class_phone.quantity_} price : {phone2_class_phone.calculate_total_price()}")

print("\n")

print("Getting all the instances of Item and phone class")
#getting all the instances of Item class
print(Item.all_instanes_Item_class)
#getting all the instances of phone class
print(phone.all_phone_instances)