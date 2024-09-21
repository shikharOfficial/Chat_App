# Python Inheritance:
1. Single Inheritance
   - ` class Subclass(BaseClass): `
2. Multiple 
   - ` class Subclass(BaseClass1, BaseClass2, ...): `
3. Multilevel
   - ` class Subclass1(BaseClass1): and class Subclass2(Subclass1): `
4. Hierarchical
   - ` class Subclass1(BaseClass): and class Subclass2(BaseClass): `

# Mysql
**Installation Fix:**
`sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`

1. mysql -u root -p
2. SHOW DATABASES;
3. CREATE DATABASE chat_app;
4. USE chat_app;
5. SHOW TABLES;


- Check Process Id for a PORT:
`sudo lsof -t -i:6379 -> Outputs Process ID`

# Models:
1. **BigAutoField vs BigIntegerField**
- Use BigAutoField when you need an auto-incrementing primary key field for your model.
- Use BigIntegerField when you need to store large integer values but don't need auto-incrementing behavior, or when you need to customize how values are assigned to the field.
- When you define a field in a Django model as BigAutoField, Django automatically treats it as the primary key for the model.  

2. **auto_now_add vs auto_now** 
- `created_date = models.DateTimeField(auto_now_add=True) ` Automatically set to the current date and time when the object is **created**.
- `last_updated = models.DateTimeField(auto_now=True) ` Automatically updated to the current date and time when the object is **saved**.  

3. By default, all fields in Django models are required unless explicitly specified otherwise. Since you haven't specified **blank=True** for these fields, they are already required.  

4. **Set Default Value:** ` is_active = models.BooleanField(default=True) `  
  
5. `email = models.EmailField(unique=True, max_length=30, error_messages={ 'unique': "Email already exists."})`
- The unique key in the **error_messages** dictionary specifies the error message to display when a unique constraint is violated.
- In this case, if a user tries to create a new user with an email that already exists in the database, Django will raise a validation error with the message **Email already exists.**
- The error_messages dictionary provided in the EmailField definition in the Django model is specifically for handling the unique constraint validation error, not for handling the max_length constraint violation. \

6. **BigAutoField vs SmallAutoField**
- BigAutoField is a 64-bit integer field
- SmallAutoField is a 32-bit integer field.
- The range of values that can be stored in a SmallAutoField is from -32768 to 32767. \

7. **Default Table Name:** By default, Django uses the app name and the lowercase version of the model's class name as the table name (e.g., appname_modelname). \

8. `class Meta:
    managed = True
    db_table = 'tbl_login' `

- When **managed=True** (the default), Django will **create, update, and delete the database table** for the model as needed based on changes to the model's definition.
- When **managed=False**, Django assumes that the table has been **created and managed externally**, and it won't make any changes to the table's structure.
- You can use **db_table** to override the default table name and specify a custom name for the table. \

# Rest Framework:

1) Generics ::: rest_framework.generics

## ListAPIView : It is used for listing multiple instances of a model.
### Get all users                
```class UserListView(ListAPIView):
    queryset = TblUser.objects.all()
    serializer_class = UserSerializer
```
    
## RetrieveAPIView : It is used for retrieving a single instance of a model by its primary key or another unique identifier.
### Get individual user
``` class UserDetailView(RetrieveAPIView):
    queryset = TblUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
```

## RetrieveUpdateDestroyAPIView


2. APIView ::: from rest_framework.views import APIView
``` class ProductView(APIView):

    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):

        products = Product.objects.all()

        serializer = self.serializer_class(products, many=True)

        return Response(serializer.data) ```

3. *ViewSets* ::: A ViewSet is a class-based view, able to handle all of the basic HTTP requests: GET, POST, PUT, DELETE without hard coding any of the logic.
``` class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post']
```
    
- Viewset uses Routers instead of URLs
    
- *APIView vs ViewSets8 ::: [Link](https://dev.to/koladev/apiview-vs-viewsets-4ln0)

..........................................................................................................................................................

# JWT Authentication ::::: simple jwt restframework

- **settings.py** ->  *'USER_ID_FIELD': 'id'*
- This should be set to the field in your user model that uniquely identifies each user.

- When creating a refresh token
  - `refresh = RefreshToken.for_user(django_user)`, the user must be a instance of **django_user`**.

- **SOLUTION**
1. **Create User Model that inherits from AbstractBaseUser**
  - ```from django.contrib.auth.models import AbstractBaseUser
    class TblKaayaLogin(AbstractBaseUser): 
    ..........
    USERNAME_FIELD = id ```
  - Create CustomTokenObtainPairSerializer to get token and send token as response.
     Use this serializer in Login View.
    
**OR**
    
2. **Create a django_user as**
   - ``` django_user, created = User.objects.get_or_create(username = user.email)
                if created:
                    django_user.set_password(password)
                    django_user.save()
      ```
                    
- Changes in the Tables in DB:
   - A user with username and password is created in `auth_user` table.
   - Refresh Token is saved in `token_blacklist_outstandingtoken`
   
   
3. **Check For Authentication**
``` from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
```
    
4. Extract User from Request JWT ::: request.user
   
   
......................................................................................................................................................

# Serializers :::

1. ## serializer.Serializer
- With **Serializer**, you have full control over how data is serialized and deserialized. You define the fields and methods explicitly in the serializer class.
- Serializer is useful when you need to customize the serialization or deserialization process extensively, or when you're working with **non-model data**. \
  
2. ## serializer.ModelSerializer
- It automatically generates serializer fields based on the model's fields, reducing the amount of boilerplate code you need to write.

 - **Valiadate Function**
     ``` def validate(self, attrs):
         email = attrs.get('email')
         password = attrs.get('password')  
         ..........
         ```
 - The validate method is a custom validation method provided by Django REST Framework's serializer class. 
    This method is called when you invoke the `is_valid()` method on the serializer instance, and it allows you to perform additional validation on the input data beyond the field-level validation provided by the serializer's fields.
 - *attrs*
    - short for "attributes", which is a dictionary containing the validated data for all the serializer's fields.

3. ## data vs instance 
- **data**
  - When you use data, you're providing data (typically a dictionary) that you want to serialize into a specific format defined by the serializer.

``` data_to_serialize = {'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}
serializer_with_data = MyModelSerializer(data=data_to_serialize)
serializer_with_data.is_valid()  # Validate the data
serialized_data = serializer_with_data.validated_data  # Get validated data
```

- **instance**
  -  When you use instance, you're providing an instance of a Django model or queryset that you want to serialize into a specific format.

``` instance = MyModel.objects.get(pk=1)  # Retrieve instance from database
serializer_with_instance = MyModelSerializer(instance=instance)
serialized_data = serializer_with_instance.data  # Get serialized data
``` 

.................................................................................................................................

# MVC vs MVT :::

## MVC (Model-View-Controller):

### Model: 
- Represents the data or business logic of the application. It encapsulates the data and behavior of the application's domain, including data validation, manipulation, and access.

### View: 
- Represents the presentation layer of the application.
- It's responsible for rendering the user interface based on the data from the model. Views are typically the HTML templates in web applications.

### Controller: 
- Acts as an intermediary between the model and the view.
- It receives user input (e.g., HTTP requests in web applications), processes that input (interacting with the model), and determines the appropriate response (rendering the view). Controllers handle the application logic and flow control.


## MVT (Model-View-Template):

### Model: 
- Similar to MVC, the model represents the data or business logic of the application.
- It defines the structure and behavior of the application's data.

### View: 
- In MVT, the view is responsible for presenting data to the user.
- However, in the context of Django (a web framework that follows the MVT pattern), the view is more like the controller in MVC.
- It receives HTTP requests, interacts with the model to retrieve data or perform operations, and returns an HTTP response (often rendered HTML content).

### Template: 
- Templates in MVT are similar to views in MVC.
- They represent the presentation layer and define the structure and appearance of the user interface.
- Templates in Django are typically HTML files with embedded template tags and expressions that dynamically generate content based on data provided by the view.
        

..............................................................................................................................................

# ORM (Object Relational Queries) Queries :::

1. **GET** ``` Model.objects.get(pk=1) ```
2. **Filter** ``` Model.objects.filter(userId=3) ```
3. **Filter + Values** ``` ModelA.objects.filter(sender_id=user_id).values("recipient", "id") ``` -> recipient and id are the fields inside ModelA
4. **Filter + Values + Referencing**``` ModelA.objects.filter(sender_id=user_id).values("recipient__id", "recipient__first_name") ```
  - first_name and id are the fields that are present in ModelB that ModelA is referencing
6. **__**
    - This notation is used to traverse relationships between models in Django's ORM queries.
7. **Create**  ``` Model.objects.create(name='Shikhar', age=24) ```
8. **Greater Than**  ``` Book.objects.filter(published_date__gt=date(2023, 1, 1)) ```
9. **Exclude + IN**  ``` Model.objects.exclude(id=userId).exclude(id__in=AnyList) ```
10. **Filter + Q + Order By**  ``` Chats.objects.filter(Q(sender_id=sender, recipient_id=receiver) | Q(sender_id=receiver, recipient_id=sender)).order_by("sent_at") ```
11. **Q**  The Q object in Django allows for complex queries using logical operators like & (AND), | (OR), and ~ (NOT).
11) **Range** ``` Model.objects.filter(Q(price__range=(40,100))) ```

## Examples :::

1. **Retrieve articles that are either written by the author "John" or published in 2022**
``` articles = Article.objects.filter(Q(author="John") | Q(published_year=2022)) ```

2.  **Retrieve users who are either active or have premium membership**
``` users = User.objects.filter(Q(is_active=True) | Q(has_premium_membership=True)) ``` 

3. **Retrieve products with a price greater than $100 and in the "Electronics" category**
``` products = Product.objects.filter(Q(price__gt=100) & Q(category="Electronics")) ```

4.  **Retrieve articles that are not published in the year 2021**
``` articles = Article.objects.filter(~Q(published_year=2021)) ```

5. **Retrieve users with names starting with 'J' or 'S'**
``` users = User.objects.filter(Q(name__startswith='J') | Q(name__startswith='S')) ```

6. **Retrieve products with prices between $50 and $100 or with a discount**
``` products = Product.objects.filter(Q(price__range=(50, 100)) | Q(discount__isnull=False)) ```

7. ### **Retrieve articles with titles containing "Django" or "Python" and published by "John"**
``` articles = Article.objects.filter(Q(title__icontains="Django") | Q(title__icontains="Python"), author="John") ```

8. **Retrieve orders containing products with prices less than $50 or quantities greater than 10**
``` orders = Order.objects.filter(Q(products__price__lt=50) | Q(products__quantity__gt=10)) ```

...........................................................................................................................

## Web Sockets

1. ```self.scope['query_string'].decode('utf8') ```
- self.scope['query_string'] results in 'query_string': b'token:.........'
- This is byte format and hence needs to be converted to string. Hence use decode('utf8')

2. **Query Dict**
- ``` query_string = b'token=eyJhbGciOiJ......8gJRpIpY&recipient=2'
query_dict = QueryDict(query_string.decode('utf-8'))
token = query_dict.get('token')
recipient = query_dict.get('recipient') ```

3. **Setup**

i) chat_app/settings.py -> ```  ASGI_APPLICATION = 'chat_app.asgi.application' ```
ii) Define application variable : 
  ``` application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
            URLRouter(
                websocket_urlpatterns
            )
        ),
}) ```

websocket_urlpatterns -> routing of websocket

iii) routing file :
``` websocket_urlpatterns = [
    re_path(r"ws/chat/", consumers.ChatConsumer.as_asgi()),
]
```

iv) Consumer.py file :

a)
``` class ChatConsumer(WebsocketConsumer):
        def connect(self):
        """Get the Access token / Recipient ID / User Id from Query String, generate a room and accept the connection"""

        self.room_name = self.generate_room_name(user.id, recipient_id)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()


    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data):
        """ This is called when message is sent from Frontend to Server. This is called only once for one message"""

        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, 
            {
                "type": "chat_message", 
                "message": message,
            }
        )

    def chat_message(self, event):
        """ This is called twice for a single message (sent from Frontend). After receiving the message, this function is called """

        self.send(text_data=json.dumps({"message": message }))
```
