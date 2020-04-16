
from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField
from wtforms.validators import DataRequired, Optional, URL


"""
FORM VALIDATION:

-For each form, validation is performed in the following ways:

- Back-End:   Defining classes that specify form attributes
              Validating them via the WTForms library

- Front-End:  Invoking the appropriate back-end form class (i.e. VenueForm, ArtistForm, ShowForm) based on the specific form
              HTML "pattern" attribute via regular expressions

"""




"""
VenueForm:

Standardizes venue forms and defines their attributes

Utilized when user clicks on "Post a venue" on the homepage
or "Edit Venue" on a specific venue page
"""
class VenueForm(FlaskForm):
    
    name = StringField(
        'name', validators=[DataRequired()]
    )

    city = StringField(
        'city', validators=[DataRequired()]
    )

    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )

    address = StringField(
        'address', validators=[DataRequired()]
    )
    
    phone = StringField('phone', validators=[DataRequired()] )


    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )

    """
    Function that validates:
    
    -The number of selected genres (Maximum limit is 5)
    -If at least one of the following is filled out: Website, Facebook Link
    """
    def validate(self):                                                         

        field_validation = FlaskForm.validate(self)                                           

        if not field_validation:                                                              
            return False                                                        

        #Enum restriction for the "genres" field
        #Up to 5 genres can be selected
        if len(self.genres.data) > 5:                                          
            self.genres.errors.append('Please select no more than 5 genres!')    
            return False

        #Checks that either the Website or the Facebook link is filled out
        #Both can be filled out as well
        if len(self.website_link.data) == 0 and len(self.facebook_link.data) == 0:
            self.website_link.errors.append('Please enter either at least one of the following: Website, Facebook Link!')
            return False                                                        

        return True  

    
    website_link = StringField(
        'website_link', validators=[URL(), Optional()]

    )


    image_link = StringField(
        'image_link', validators=[URL(), DataRequired()]

    )

    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]

    )

    seeking_talent = SelectField(
        'seeking_talent', validators=[DataRequired()],
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ]
    )

    seeking_description = StringField(
        'description'
    )


"""
ArtistForm:

Standardizes artist forms and defines their attributes

Utilized when user clicks on "Post an artist" on the homepage
or "Edit Artist" on a specific artist page
"""
class ArtistForm(FlaskForm):
    
    name = StringField(
        'name', validators=[DataRequired()]
    )

    city = StringField(
        'city', validators=[DataRequired()]
    )

    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    
    phone = StringField('phone', validators=[DataRequired()] )

    
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )


    """
    Function that validates:
    
    -The number of selected genres (Maximum limit is 5)
    -If at least one of the following is filled out: Website, Facebook Link
    """
    def validate(self):                                                         

        field_validation = FlaskForm.validate(self)                                           

        if not field_validation:                                                              
            return False                                                        

        #Enum restriction for the "genres" field
        #Up to 5 genres can be selected
        if len(self.genres.data) > 5:                                          
            self.genres.errors.append('Please select no more than 5 items')    
            return False

        #Checks that either the Website or the Facebook link is filled out
        #Both can be filled out as well
        if len(self.website_link.data) == 0 and len(self.facebook_link.data) == 0:
            self.website_link.errors.append('Please enter either at least one of the following: Website, Facebook Link!')
            return False                                                        

        return True



    website_link = StringField(
        'website_link', validators=[URL(), Optional()]
    )


    image_link = StringField(
        'image_link', validators=[URL(), DataRequired()]

    )

    facebook_link = StringField(
        'facebook_link', validators=[URL(), Optional()]

    )

    seeking_venues = SelectField(
        'seeking_venues', validators=[DataRequired()],
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No')
        ]
    )

    seeking_description = StringField(
        'description'
    )

    

"""
ShowForm:

Standardizes show forms and defines their attributes

Utilized when user clicks on "Post a Show" on the homepage

"""
class ShowForm(FlaskForm):

    artist_name = StringField(
        'artist_name', validators=[DataRequired()]

    )

    venue_name = StringField(
        'venue_name', validators=[DataRequired()]

    )
    start_time = StringField(
        'start_time',
        validators=[DataRequired()]
        
    )