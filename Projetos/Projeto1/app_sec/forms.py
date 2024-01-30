from wtforms import StringField, SelectField, validators, PasswordField, Form, EmailField, DecimalField, IntegerField, FileField, ValidationError
from flask_wtf.file import FileAllowed

class LoginForm(Form):
    """Form to login in the website"""
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})

    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})


class AddOrder(Form):
    """Form to add a product to the shopping cart"""
    quantity = SelectField('', [validators.DataRequired()],
                           choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])


class ShoppingCart(Form):
    """Form to confirm order"""
    first_name = StringField('', [validators.length(min=3, max=20), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'First Name'})
    
    last_name = StringField('', [validators.length(min=3, max=20), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Last Name'})
    
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    
    mobile = StringField('', [validators.length(min=9, max=12)],
                        render_kw={'placeholder': 'Mobile'})

    address = StringField('', [validators.length(min=3),validators.DataRequired()],
                            render_kw={'autofocus': True, 'placeholder': 'Address'})

class DeleteCartForm(Form):
    """Form to delete a shopping cart item"""
    prodID = IntegerField('prodID', render_kw={'placeholder': 'prodID'})

    usrID = IntegerField('usrID', render_kw={'placeholder': 'usrID'})

class RegisterForm(Form):
    """Form to register a user in the website"""

    first_name = StringField('', [validators.length(min=3, max=20), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'First Name'})
    
    last_name = StringField('', [validators.length(min=3, max=20), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Last Name'})
    
    username = StringField('', [validators.length(min=3, max=25)], 
                           render_kw={'placeholder': 'Username'})
    
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    
    password = PasswordField('', [validators.length(min=3), validators.DataRequired()],
                             render_kw={'placeholder': 'Password'})
    
    description = StringField('', [validators.length(min=1)], 
                              render_kw={'autofocus': True, 'placeholder': 'Description'})

    mobile = StringField('', [validators.length(min=9, max=12)],
                        render_kw={'placeholder': 'Mobile'})

class UpdateRegisterForm(Form):
    """Form to update a field from the user profile"""
    first_name = StringField('First Name', [validators.length(min=3, max=25)],
                       render_kw={'autofocus':True, 'placeholder': 'First Name'})
    
    last_name = StringField('Last Name', [validators.length(min=3, max=25)],
                       render_kw={'autofocus':True, 'placeholder': 'Last Name'})
    
    username = StringField('Username', [validators.length(min=3, max=25)], 
                        render_kw={'placeholder': 'Username'})

    email = EmailField('Email', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    
    description = StringField('Description', [validators.length(min=1)], 
                              render_kw={'autofocus': True, 'placeholder': 'Description'})

    mobile = StringField('Mobile', [validators.length(min=11, max=15)],
                         render_kw={'placeholder': 'Mobile'})


class UpdatePasswordForm(Form):
    """Form to update password"""
    password = PasswordField('Password', [validators.length(min=3)],
                             render_kw={'placeholder': 'Old Password'})

    new_password = PasswordField('New Password', [validators.length(min=3)],
                                 render_kw={'placeholder': 'New Password'})

    confirm_password = PasswordField('Confirm Password', [validators.length(min=3)],
                                     render_kw={'placeholder': 'Confirm Password'})


class AddProductForm(Form):
    """Form to add a new product"""
    prod_name = StringField('', [validators.length(min=3, max=20), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Product Name'})
    
    price = DecimalField('', places=2, validators=[validators.InputRequired("Price is required")],
                         render_kw={'autofocus': True, "placeholder": "Price"})
    
    description = StringField('Description', [validators.length(min=1)], 
                              render_kw={'autofocus': True, 'placeholder': 'Description'})
    
    category = SelectField('', [validators.DataRequired()],
                           choices=[('Clothing','Clothing'),('FootWear','FootWear'),('Eletronics','Eletronics'),('Utilities','Utilities'),('Furniture','Furniture')])
    
    stock = IntegerField('', validators=[validators.DataRequired(), validators.NumberRange(min=1, message="Must have at least 1 product")],
                         render_kw={"autfocus": True, "placeholder": "Stock"})
    
    # image = FileField('', validators=[validators.InputRequired(message='Image is Required'), FileAllowed(['jpg', 'jpeg', 'png'], 'Only images files (.png, .jpeg, .jpg) are allowed')])

    image = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only images files (.png, .jpeg, .jpg) are allowed')])


class CommentForm(Form):
    """Form to add a new comment to a product"""
    rating = StringField('Rating', [validators.length(min=1, max=2)],
                       render_kw={'placeholder': 'Insert your rating (0 to 10)'})
    comment = StringField('Comment', [validators.length(min=3, max=5000)],
                       render_kw={'autofocus':True, 'placeholder': 'Insert your comment here'})

class DeveloperForm(Form):
    """Form for a developer to update products"""
    id = StringField('', [validators.length(min=1)],
                     render_kw={'placeholder': 'Input a product id ...'})